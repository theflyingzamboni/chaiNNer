from __future__ import annotations

import math
from enum import Enum
from typing import Dict, Union

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import EnumInput, NumberInput
from ...properties.outputs import NumberOutput
from . import category as UtilityCategory


class MathOperation(Enum):
    ADD = "add"
    SUBTRACT = "sub"
    MULTIPLY = "mul"
    DIVIDE = "div"
    POWER = "pow"
    LOG = "log"
    MAXIMUM = "max"
    MINIMUM = "min"
    MODULO = "mod"
    PERCENT = "percent"


OP_LABEL: Dict[MathOperation, str] = {
    MathOperation.ADD: "Add: a + b",
    MathOperation.SUBTRACT: "Subtract: a - b",
    MathOperation.MULTIPLY: "Multiply: a × b",
    MathOperation.DIVIDE: "Divide: a ÷ b",
    MathOperation.POWER: "Exponent: a ^ b",
    MathOperation.LOG: "Logarithm: log a of b",
    MathOperation.MAXIMUM: "Maximum: max(a, b)",
    MathOperation.MINIMUM: "Minimum: min(a, b)",
    MathOperation.MODULO: "Modulo: a mod b",
    MathOperation.PERCENT: "Percent: a × b ÷ 100",
}

_special_mod_numbers = (0.0, float("inf"), float("-inf"), float("nan"))


@NodeFactory.register("chainner:utility:math")
class MathNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Perform mathematical operations on numbers."
        self.inputs = [
            NumberInput(
                "Operand a",
                minimum=None,
                maximum=None,
                precision=100,
                controls_step=1,
            ),
            EnumInput(MathOperation, "Math Operation", option_labels=OP_LABEL),
            NumberInput(
                "Operand b",
                minimum=None,
                maximum=None,
                precision=100,
                controls_step=1,
            ),
        ]
        self.outputs = [
            NumberOutput(
                "Result",
                output_type="""
                let a = Input0;
                let b = Input2;

                match Input1 {
                    MathOperation::Add      => a + b,
                    MathOperation::Subtract => a - b,
                    MathOperation::Multiply => a * b,
                    MathOperation::Divide   => a / b,
                    MathOperation::Power    => number::pow(a, b),
                    MathOperation::Log      => number::log(a) / number::log(b),
                    MathOperation::Maximum  => max(a, b),
                    MathOperation::Minimum  => min(a, b),
                    MathOperation::Modulo   => number::mod(a, b),
                    MathOperation::Percent  => a * b / 100,
                }
                """,
            )
        ]

        self.category = UtilityCategory
        self.name = "Math"
        self.icon = "MdCalculate"
        self.sub = "Math"

    def run(
        self, a: Union[int, float], op: MathOperation, b: Union[int, float]
    ) -> Union[int, float]:
        if op == MathOperation.ADD:
            return a + b
        elif op == MathOperation.SUBTRACT:
            return a - b
        elif op == MathOperation.MULTIPLY:
            return a * b
        elif op == MathOperation.DIVIDE:
            return a / b
        elif op == MathOperation.POWER:
            return a**b
        elif op == MathOperation.LOG:
            return math.log(b, a)
        elif op == MathOperation.MAXIMUM:
            return max(a, b)
        elif op == MathOperation.MINIMUM:
            return min(a, b)
        elif op == MathOperation.MODULO:
            if a in _special_mod_numbers or b in _special_mod_numbers:
                return a - b * math.floor(a / b)
            else:
                return a % b
        elif op == MathOperation.PERCENT:
            return a * b / 100
        else:
            raise RuntimeError(f"Unknown operator {op}")
