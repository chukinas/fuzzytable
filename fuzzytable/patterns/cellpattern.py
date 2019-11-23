"""
CellPattern provides tools for normalizing and parsing the values retrieved from each data cell.
"""

# --- Standard Library Imports ------------------------------------------------
from abc import ABC, abstractmethod
from inspect import isclass

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable import exceptions

# --- Third Party Imports -----------------------------------------------------
# None


# --- base class --------------------------------------------------------------

class CellPattern(ABC):
    """Base class for all normalization classes."""

    def __init__(self, default_value=None):
        self.default_value = default_value

    @abstractmethod
    def apply_pattern(self, value):
        raise NotImplementedError  # pragma: no cover


def normalize_cellpattern(value):
    # returns a single callable that each cell value will be passed through

    if value is None:
        return None
    elif isinstance(value, CellPattern):
        return value.apply_pattern
    elif isclass(value) and issubclass(value, CellPattern):
        return value().apply_pattern
    elif callable(value):
        return value
    else:
        raise exceptions.CellPatternError(value)
