from importlib.metadata import PackageNotFoundError, version

from .core import (
    ExtractError,
    ValidationError,
    extract,
    extract_from_file,
    extract_from_yaml,
    schema,
    schema_from_file,
    schema_from_yaml,
)
from .types import (
    Clear,
    Field,
    FieldType,
    Options,
    RegexSub,
    ScalarType,
    ArrayType,
    Schema,
    Split,
    TransformStep,
)

try:
    __version__ = version("selectolax-schema")
except PackageNotFoundError:
    # Keep source-tree imports usable before the distribution is installed.
    __version__ = "0+unknown"

__all__ = [
    "__version__",
    "ExtractError",
    "ValidationError",
    "extract",
    "extract_from_file",
    "extract_from_yaml",
    "schema",
    "schema_from_file",
    "schema_from_yaml",
    # types
    "Schema",
    "Field",
    "FieldType",
    "ScalarType",
    "ArrayType",
    "Options",
    "Clear",
    "RegexSub",
    "Split",
    "TransformStep",
]

