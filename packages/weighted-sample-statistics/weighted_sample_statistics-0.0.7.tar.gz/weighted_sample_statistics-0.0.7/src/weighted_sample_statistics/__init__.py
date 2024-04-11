import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from .core import (
    Weightedweighted_sample_statistics as Weightedweighted_sample_statistics,
)
from .variable_properties import VariableProperties as VariableProperties
from .utils import rename_all_variables as rename_all_variables
from .utils import make_negation_name as make_negation_name
from .utils import get_records_select as get_records_select
