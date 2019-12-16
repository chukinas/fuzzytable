"""CellPatterns normalize fields' data values"""

# --- Standard Library Imports ------------------------------------------------
import datetime
import re
from typing import Optional, List
from datetime import datetime
from functools import lru_cache

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable.patterns.cellpattern import CellPattern
from fuzzytable.main.utils import force_list
from fuzzytable.main import string_analysis as strings
from fuzzytable import exceptions

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

    .. code-block:: python

        # warm_colors.py

        from fuzzytable import FuzzyTable, FieldPattern, cellpatterns

        iswarmcolor_field = FieldPattern(
            name="is_warm_color",
            cellpattern=cellpatterns.Boolean,
        )

        warmcolor_table = FuzzyTable(
            path='warm_colors.csv',
            fields=['color', boolean_field],
            approximate_match=True,
        )

    .. csv-table:: warm_colors.csv
       :file: _docstringfiles/warm_colors.csv
       :widths: auto
       :align: left

    >>> python warm_colors.py
    >>> for record in warmcolor_table.records
    ...     print(record)
    ...
    {'color': 'brown', 'is_warm_color': True}
    {'color': 'green', 'is_warm_color': False}
    {'color': 'yellow', 'is_warm_color': True}
    {'color': 'black', 'is_warm_color': False}

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
    Return "choice" that best fits the cell value.

    This pattern operates in one of these three modes:
    - ``exact``
    - ``approx``
    - ``contains``

    .. code-block:: python

        # cities.py

        from fuzzytable import FuzzyTable, FieldPattern, cellpatterns

        state_field = FieldPattern(
            name="states",
            cellpattern=cellpatterns.StringChoice(
                choices='pennsylvania new_york north_carolina'.split()
                case_sensitive=False,
                approximate_match=True,
                min_ratio=0.5,
            ),
        )

        cities_table = FuzzyTable(path='cities.csv', fields=['city', state_field],)

    .. csv-table:: cities.csv
       :file: _docstringfiles/cities.csv
       :widths: auto
       :align: left

    >>> python cities.py
    >>> for record in cities_table.records
    ...     print(record)
    ...
    {'city': 'New York', 'state': 'new_york'}
    {'city': 'Philadelphia', 'state': 'pennsylvania'}
    {'city': 'Albany', 'state': 'new_york'}
    {'city': 'Raleigh', 'state': 'north_carolina'}
    {'city': 'Wilmington', 'state': None}

    Args:
        choices (sequence of strings or dict whose values are sequences of strings) If dict,
            the key is what is returned.
        case_sensitive (``bool``, default ``False``)
        dict_use_keys (``bool``, default ``True``) If ``True`` and if ``choices`` is a dictionary,
            the keys of the dict will be used as search terms.
        default (Any, default ``None``) This value is returned if the cell value does not match
            any of the choices given.
        approximate_match (``bool``, default ``False``)
            *Deprecated in v0.18. To be removed in v1.0. Use* ``mode`` *instead.*
            True overrides ``contains_match``.
        min_ratio (``float`` within [0.0, 1.0], default ``0.6``)
        case_sensitive (``bool``, default ``False``)
        contains_match (``bool``, default ``True``)
            *Deprecated in v0.18. To be removed in v1.0. Use* ``mode`` *instead.*
        mode (None or ``str``): Choose from ``'exact'``, ``'approx'``, or ``'contains'``.
            ``mode`` overrides approximate_match and contains_match.
    """

    user_instantiated = True
    get_str = String().apply_pattern

    def __init__(
        self,
        choices,
        dict_use_keys=True,
        default=None,
        approximate_match=False,
        min_ratio=0.6,
        case_sensitive=False,
        contains_match=True,
        mode=None,
    ):
        super().__init__(default)
        self.min_ratio = min_ratio
        self.case_sensitive = case_sensitive

        self.mode = strings.mode_setter(mode, approximate_match, contains_match)

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
        value_str = StringChoice.get_str(value)
        bestkey = strings.get_bestkey(
            search_dict=self._choices,
            target=value_str,
            min_ratio=self.min_ratio,
            case_sensitive=self.case_sensitive,
            mode=self.mode,
            default_value=self.default_value,
        )
        return bestkey.name


class StringChoiceMulti(CellPattern):
    """
    Check cell for desired strings. Return list of found strings.

    .. code-block:: python

        # colors.py

        from fuzzytable import FuzzyTable, FieldPattern, cellpatterns

        warm_color_field = FieldPattern(
            name="warm_colors",
            cellpattern=cellpatterns.StringChoiceMulti(
                choices='red pink brown yellow'.split()
                case_sensitive=False,
            ),
        )

        colors_table = FuzzyTable(
            path='colors.csv',
            fields=[warm_color_field, 'cool_colors'],
            approximate_match=True,
        )

    .. csv-table:: colors.csv
       :file: _docstringfiles/colors.csv
       :widths: auto
       :align: left

    >>> python colors.py
    >>> for record in colors_table.records
    ...     print(record)
    ...
    {'warm_colors': ['red', 'brown', 'yellow'], 'cool_colors': None}
    {'warm_colors': ['brown'], 'cool_colors': 'green'}
    {'warm_colors': ['red', 'yellow'], 'cool_colors': 'blue'}
    {'warm_colors': [], 'cool_colors': 'black'}

    Args:
        choices (sequence of strings)
        case_sensitive (``bool``, default ``True``)
    """

    user_instantiated = True
    get_str = String().apply_pattern

    def __init__(self, choices: List[str], case_sensitive=True):
        super().__init__(default_value=None)
        self.case_sensitive = case_sensitive
        self.choices_orig = choices
        self.choices_compare = choices if case_sensitive else [choice.lower() for choice in choices]

    def apply_pattern(self, value):
        found_choices = []
        value = StringChoice.get_str(value)
        value = value if self.case_sensitive else value.lower()
        for choice_orig, choice_compare in zip(self.choices_orig, self.choices_compare):
            if choice_compare in value:
                found_choices.append(choice_orig)
        return found_choices
