"""CellPatterns normalize fields' data values"""

# --- Standard Library Imports ------------------------------------------------
import datetime
import re
from typing import Optional, List
from datetime import datetime

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable.patterns.cellpattern import CellPattern
from fuzzytable.main.utils import force_list

# --- Third Party Imports -----------------------------------------------------
# None


class String(CellPattern):
    """
    Normalizes cell values to ``str``.
    """

    def __init__(self, default_value=''):
        super().__init__(default_value=default_value)

    def apply_pattern(self, value) -> str:
        if value is None:
            return self.default_value
        value = str(value)
        value = value.strip()
        return value
        # try:
        #     value = str(value)
        #     value = value.strip()
        #     return value
        # except TypeError:
        #     return self.default_value


class IntegerList(CellPattern):
    """
    Normalize cell values to ``list`` of ``int``.
    """

    def __init__(self):
        super().__init__(default_value=[])

    def apply_pattern(self, value):
        if value is None or isinstance(value, bool):
            return self.default_value
        if isinstance(value, (int, float)):
            return [int(value)]
        try:
            return [int(float(value))]
        except (TypeError, ValueError):
            string_of_ints = re.findall(r'\d+', str(value))
            return [int(val) for val in string_of_ints]


class Integer(CellPattern):
    """
    Normalize cell values to ``int``.
    """

    def apply_pattern(self, value) -> Optional[int]:
        try:
            if not isinstance(value, str):
                return value[0]
        except TypeError:
            pass
        if isinstance(value, bool) or value is None:
            return self.default_value
        if isinstance(value, datetime):
            return value.year
        try:
            return int(float(value))
        except ValueError:
            int_list = IntegerList().apply_pattern(value)
            if len(int_list) > 0:
                return int_list[0]
            else:
                return self.default_value
            # return self.default_value
        # except ValueError:
        # return self.default_value


class Float(CellPattern):
    """
    Normalize cell values to ``float``.
    """

    def apply_pattern(self, value) -> Optional[float]:
        try:
            if not isinstance(value, str):
                return float(value[0])
        except TypeError:
            pass
        if isinstance(value, bool) or value is None:
            return self.default_value
        if isinstance(value, datetime):
            return float(value.year)
        try:
            return float(value)
        except ValueError:
            int_list = IntegerList().apply_pattern(value)
            if len(int_list) > 0:
                return float(int_list[0])
            else:
                return self.default_value


class WordList(CellPattern):
    """
    Normalize cell values to a list of words (no digits, no punctuation).
    """

    get_str = String().apply_pattern

    def apply_pattern(self, value) -> List[str]:
        value_str = WordList.get_str(value)
        # p = re.compile(r'\w+')  # Regular Expression for consecutive alphabetical characters
        p = re.compile(r'[a-zA-Z]+')
        words = list(p.findall(value_str))
        return words


class Boolean(CellPattern):
    """
    Normalize cell values to booleans.
    """
    def apply_pattern(self, value) -> bool:
        return bool(value)


class Digit(CellPattern):
    """
    Normalize cell values to an integer between 0-9.
    """

    get_str = String().apply_pattern

    def apply_pattern(self, value) -> Optional[int]:
        min_integer = 0
        max_integer = 9
        value_str = Digit.get_str(value)
        pattern = f'[{min_integer}-{max_integer}]'
        p = re.compile(pattern)  # Regular Expression for individual digits
        list_of_individual_digits = p.findall(value_str)
        try:
            first_digit = list_of_individual_digits[0]
            return int(first_digit)
        except IndexError:
            return None


class StringChoice(CellPattern):
    """
    Normalize cell values to a given list with a default value.

    ``choices`` can be either a list or a dict.
    If a dict, the keys are the choices that will be returned as data.
    The values are used to match values. So are the keys, if ``dict_use_keys`` is True.
    Case insensitive.
    """

    user_instantiated = True
    get_str = String().apply_pattern

    def __init__(self, choices, dict_use_keys=True, default=None):
        super().__init__(default)
        if isinstance(choices, dict):
            self._choices = {}
            for key in choices.keys():
                val = force_list(choices[key])
                if dict_use_keys:
                    val.append(key)
                self._choices[key] = val
        else:
            self._choices = {
                val: [val]
                for val in choices
            }
        # Here is how self._choices now stands:
        # It is a dictionary.
        # The keys are the values that be returned as cell values.
        # The values (and the values alone!) are the matching criteria.

    def apply_pattern(self, value):
        value = StringChoice.get_str(value)
        value.lower()
        for enum_name, match_criteria in self._choices.items():
            for match_criterion in match_criteria:
                if match_criterion in value:
                    return enum_name
        return self.default_value
