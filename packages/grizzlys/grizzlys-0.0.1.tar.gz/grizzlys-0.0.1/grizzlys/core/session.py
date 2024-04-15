"""
Module for instantiating a singleton Julia session for the grizzlys module
It could then be reused everywhere via import to interact with Julia from Python
e.g. `from grizzlys.core.session import julia as jl`
"""

import juliacall

julia = juliacall.newmodule("grizzlys")
