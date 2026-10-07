import cv2
import numpy as np


# ================= ENHANCE (FirstExecutor) =================

def enhance_clahe(img, clip_limit=2.0, tile_size=8):
    """Yerel kontrast artırma. Görüntüyü küçük karelere bölüp her birinde
    kontrastı ayrı ayrı açar; karanlık/sisli görüntülerde detay çıkarır."""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)          # L: parlaklık, A-B: renk
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=float(clip_limit),
                            tileGridSize=(int(tile_size), int(tile_size)))
    l = clahe.apply(l)                                   # sadece parlaklığa uygula, renkler bozulmasın
    return cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2BGR)


def enhance_gamma(img, gamma=1.0, channel="All"):
    """Parlaklık eğrisi. gamma > 1 karanlık bölgeleri aydınlatır, < 1 koyulaştırır."""
    inv = 1.0 / float(gamma)
    table = ((np.arange(256) / 255.0) ** inv * 255).astype("uint8")   # 0-255 için hazır tablo
    if channel == "Luminance":
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = cv2.LUT(l, table)
        return cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2BGR)
    return cv2.LUT(img, table)


# ================= CHANGE DETECTION (SecondExecutor) =================

def _prepare_pair(before, after):
    """İki görüntüyü aynı boyuta getirip griye çevirir."""
    if before.shape[:2] != after.shape[:2]:
        after = cv2.resize(after, (before.shape[1], before.shape[0]))
    g1 = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)
    return after, g1, g2


def _draw_changes(mask, after, min_area):
    """Maskedeki beyaz bölgelerin etrafına kırmızı kutu çizer."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxed = after.copy()
    for c in contours:
        if cv2.contourArea(c) < min_area:                # küçük gürültüleri atla
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(boxed, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return boxed


def _make_heatmap(diff):
    """Farkı 0-255 aralığına yayıp renklendirir: mavi=aynı, kırmızı=en çok değişen."""
    diff_norm = cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX)
    return cv2.applyColorMap(diff_norm, cv2.COLORMAP_JET)


def change_absdiff(before, after, threshold=30, morphology="Open"):
    """Piksel piksel fark alır, eşikten büyük farkları 'değişim' sayar."""
    after, g1, g2 = _prepare_pair(before, after)
    diff = cv2.absdiff(g1, g2)
    _, mask = cv2.threshold(diff, int(threshold), 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    op = cv2.MORPH_OPEN if morphology == "Open" else cv2.MORPH_CLOSE
    mask = cv2.morphologyEx(mask, op, kernel)
    return _make_heatmap(diff), _draw_changes(mask, after, min_area=50)


def change_blurred(before, after, kernel_size=5, min_area=500):
    """Önce bulanıklaştırır (ışık/titreme gürültüsünü azaltır), sonra fark alır.
    Eşiği Otsu yöntemiyle otomatik seçer."""
    after, g1, g2 = _prepare_pair(before, after)
    k = int(kernel_size)
    g1 = cv2.GaussianBlur(g1, (k, k), 0)
    g2 = cv2.GaussianBlur(g2, (k, k), 0)
    diff = cv2.absdiff(g1, g2)
    _, mask = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=2)
    return _make_heatmap(diff), _draw_changes(mask, after, int(min_area))