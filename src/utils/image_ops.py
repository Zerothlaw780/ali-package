import cv2
import numpy as np


def _to_uint8(img):
    """cv2.LUT only accepts 8-bit images; convert anything else to uint8 (0-255)."""
    img = np.asarray(img)
    if img.dtype == np.uint8:
        return img
    if np.issubdtype(img.dtype, np.floating) and img.size and img.max() <= 1.0:
        img = img * 255.0
    return np.clip(img, 0, 255).astype(np.uint8)


def apply_gamma(img, gamma=1.0, channel="All"):
    """Gamma correction with a lookup table.

    gamma < 1 brightens the image, gamma > 1 darkens it.
    channel="All" applies it to every color channel,
    channel="Luminance" applies it only to brightness (L in LAB), keeping colors.
    """
    img = _to_uint8(img)
    table = np.array([((i / 255.0) ** float(gamma)) * 255 for i in range(256)]).astype("uint8")

    if channel == "Luminance" and img.ndim == 3 and img.shape[2] == 3:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = cv2.LUT(l, table)
        return cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2BGR)

    return cv2.LUT(img, table)
