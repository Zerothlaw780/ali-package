import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.AliPackage.src.utils.response import build_response
from components.AliPackage.src.models.PackageModel import PackageModel
from components.AliPackage.src.utils.image_ops import apply_gamma


class SecondExecutor(Component):

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image1 = self.request.get_param("inputImage")
        self.image2 = self.request.get_param("inputImage2")
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
        img1 = Image.get_frame(
            img=self.image1,
            redis_db=self.redis_db
        )
        img2 = Image.get_frame(
            img=self.image2,
            redis_db=self.redis_db
        )

        gamma = self.gamma_mode.gamma.value
        channel = self.gamma_mode.channel.value.value
        img1.value = apply_gamma(img1.value, gamma, channel)
        img2.value = apply_gamma(img2.value, gamma, channel)

        self.image1 = Image.set_frame(
            img=img1,
            package_uID=self.uID,
            redis_db=self.redis_db
        )
        self.image2 = Image.set_frame(
            img=img2,
            package_uID=self.uID,
            redis_db=self.redis_db
        )

        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
