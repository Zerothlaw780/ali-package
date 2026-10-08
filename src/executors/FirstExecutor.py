import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.demoPackageAli.src.utils.response import build_response
from components.demoPackageAli.src.models.PackageModel import PackageModel
from components.demoPackageAli.src.utils.image_ops import apply_gamma


class FirstExecutor(Component):

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image = self.request.get_param("inputImage")
        self.gamma_mode = (
            self.request.model
            .configs
            .executor
            .value
            .value
            .configs
            .gammaMode
            .value
        )

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        img = Image.get_frame(
            img=self.image,
            redis_db=self.redis_db
        )

        mode = self.gamma_mode
        if mode.name == "Brighten":
            gamma = mode.gammaBrighten.value
        else:
            gamma = mode.gammaDarken.value
        channel = mode.channel.value.value
        img.value = apply_gamma(img.value, gamma, channel)

        self.image = Image.set_frame(
            img=img,
            package_uID=self.uID,
            redis_db=self.redis_db
        )

        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
