import os
import sys
import cv2
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.utils.image_ops import enhance_clahe, enhance_gamma, change_absdiff, change_blurred

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
IMG = os.path.join(HERE, "..", "images")
os.makedirs(OUT, exist_ok=True)


def load_or_make():
    before = cv2.imread(os.path.join(IMG, "before.jpg"))
    after = cv2.imread(os.path.join(IMG, "after.jpg"))
    if before is not None and after is not None:
        return before, after
    print("images/before.jpg ve after.jpg yok, sentetik görüntü kullanılıyor")
    before = np.full((400, 600, 3), 90, np.uint8)
    cv2.rectangle(before, (50, 50), (150, 150), (200, 200, 200), -1)
    after = before.copy()
    cv2.rectangle(after, (350, 200), (450, 300), (40, 180, 40), -1)   # yeni nesne
    return before, after


before, after = load_or_make()
dark = (before * 0.3).astype(np.uint8)        # enhance testi için karartılmış görüntü

cv2.imwrite(f"{OUT}/1_dark_input.jpg", dark)
cv2.imwrite(f"{OUT}/2_clahe.jpg", enhance_clahe(dark, 3.0, 8))
cv2.imwrite(f"{OUT}/3_gamma.jpg", enhance_gamma(dark, 2.2, "Luminance"))

heat, boxed = change_absdiff(before, after, 30, "Open")
cv2.imwrite(f"{OUT}/4_absdiff_heatmap.jpg", heat)
cv2.imwrite(f"{OUT}/5_absdiff_boxes.jpg", boxed)

heat, boxed = change_blurred(before, after, 5, 500)
cv2.imwrite(f"{OUT}/6_blurred_heatmap.jpg", heat)
cv2.imwrite(f"{OUT}/7_blurred_boxes.jpg", boxed)

print("Bitti! Çıktılar:", OUT)