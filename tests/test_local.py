"""Local test for the gamma logic (no NovaVision SDK needed).

Run from the repo root:  python tests/test_local.py
Results are written to tests/output/.
"""
import os
import sys

import cv2

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "src", "utils"))
from image_ops import apply_gamma  # noqa: E402

IMG = os.path.join(ROOT, "images")
OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)

img = cv2.imread(os.path.join(IMG, "dark.jpg"))
if img is None:
    raise SystemExit("images/dark.jpg not found")

cases = {
    "1_input.jpg": img,
    "2_brighten_0.5_all.jpg": apply_gamma(img, 0.5, "All"),
    "3_brighten_0.5_luminance.jpg": apply_gamma(img, 0.5, "Luminance"),
    "4_darken_2.0_all.jpg": apply_gamma(img, 2.0, "All"),
}
for name, out in cases.items():
    cv2.imwrite(os.path.join(OUT, name), out)
    print(f"{name}: mean brightness = {out.mean():.1f}")
