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


# --- Normalization "data types" ----------------------------------------------
# def convert_first_digit_bw_2_6(ratio):
#     min_integer = 2
#     max_integer = 6
#     # first_integer = 0  # default ratio
#     value_string = convert_string(ratio)
#     if pd.isna(value_string):
#         return nan
#     pattern = f'[{min_integer}-{max_integer}]'
#     p = re.compile(pattern)  # Regular Expression for individual digits
#     list_of_individual_digits = p.findall(value_string)
#     if len(list_of_individual_digits) > 0:
#         first_digit = list_of_individual_digits[0]
#         return int(first_digit)
#     return pd.np.nan
#
#
# def convert_tuple_words(ratio):
#     """get a list of alphanumeric sequences"""
#     value_string = convert_string(ratio)
#     if pd.isna(value_string):
#         return nan
#     p = re.compile(r'\w+')  # Regular Expression for consecutive alphabetical characters
#     words = tuple(p.findall(value_string))
#     if len(words) == 0:
#         return nan
#     return words
