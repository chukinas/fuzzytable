"""CellPatterns normalize fields' data values"""

# --- Standard Library Imports ------------------------------------------------
import datetime
import re
from typing import Optional
from datetime import datetime

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable.patterns.cellpattern import CellPattern

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

    def apply_pattern(self, value) -> Optional[int]:
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
