"""Use normalization functions when you want to guarantee you get the data types you want.

"""

# --- Standard Library Imports ------------------------------------------------
import datetime
import numbers
import re

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None





# --- Normalization functions -------------------------------------------------

def norm_int_list(value):
    if isinstance(value, (int, float)):
        return [int(value)]
    else:
        string_of_ints = re.findall(r'\d+', str(value))
        return [int(val) for val in string_of_ints]


# --- Normalization "data types" ----------------------------------------------

def STRING():
    """Normalizes cell values to str data type.

    Note: Booleans and dates are converted to ``''``.
    Dates are converted to a string of the year alone.

    Returns:
        str: A string with leading and trailing whitespace removed.
    """
    def norm_string(value):
        if value is None or isinstance(value, (bool, datetime.date, datetime.datetime)):
            return ''
        return str(value).strip()
    return norm_string


def INTEGER():
    """Normalizes cell values to int data type.

    Returns:
        int
        None
    """
    def norm_int(value):
        if isinstance(value, (int, float)):
            return int(value)
        ints = norm_int_list(value)
        if len(ints) == 0:
            return None
        return ints[0]

    return norm_int


def INTEGER_LIST():
    """Normalizes cell values to list of integers.

    Returns:
        list(int)
    """
    return norm_int_list


# def FLOAT():
#     def norm_float_val(value):
#         if isinstance(value, bool):
#             return None
#         if isinstance(value, numbers.Real):
#             return float(value)
#         return None
#     return norm_float_val
#
#
# def bool_val(value):
#     if isinstance(value, bool):
#         return value
#     return nan
#
#
# def convert_first_digit_bw_2_6(value):
#     min_integer = 2
#     max_integer = 6
#     # first_integer = 0  # default value
#     value_string = convert_string(value)
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
# def convert_tuple_words(value):
#     """get a list of alphanumeric sequences"""
#     value_string = convert_string(value)
#     if pd.isna(value_string):
#         return nan
#     p = re.compile(r'\w+')  # Regular Expression for consecutive alphabetical characters
#     words = tuple(p.findall(value_string))
#     if len(words) == 0:
#         return nan
#     return words
