"""
Currently, this module does nothing. Clearly.
A later release will make the DataPattern class available to the user.
It will provide tools for normalizing and parsing the values retrieved from each data cell.
"""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

############################################


# """Use normalization functions when you want to guarantee you get the data types you want.
#
# """
#
# # --- Standard Library Imports ------------------------------------------------
# import datetime
# import numbers
# import re
# from abc import ABC, abstractmethod
#
# # --- Third Party Imports -----------------------------------------------------
# # None
#
# # --- Intra-Package Imports ---------------------------------------------------
# # None
#
#
# # --- base class --------------------------------------------------------------
#
# class DataPattern(ABC):
#     """Base class for all normalization classes.
#     """
#
#     @abstractmethod
#     def apply_pattern(self, value):
#         """Abstract method that needs implemented when subclassed.
#
#         Args:
#             value:
#
#         Returns:
#
#         """
#         return value
#
#

#
# # --- Normalization "data types" ----------------------------------------------
#
# class STRING(DataPattern):
#     """Normalizes cell values to :obj:`str`.
#
#     Other Parameters:
#         strip_whitespace (``bool``, default ``True``): If `True`, remove leading and trailing whitespace.
#         exclude_excel_bool (``bool``, default ``True``): If `True`,
#             native excel booleans are normalized to empty string.
#         exclude_excel_dates (``bool``, default ``True``): If `True`,
#             native excel dates are normalized to empty string.
#
#     Warning:
#         All ``Other Parameters`` are not yet implemented.
#
#         Passing these arguments does nothing. No errors are raised.
#     """
#
#     def __init__(
#             self,
#             strip_whitespace=True,
#             exclude_excel_bool=True,
#             exclude_excel_dates=True,
#     ):
#         pass
#
#     def apply_pattern(self, value) -> str:
#         # """
#         #
#         # Args:
#         #     ratio: The ratio of an excel worksheet cell.
#         #
#         # Returns:
#         #     str: see class desription and parameters for details.
#         #
#         # """
#         if value is None or isinstance(value, (bool, datetime.date, datetime.datetime)):
#             return ''
#         return str(value).strip()
#
#
# class INTEGER_LIST(DataPattern):
#     """Normalize cell values to :obj:`list` of :obj:`int`.
#     """
#
#     def apply_pattern(self, value):
#         if isinstance(value, (int, float)):
#             return [int(value)]
#         else:
#             string_of_ints = re.findall(r'\d+', str(value))
#             return [int(val) for val in string_of_ints]
#
#
# class INTEGER(DataPattern):
#     """Normalize cell values to ``int``.
#
#     Other Parameters:
#         allow_none (``bool``, default ``True``): Determines response when cell is either blank or contains no digits.
#             If `True`, allow the return of ``None``.
#             If `False`, return ``-1`` instead.
#
#     Warning:
#         All ``Other Parameters`` are not yet implemented.
#
#         Passing these arguments does nothing. No errors are raised.
#     """
#
#     def __init__(
#             self,
#             allow_none=True,
#     ):
#         pass
#
#     def apply_pattern(self, value) -> int:
#
#         # Try simple conversion first
#         if isinstance(value, (int, float)):
#             return int(value)
#
#         # Then the more resource intensive method
#         ints = INTEGER_LIST().apply_pattern(value)
#         if len(ints) == 0:
#             return None
#         return ints[0]
#
#
# # def FLOAT():
# #     def norm_float_val(ratio):
# #         if isinstance(ratio, bool):
# #             return None
# #         if isinstance(ratio, numbers.Real):
# #             return float(ratio)
# #         return None
# #     return norm_float_val
# #
# #
# # def bool_val(ratio):
# #     if isinstance(ratio, bool):
# #         return ratio
# #     return nan
# #
# #
# # def convert_first_digit_bw_2_6(ratio):
# #     min_integer = 2
# #     max_integer = 6
# #     # first_integer = 0  # default ratio
# #     value_string = convert_string(ratio)
# #     if pd.isna(value_string):
# #         return nan
# #     pattern = f'[{min_integer}-{max_integer}]'
# #     p = re.compile(pattern)  # Regular Expression for individual digits
# #     list_of_individual_digits = p.findall(value_string)
# #     if len(list_of_individual_digits) > 0:
# #         first_digit = list_of_individual_digits[0]
# #         return int(first_digit)
# #     return pd.np.nan
# #
# #
# # def convert_tuple_words(ratio):
# #     """get a list of alphanumeric sequences"""
# #     value_string = convert_string(ratio)
# #     if pd.isna(value_string):
# #         return nan
# #     p = re.compile(r'\w+')  # Regular Expression for consecutive alphabetical characters
# #     words = tuple(p.findall(value_string))
# #     if len(words) == 0:
# #         return nan
# #     return words
