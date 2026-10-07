from sdks.novavision.src.helper.package import PackageHelper

from components.AliPackage.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    FirstExecutorOutputs,
    FirstExecutorResponse,
    FirstExecutor,
    SecondExecutorOutputs,
    SecondExecutorResponse,
    SecondExecutor,
    OutputImage,
    OutputImage2
)


def _build(executor, context):
    config_executor = ConfigExecutor(value=executor)
    package_configs = PackageConfigs(executor=config_executor)

    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs
    )
    return package.build_model(context)


def build_executor1_response(context):
    outputs = FirstExecutorOutputs(
        outputImage=OutputImage(value=context.image)
    )
    response = FirstExecutorResponse(outputs=outputs)
    return _build(FirstExecutor(value=response), context)


def build_executor2_response(context):
    outputs = SecondExecutorOutputs(
        outputImage=OutputImage(value=context.image1),
        outputImage2=OutputImage2(value=context.image2)
    )
    response = SecondExecutorResponse(outputs=outputs)
    return _build(SecondExecutor(value=response), context)


def build_response(context):
    if hasattr(context, "image2"):
        return build_executor2_response(context)
    return build_executor1_response(context)
