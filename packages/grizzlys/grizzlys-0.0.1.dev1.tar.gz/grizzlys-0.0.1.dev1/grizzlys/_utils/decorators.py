from functools import wraps
from typing import Sequence
from grizzlys.core.session import julia as jl


def julia_using(modules: Sequence[str]):
    def using_decorator(function: callable):
        @wraps(function)
        def wrapper(*args, **kwargs):
            jl.seval(rf"using {','.join(modules)}")
            return function(*args, **kwargs)

        return wrapper

    return using_decorator
