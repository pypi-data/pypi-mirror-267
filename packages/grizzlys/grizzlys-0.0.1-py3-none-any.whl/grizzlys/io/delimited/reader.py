from pathlib import Path

from juliacall import convert

from grizzlys._utils.decorators import julia_using
from grizzlys.core.session import julia as jl


@julia_using(["DataFrames", "DelimitedFiles"])
def read_delimited(filepath: str | Path, delimiter: str, header: bool):
    if len(delimiter) != 1:
        raise ValueError(rf"Delimiter must be a single character, got {delimiter!r}")
    else:
        _delimiter = convert(jl.Char, delimiter)
    _filepath = str(filepath)
    if header:
        data, head = jl.DelimitedFiles.readdlm(_filepath, _delimiter, header=header)
        df = jl.DataFrame(data, jl.vec(head))
    else:
        data = jl.DelimitedFiles.readdlm(_filepath, _delimiter, header=header)
        df = jl.DataFrame(data, jl.seval(":auto"))
    return df
