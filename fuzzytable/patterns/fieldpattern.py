"""
Each field desired by the user is converted to a FieldPattern object.
A later release will make this class directly available to the user,
providing more advanded field search options.
"""

# --- Standard Library Imports ------------------------------------------------
from typing import List, Optional

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable import exceptions
from fuzzytable.main.string_analysis import mode_setter, DefaultValue
from fuzzytable.main.utils import get_repr
from fuzzytable.patterns.cellpattern import normalize_cellpattern

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
            *Deprecated in v0.18. To be removed in v1.0. Use* ``mode`` *instead.*
        min_ratio (``float``, default ``None``):  Overrides
            the default behavior of the :obj:`~fuzzytable.FuzzyTable` ``min_ratio`` parameter.
        contains_match (``bool``, default ``False``): Overrides the standard ratio-based approximate matching.
            Instead, a match succeeds if any of this field's terms are contained in a cell string.
            *Deprecated in v0.18. To be removed in v1.0. Use* ``mode`` *instead.*
        multifield (``bool``, default ``False``):
        cellpattern (:obj:`~fuzzytable.patterns.cellpattern.CellPattern` or any callable):
            This normalizes this field's data.
        mode (None or ``str``): Choose from ``'exact'``, ``'approx'``, or ``'contains'``.
            ``mode`` overrides approximate_match and contains_match.
        searchterms_excludename (``bool``, default ``False``): If True, the FieldPattern `name` is not used
            as a search term; only aliases are used. This means a FieldPattern with `searchterms_excludename` and no aliases
            will produce no matches!
        case_sensitive (None or ``bool``, default ``True``): Used when seeking header row and
            matching Fields to FieldPatterns.
    """

    def __init__(
            self,
            name,
            alias=None,
            # converts to `mode`, which overrides FuzzyTable mode:
            approximate_match: Optional[bool] = None,
            # Overrides FuzzyTable value:
            min_ratio: Optional[float] = DefaultValue,
            # The IS NO corresponding FuzzyTable value:
            contains_match: [bool] = False,
            # The IS NO corresponding FuzzyTable value:
            multifield: [bool] = False,
            # The IS NO corresponding FuzzyTable value:
            cellpattern=None,
            # API Change: reorder parameters here and in other classes
            # Overrides FuzzyTable value:
            mode=DefaultValue,
            # API Change: need to add 'exact' default back in.
            # The IS NO corresponding FuzzyTable value:
            searchterms_excludename=False,
            case_sensitive=DefaultValue,
    ):
        self.name = name
        self.alias = alias
        self.min_ratio = min_ratio
        self.multifield = bool(multifield)
        self.cellpattern = normalize_cellpattern(cellpattern)
        self.searchterms_excludename = searchterms_excludename
        self._mode = mode_setter(mode, approximate_match, contains_match)
        self._case_sensitive = casesensitive_setter(case_sensitive)
        self.fuzzytable = None  #

    @property
    def case_sensitive(self):
        attr_value = self._get_value_allow_fuzzytable_to_override('_case_sensitive')
        return casesensitive_getter(attr_value)

    @property
    def mode(self):
        attr_value = self._get_value_allow_fuzzytable_to_override('_mode')
        return mode_getter(attr_value)

    def _get_value_allow_fuzzytable_to_override(self, attr):
        # FieldPattern attributes override the 'global' arguments passed to FuzzyTable.
        # Any FieldPattern attributes that were left at default use the FuzzyTable's value.
        self_attr = getattr(self, attr)
        if self_attr is not DefaultValue:
            return self_attr
        else:
            return getattr(self.fuzzytable, attr)

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
        attr_value = self._get_value_allow_fuzzytable_to_override('_min_ratio')
        return minratio_getter(attr_value)

    @min_ratio.setter
    def min_ratio(self, value):
        self._min_ratio = minratio_setter(value)

    @property
    def terms(self) -> List[str]:  # API Change to 'search_terms'. Update docs as well.
        if self.searchterms_excludename:
            a = 1
            return self.alias
        else:
            return [self.name] + self.alias

    def __repr__(self):
        return get_repr(self)  # pragma: no cover


def casesensitive_getter(value):
    if value is DefaultValue:
        return True
    else:
        return value


def casesensitive_setter(value):
    if value is DefaultValue:
        return value
    else:
        return bool(value)


def minratio_getter(minratio):
    if minratio is DefaultValue:
        return 0.6
    else:
        return minratio


def minratio_setter(value):
    if value in [None, DefaultValue]:
        return DefaultValue
    try:
        if 0.0 < value <= 1.0:
            return value
    except TypeError:
        raise exceptions.InvalidRatioError(value)
    raise exceptions.InvalidRatioError(value)


def mode_getter(value):
    if value is DefaultValue:
        return 'exact'
    else:
        return value


if __name__ == '__main__':
    pass
