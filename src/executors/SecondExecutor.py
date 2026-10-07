import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.AliPackage.src.utils.response import build_response
from components.AliPackage.src.models.PackageModel import PackageModel
from components.AliPackage.src.utils.image_ops import change_absdiff, change_blurred


class SecondExecutor(Component):

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image1 = self.request.get_param("inputImage")
        self.image2 = self.request.get_param("inputImage2")
        self.method = (
            self.request.model
            .configs
            .executor
            .value
            .value
            .configs
            .detectionMethod
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

        m = self.method
        if m.name == "AbsDiff":
            heatmap, boxed = change_absdiff(
                img1.value,
                img2.value,
                threshold=m.threshold.value,
                morphology=m.morphology.value.value
            )
        else:
            heatmap, boxed = change_blurred(
                img1.value,
                img2.value,
                kernel_size=m.kernelSize.value.value,
                min_area=m.minArea.value
            )

        img1.value = heatmap
        img2.value = boxed

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
