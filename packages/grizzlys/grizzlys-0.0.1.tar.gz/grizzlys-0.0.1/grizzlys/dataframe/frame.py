"""
Module for grizzlys DataFrame Implementation
# TODO: elaborate here
"""

from grizzlys.core.session import julia as jl


class DataFrame:
    """
    # TODO: add docstring
    """

    def __init__(self, data=None):
        if data is None:
            self._df = jl.DataFrame()
