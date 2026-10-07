# AliPackage

> Applies gamma correction to one or two images.

**Category:** Classical Computer Vision / Preprocessing

---

## 1. Overview

AliPackage is a NovaVision **component** package with two executors:

1. **Gamma Correction (1 Image)** — `FirstExecutor`
2. **Gamma Correction (2 Images)** — `SecondExecutor` (applies the same setting to both images)

Gamma correction changes the brightness of an image with a power curve:
`output = 255 * (input / 255) ^ gamma`.
A gamma below 1 brightens the image (useful for dark / low-light images); a gamma above 1 darkens it.

**Typical use cases:**
- Brightening dark camera frames before further processing
- Normalizing the brightness of two images before comparing them

---

## 2. Inputs

### Gamma Correction (1 Image)

| Field Name | Kind/Type | Required | Description |
|---|---|---|---|
| `inputImage` | Image | Yes | Image to correct |

### Gamma Correction (2 Images)

| Field Name | Kind/Type | Required | Description |
|---|---|---|---|
| `inputImage` | Image | Yes | First image |
| `inputImage2` | Image | Yes | Second image |

---

## 3. Configuration Parameters

Both executors have the same configuration.

| Parameter | Type | Field Type (UI control) | Allowed Values / Range | Description |
|---|---|---|---|---|
| `GammaMode` | object | `dependentDropdownlist` | Brighten / Darken | Selects the mode; the fields below change with it |
| `Gamma` (Brighten) | number | `textInput` | 0.1 – 1.0 | Smaller value = brighter image |
| `Gamma` (Darken) | number | `textInput` | 1.0 – 5.0 | Larger value = darker image |
| `Channel` | object | `dropdownlist` | All Channels / Luminance Only | Where gamma is applied |

- **All Channels:** gamma is applied to B, G and R separately.
- **Luminance Only:** the image is converted to LAB and gamma is applied only to L (brightness), so colors are preserved.

> `ConfigExecutor` is not included in this table.

---

## 4. Outputs

| Executor | Output | Description |
|---|---|---|
| Gamma Correction (1 Image) | `outputImage` | Corrected image |
| Gamma Correction (2 Images) | `outputImage`, `outputImage2` | Both corrected images |

---

## 5. Project Structure

```
src/
├── executors/   # FirstExecutor.py, SecondExecutor.py
├── models/      # PackageModel.py
└── utils/       # image_ops.py (gamma logic), response.py
tests/test_local.py   # tests the gamma logic without the SDK
```

## 6. Local Test

```bash
pip install opencv-python-headless numpy
python tests/test_local.py
```

## Image Credits

- `images/dark.jpg`: OpenCV sample `building.jpg`, artificially darkened to simulate low light.
