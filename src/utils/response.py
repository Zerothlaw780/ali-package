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
    SecondOutputImage
)


def build_executor1_response(context):
    output = OutputImage(value=context.image)
    outputs = FirstExecutorOutputs(outputImage=output)
    response = FirstExecutorResponse(outputs=outputs)

    executor = FirstExecutor(value=response)
    config_executor = ConfigExecutor(value=executor)
    package_configs = PackageConfigs(executor=config_executor)

    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs
    )

    return package.build_model(context)


def build_executor2_response(context):
    output1 = OutputImage(value=context.image1)
    output2 = SecondOutputImage(value=context.image2)

    outputs = SecondExecutorOutputs(
        outputImage=output1,
        outputImage2=output2
    )

    response = SecondExecutorResponse(outputs=outputs)

    executor = SecondExecutor(value=response)
    config_executor = ConfigExecutor(value=executor)
    package_configs = PackageConfigs(executor=config_executor)

    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs
    )

    return package.build_model(context)


def build_response(context):
    if hasattr(context, "image2"):
        return build_executor2_response(context)

    return build_executor1_response(context)
