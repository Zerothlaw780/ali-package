import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.AliPackage.src.utils.response import build_response
from components.AliPackage.src.models.PackageModel import PackageModel
from components.AliPackage.src.utils.image_ops import enhance_clahe, enhance_gamma


class FirstExecutor(Component):

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image = self.request.get_param("inputImage")
        self.method = (
            self.request.model
            .configs
            .executor
            .value
            .value
            .configs
            .enhanceMethod
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

        m = self.method
        if m.name == "CLAHE":
            img.value = enhance_clahe(
                img.value,
                clip_limit=m.clipLimit.value,
                tile_size=m.tileSize.value.value
            )
        else:
            img.value = enhance_gamma(
                img.value,
                gamma=m.gammaValue.value,
                channel=m.channel.value.value
            )

        self.image = Image.set_frame(
            img=img,
            package_uID=self.uID,
            redis_db=self.redis_db
        )

        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
