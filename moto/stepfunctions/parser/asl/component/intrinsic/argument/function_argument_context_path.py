from moto.stepfunctions.parser.asl.component.intrinsic.argument.function_argument import (
    FunctionArgument,
)
from moto.stepfunctions.parser.asl.eval.environment import Environment
from moto.stepfunctions.parser.asl.utils.json_path import extract_json


class FunctionArgumentContextPath(FunctionArgument):
    _value: str

    def __init__(self, json_path: str):
        super().__init__()
        self._json_path: str = json_path

    def _eval_body(self, env: Environment) -> None:
        self._value = extract_json(
            self._json_path, env.states.context_object.context_object_data
        )
        super()._eval_body(env=env)
