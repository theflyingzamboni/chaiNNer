from __future__ import annotations

from typing import Tuple

import numpy as np

from ...impl.onnx.model import OnnxRemBgModel
from ...impl.onnx.session import get_onnx_session
from ...impl.rembg.bg import remove_bg
from ...node_base import NodeBase, group
from ...node_factory import NodeFactory
from ...properties import expression
from ...properties.inputs import ImageInput, OnnxRemBgModelInput
from ...properties.inputs.generic_inputs import BoolInput
from ...properties.inputs.numeric_inputs import NumberInput, SliderInput
from ...properties.outputs import ImageOutput
from ...utils.exec_options import get_execution_options
from . import category as ONNXCategory


@NodeFactory.register("chainner:onnx:rembg")
class RemBgNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Run rembg"
        self.inputs = [
            ImageInput(),
            OnnxRemBgModelInput(),
            BoolInput("Post-process Mask", default=False),
            BoolInput("Alpha Matting", default=False),
            group("conditional-enum", {"enum": 3, "conditions": [1, 1, 1],},)(
                SliderInput(
                    "Foreground Threshold", minimum=1, maximum=255, default=240
                ),
                SliderInput("Background Threshold", maximum=254, default=10),
                NumberInput("Erode Size", minimum=1, default=10),
            ),
        ]
        self.outputs = [
            ImageOutput(
                "Image",
                image_type="""Input0""",
            ),
            ImageOutput(
                "Mask", image_type=expression.Image(size_as="Input0"), channels=1
            ),
        ]

        self.category = ONNXCategory
        self.name = "Remove Background"
        self.icon = "ONNX"
        self.sub = "Processing"

    def run(
        self,
        img: np.ndarray,
        model: OnnxRemBgModel,
        post_process_mask: int,
        alpha_matting: int,
        foreground_threshold: int,
        background_threshold: int,
        kernel_size: int,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Upscales an image with a pretrained model"""
        session = get_onnx_session(model, get_execution_options())

        return remove_bg(
            img,
            session,
            bool(alpha_matting),
            foreground_threshold,
            background_threshold,
            alpha_matting_erode_size=kernel_size,
            post_process_mask=bool(post_process_mask),
        )
