"""
Each field desired by the user is converted to a FieldPattern object.
A later release will make this class directly available to the user,
providing more advanded field search options.
"""

# --- Standard Library Imports ------------------------------------------------
from typing import List, Union, Optional

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable import exceptions
from fuzzytable.main.utils import get_repr

# --- Third Party Imports -----------------------------------------------------
# None


class FieldPattern:
    """
    Optional argument for :obj:`FuzzyTable subfields<fuzzytable.FuzzyTable>` parameter.

    FieldPattern arguments override FuzzyTable arguments of the same name.
    In the following example,
    the ``first_name`` FieldPattern uses approximate matching while ``last_name`` uses exact matching.

    >>> from fuzzytable import FuzzyTable
    >>> subfields = [
    ...     FieldPattern('first_name', approximate_match=False),
    ...     FieldPattern('last_name')
    ... ]
    >>> FuzzyTable(approximate_match=True, subfields=subfields)




    Args:
        name (``str``): SingleField name. This is the name that will given to a matched field.
            This parameter, along with any aliases supplied, are the search criteria.
        alias (``str`` or ``iterable`` thereof, default ``None``): Additional search criteria.
        approximate_match (``bool``, default ``None``): Overrides
            the default behavior of the :obj:`~fuzzytable.FuzzyTable` ``approximate_match`` parameter.
        min_ratio (``float``, default ``None``):  Overrides
            the default behavior of the :obj:`~fuzzytable.FuzzyTable` ``min_ratio`` parameter.
    """

    def __init__(
            self,
            name,
            alias=None,
            approximate_match: Optional[bool] = None,
            min_ratio: Optional[float] = None,
            contains_match: [bool] = False,
            multifield: [bool] = False,
    ):
        self.name = name
        self.alias = alias
        self.approximate_match = approximate_match
        self.min_ratio = min_ratio
        self.contains_match = bool(contains_match)
        self.multifield = bool(multifield)

        # These are not set yet.
        self.path = None
        self.sheetname = None
        self.col = None
        self.matched = False

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, value) -> None:
        if value is None:
            self._alias = []
        elif isinstance(value, str):
            self._alias = [value]
        else:
            self._alias = list(value)

    @property
    def min_ratio(self):
        return self._min_ratio

    @min_ratio.setter
    def min_ratio(self, value):
        if value is None:
            self._min_ratio = 0.6
            return
        try:
            if 0.0 < value <= 1.0:
                self._min_ratio = value
                return
        except TypeError:
            raise exceptions.InvalidRatioError(value)
        raise exceptions.InvalidRatioError(value)

    @property
    def terms(self) -> List[str]:
        return [self.name] + self.alias

    def __repr__(self):
        return get_repr(self)  # pragma: no cover


if __name__ == '__main__':
    pass
