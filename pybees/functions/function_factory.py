from functions.function_type import FunctionType
from functions.rastrigin import Rastrigin


def build_function(typ):
    if typ == FunctionType.RASTRIGIN.value:
        return Rastrigin()
