from pydantic import validator
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