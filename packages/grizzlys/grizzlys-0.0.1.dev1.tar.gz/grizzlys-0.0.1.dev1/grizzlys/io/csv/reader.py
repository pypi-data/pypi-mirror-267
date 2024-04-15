from pathlib import Path

from grizzlys._utils.decorators import julia_using
from grizzlys.core.session import julia as jl


@julia_using(["DataFrames", "CSV"])
def read_csv(filepath: str | Path):
    return jl.DataFrame(jl.CSV.File(str(filepath)))
