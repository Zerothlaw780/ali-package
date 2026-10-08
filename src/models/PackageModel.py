from pydantic import Field, validator

from typing import List, Optional, Union, Literal

from sdks.novavision.src.base.model import (
    Package,
    Image,
    Inputs,
    Configs,
    Outputs,
    Response,
    Request,
    Output,
    Input,
    Config
)


# ============ INPUTS / OUTPUTS ============

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

class SecondInputImage(Input):
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
        title = "Image 2"

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

class SecondOutputImage(Output):
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
        title = "Image 2"


class FirstExecutorInputs(Inputs):
    inputImage: InputImage


class FirstExecutorOutputs(Outputs):
    outputImage: OutputImage


class SecondExecutorInputs(Inputs):
    inputImage: InputImage
    inputImage2: SecondInputImage


class SecondExecutorOutputs(Outputs):
    outputImage: OutputImage
    outputImage2: SecondOutputImage


# ============ FIRST EXECUTOR CONFIGS (gamma, 1 image) ============

class FirstBrightenGamma(Config):
    name: Literal["GammaBrighten"] = "GammaBrighten"
    value: float = Field(ge=0.1, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Gamma (0.1 - 1.0)"


class FirstBrightenChannelAll(Config):
    name: Literal["All"] = "All"
    value: Literal["All"] = "All"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "All Channels"


class FirstBrightenChannelLuminance(Config):
    name: Literal["Luminance"] = "Luminance"
    value: Literal["Luminance"] = "Luminance"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Luminance Only"


class FirstBrightenChannel(Config):
    name: Literal["Channel"] = "Channel"
    value: Union[FirstBrightenChannelAll, FirstBrightenChannelLuminance]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Channel"


class FirstBrighten(Config):
    name: Literal["Brighten"] = "Brighten"
    gammaBrighten: FirstBrightenGamma
    channel: FirstBrightenChannel
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Brighten"

class FirstDarkenGamma(Config):
    name: Literal["GammaDarken"] = "GammaDarken"
    value: float = Field(ge=1.0, le=5.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Gamma (1.0 - 5.0)"


class FirstDarkenChannelAll(Config):
    name: Literal["All"] = "All"
    value: Literal["All"] = "All"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "All Channels"


class FirstDarkenChannelLuminance(Config):
    name: Literal["Luminance"] = "Luminance"
    value: Literal["Luminance"] = "Luminance"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Luminance Only"


class FirstDarkenChannel(Config):
    name: Literal["Channel"] = "Channel"
    value: Union[FirstDarkenChannelAll, FirstDarkenChannelLuminance]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Channel"


class FirstDarken(Config):
    name: Literal["Darken"] = "Darken"
    gammaDarken: FirstDarkenGamma
    channel: FirstDarkenChannel
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Darken"

class FirstExecutorGammaMode(Config):
    name: Literal["GammaMode"] = "GammaMode"
    value: Union[FirstBrighten, FirstDarken]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Gamma Mode"


class FirstExecutorConfigs(Configs):
    gammaMode: FirstExecutorGammaMode


class FirstExecutorRequest(Request):
    inputs: Optional[FirstExecutorInputs]
    configs: FirstExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class FirstExecutorResponse(Response):
    outputs: FirstExecutorOutputs


class FirstExecutor(Config):
    name: Literal["FirstExecutor"] = "FirstExecutor"
    value: Union[FirstExecutorRequest, FirstExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Gamma Correction (1 Image)"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


# ============ SECOND EXECUTOR CONFIGS (gamma, 2 images) ============

class SecondBrightenGamma(Config):
    name: Literal["GammaBrighten"] = "GammaBrighten"
    value: float = Field(ge=0.1, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Gamma (0.1 - 1.0)"


class SecondBrightenChannelAll(Config):
    name: Literal["All"] = "All"
    value: Literal["All"] = "All"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "All Channels"


class SecondBrightenChannelLuminance(Config):
    name: Literal["Luminance"] = "Luminance"
    value: Literal["Luminance"] = "Luminance"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Luminance Only"


class SecondBrightenChannel(Config):
    name: Literal["Channel"] = "Channel"
    value: Union[SecondBrightenChannelAll, SecondBrightenChannelLuminance]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Channel"


class SecondBrighten(Config):
    name: Literal["Brighten"] = "Brighten"
    gammaBrighten: SecondBrightenGamma
    channel: SecondBrightenChannel
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Brighten"

class SecondDarkenGamma(Config):
    name: Literal["GammaDarken"] = "GammaDarken"
    value: float = Field(ge=1.0, le=5.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Gamma (1.0 - 5.0)"


class SecondDarkenChannelAll(Config):
    name: Literal["All"] = "All"
    value: Literal["All"] = "All"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "All Channels"


class SecondDarkenChannelLuminance(Config):
    name: Literal["Luminance"] = "Luminance"
    value: Literal["Luminance"] = "Luminance"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Luminance Only"


class SecondDarkenChannel(Config):
    name: Literal["Channel"] = "Channel"
    value: Union[SecondDarkenChannelAll, SecondDarkenChannelLuminance]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Channel"


class SecondDarken(Config):
    name: Literal["Darken"] = "Darken"
    gammaDarken: SecondDarkenGamma
    channel: SecondDarkenChannel
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Darken"

class SecondExecutorGammaMode(Config):
    name: Literal["GammaMode"] = "GammaMode"
    value: Union[SecondBrighten, SecondDarken]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Gamma Mode"


class SecondExecutorConfigs(Configs):
    gammaMode: SecondExecutorGammaMode


class SecondExecutorRequest(Request):
    inputs: Optional[SecondExecutorInputs]
    configs: SecondExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class SecondExecutorResponse(Response):
    outputs: SecondExecutorOutputs


class SecondExecutor(Config):
    name: Literal["SecondExecutor"] = "SecondExecutor"
    value: Union[SecondExecutorRequest, SecondExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Gamma Correction (2 Images)"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


# ============ PACKAGE ============

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
    name: Literal["demoPackageAli"] = "demoPackageAli"
