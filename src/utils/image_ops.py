import cv2
import numpy as np


def apply_gamma(img, gamma=1.0, channel="All"):
    """Gamma correction with a lookup table.

    gamma < 1 brightens the image, gamma > 1 darkens it.
    channel="All" applies it to every color channel,
    channel="Luminance" applies it only to brightness (L in LAB), keeping colors.
    """
    inv = float(gamma)
    table = np.array([((i / 255.0) ** inv) * 255 for i in range(256)]).astype("uint8")

    if channel == "Luminance" and img.ndim == 3:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = cv2.LUT(l, table)
        return cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2BGR)

    return cv2.LUT(img, table)
