from pydantic import validator
from pydantic import Field
from typing import List, Optional, Union, Literal

from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Configs, Outputs,
    Response, Request, Output, Input, Config
)


# ---------- GİRDİLER ----------

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class InputImage2(Input):
    name: Literal["inputImage2"] = "inputImage2"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "After Image"


# ---------- ÇIKTILAR ----------

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class OutputImage2(Output):
    name: Literal["outputImage2"] = "outputImage2"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Detected Changes"


# ---------- EXECUTOR'LARA GÖRE GRUPLAMA ----------

class FirstExecutorInputs(Inputs):
    inputImage: InputImage


class FirstExecutorOutputs(Outputs):
    outputImage: OutputImage


class SecondExecutorInputs(Inputs):
    inputImage: InputImage
    inputImage2: InputImage2


class SecondExecutorOutputs(Outputs):
    outputImage: OutputImage
    outputImage2: OutputImage2


#  FIRST EXECUTOR AYARLARI

# --- CLAHE seçeneğinin alanları ---
class ClipLimit(Config):
    name: Literal["ClipLimit"] = "ClipLimit"
    value: float = Field(ge=0.5, le=10.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Clip Limit"


class TileSize4(Config):
    name: Literal["TileSize4"] = "TileSize4"
    value: Literal[4] = 4
    type: Literal["number"] = "number"
    field: Literal["option"] = "option"

    class Config:
        title = "4x4"


class TileSize8(Config):
    name: Literal["TileSize8"] = "TileSize8"
    value: Literal[8] = 8
    type: Literal["number"] = "number"
    field: Literal["option"] = "option"

    class Config:
        title = "8x8"


class TileSize16(Config):
    name: Literal["TileSize16"] = "TileSize16"
    value: Literal[16] = 16
    type: Literal["number"] = "number"
    field: Literal["option"] = "option"

    class Config:
        title = "16x16"


class TileSize(Config):
    name: Literal["TileSize"] = "TileSize"
    value: Union[TileSize4, TileSize8, TileSize16]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Tile Size"


class OptionCLAHE(Config):
    name: Literal["CLAHE"] = "CLAHE"
    value: Literal["CLAHE"] = "CLAHE"
    clipLimit: ClipLimit
    tileSize: TileSize
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "CLAHE"


# --- Gamma seçeneğinin alanları ---
class GammaValue(Config):
    name: Literal["GammaValue"] = "GammaValue"
    value: float = Field(ge=0.1, le=5.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Gamma"


class ChannelAll(Config):
    name: Literal["ChannelAll"] = "ChannelAll"
    value: Literal["All"] = "All"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "All Channels"


class ChannelLuminance(Config):
    name: Literal["ChannelLuminance"] = "ChannelLuminance"
    value: Literal["Luminance"] = "Luminance"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Luminance Only"


class Channel(Config):
    name: Literal["Channel"] = "Channel"
    value: Union[ChannelAll, ChannelLuminance]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Channel"


class OptionGamma(Config):
    name: Literal["Gamma"] = "Gamma"
    value: Literal["Gamma"] = "Gamma"
    gammaValue: GammaValue
    channel: Channel
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Gamma Correction"


# --- Ana menü ---
class EnhanceMethod(Config):
    name: Literal["EnhanceMethod"] = "EnhanceMethod"
    value: Union[OptionCLAHE, OptionGamma]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Enhance Method"


class FirstExecutorConfigs(Configs):
    enhanceMethod: EnhanceMethod

class Threshold(Config):
    name: Literal["Threshold"] = "Threshold"
    value: int = Field(ge=0, le=255)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Threshold"
class MorphOpen(Config):
    name: Literal["MorphOpen"] = "MorphOpen"
    value: Literal["Open"] = "Open"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Morph Open"

class MorphClose(Config):
    name: Literal["MorphClose"] = "MorphClose"
    value: Literal["Close"] = "Close"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Morph Close"

class Morphology(Config):
    name: Literal["Morphology"] = "Morphology"
    value: Union[MorphOpen, MorphClose]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Morphology"

class OptionAbsDiff(Config):
    name: Literal["AbsDiff"] = "AbsDiff"
    value: Literal["AbsDiff"] = "AbsDiff"
    threshold: Threshold
    morphology: Morphology
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Absolute Difference"

class KernelSize3(Config):
    name: Literal["KernelSize3"] = "KernelSize3"
    value: Literal[3] = 3
    type: Literal["number"] = "number"
    field: Literal["option"] = "option"

    class Config:
        title = "3x3"

class KernelSize5(Config):
    name: Literal["KernelSize5"] = "KernelSize5"
    value: Literal[5] = 5
    type: Literal["number"] = "number"
    field: Literal["option"] = "option"

    class Config:
        title = "5x5"

class KernelSize7(Config):
    name: Literal["KernelSize7"] = "KernelSize7"
    value: Literal[7] = 7
    type: Literal["number"] = "number"
    field: Literal["option"] = "option"

    class Config:
        title = "7x7"

class KernelSize(Config):
    name: Literal["KernelSize"] = "KernelSize"
    value: Union[KernelSize3, KernelSize5, KernelSize7]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Kernel Size"
class MinArea(Config):
    name: Literal["MinArea"] = "MinArea"
    value: int = Field(ge=0, le=100000)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Min Area"
class OptionBlurredDiff(Config):
    name: Literal["BlurredDiff"] = "BlurredDiff"
    value: Literal["BlurredDiff"] = "BlurredDiff"
    kernelSize: KernelSize
    minArea: MinArea
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Blurred Difference"


class DetectionMethod(Config):
    name: Literal["DetectionMethod"] = "DetectionMethod"
    value: Union[OptionAbsDiff, OptionBlurredDiff]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Detection Method"


class SecondExecutorConfigs(Configs):
    detectionMethod: DetectionMethod

# ============ REQUEST / RESPONSE ============

class FirstExecutorRequest(Request):
    inputs: Optional[FirstExecutorInputs]
    configs: FirstExecutorConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class FirstExecutorResponse(Response):
    outputs: FirstExecutorOutputs


class SecondExecutorRequest(Request):
    inputs: Optional[SecondExecutorInputs]
    configs: SecondExecutorConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class SecondExecutorResponse(Response):
    outputs: SecondExecutorOutputs


# ============ EXECUTOR'LAR ============

class FirstExecutor(Config):
    name: Literal["FirstExecutor"] = "FirstExecutor"
    value: Union[FirstExecutorRequest, FirstExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Enhance Image"
        json_schema_extra = {"target": {"value": 0}}


class SecondExecutor(Config):
    name: Literal["SecondExecutor"] = "SecondExecutor"
    value: Union[SecondExecutorRequest, SecondExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Change Detection"
        json_schema_extra = {"target": {"value": 0}}


# ============ PAKET ============

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FirstExecutor, SecondExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["AliPackage"] = "AliPackage"
