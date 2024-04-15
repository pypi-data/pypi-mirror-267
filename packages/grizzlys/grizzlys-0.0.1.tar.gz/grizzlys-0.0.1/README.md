![grizzlys](docs/logos/grizzlys-logo-cubes-with-text.png "grizzlys")

<hr>

<div style="text-align: center;">

[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json&label=Formatter)](https://github.com/charliermarsh/ruff)
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json&label=Linter)](https://github.com/charliermarsh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

</div>

# grizzlys: User-friendly Python DataFrames powered by Julia

**grizzlys** is a Python package that provides a native interface on top of Julia's popular
[___DataFrames.jl___](https://github.com/JuliaData/DataFrames.jl) package.

As a user-friendly alternative to existing Python packages such as __pandas__ and __polars__, it is designed to be a
convenient & easy to use DataFrames tool for data analysts, data engineers and data scientists alike, while still
providing high performance and abstractions, thanks to Julia's high-performance computing capabilities.

## Why you might consider using grizzlys

:white_check_mark: You are transitioning into Python from a **Julia** or **R** programming background

:white_check_mark: You are accustomed to working with **Jupyter notebooks** (or a REPL) and performing exploratory data
analysis **(EDA)** on-the-fly

:white_check_mark: You need a quick-and-dirty data wrangling tool that provides readymade **macros** and **convenience
functions** out of the box

:white_check_mark: You work with **statistics** or **linear algebra** often and require a wide range of
statistical/algebraic functions to be well-integrated with your DataFrames

## What is grizzlys (currently) NOT well-suited for

:x: __Larger-than-memory datasets__ - grizzlys' current implementation relies on data being stored in-memory, and therefore
it is not a good choice if you work with datasets that don't fit in your machine's RAM.

For such cases, using [__Polars__](https://github.com/pola-rs/polars) or
[__Dask DataFrames__](https://docs.dask.org/en/stable/dataframe.html) would be a much better choice as of now.

:x: __Lazy Evaluation__ - Similar to the above, grizzlys is currently designed to be fully eager, which means it always
immediately executes your code, as opposed to building a task/computation graph or thereabout and delaying execution
until it's needed.

:x: __Backwards compatibility__ - grizzlys is based on a relatively new programming language in Julia, and is developed
using an advanced version of Python, with little regard to end-of-life versions or any compatibility with Python 2.7,
for example.

You should therefore not rely on grizzlys for integrations with very old code or any other legacy/deprecated tools and
implementations.

:x: __Best-in-class Performance__ - Though Julia is widely considered a very high-performance language (it is actually a
major reason why it's used under the hood here), grizzlys is still a work-in-progress (WIP) and therefore does not
currently aim to compete with, or outperform, other high-performance DataFrame libraries, such as
[__Polars__](https://github.com/pola-rs/polars) (written in Rust) or
[__Modin__](https://github.com/modin-project/modin) (Multi-threaded pandas).

This, of course, might no longer be a limitation in the future, as __grizzlys__ will have undergone optimizations and
maturation.

<hr>

[Go to Top](#grizzlys-user-friendly-python-dataframes-powered-by-julia)
