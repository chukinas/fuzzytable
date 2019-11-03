"""
Each field desired by the user is converted to a FieldPattern object.
A later release will make this class directly available to the user,
providing more advanded field search options.
"""

# --- Standard Library Imports ------------------------------------------------
from typing import List, Union

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable import exceptions
from fuzzytable.main.utils import get_repr

# --- Third Party Imports -----------------------------------------------------
# None


class FieldPattern:
    """Optional argument for  :obj:`exclerator.FuzzyTable` :obj:`fields` parameter.

    When using ``FieldPattern``, typically you will pass a sequence of them to a
    ``FuzzyTable`` as ``fields`` parameter. The ``FuzzyTable`` generally finds the row in a worksheet that best
    matches each FieldPattern object.

    Args:
        name (``str``): Field name.
            Default behavior: FuzzyTable find the header matching this ratio.
        alias (``str`` or ``list`` thereof, default ``None``):

    Other Parameters:
        approx_match (``bool``, default ``False``): Allows
        normalize (:obj:`normalize.DataPattern`, default ``None``)
            This overrides any normalize classes in ``TablerParser`` ``normalize`` parameter.

    Note: When a sequence of ``FieldPattern`` objects is passed to a ``FuzzyTable``, \
        each ``FieldPattern`` is mapped to a single header cell if possible. \
        This happens in the following order:
        1. Find the header row. See ``FuzzyTable`` parameters for details.
        2. For each ``field_parser.name``, find exact matches.
        3. For each ``field_parser.get_aliases()``, find exact matches.
        4. For each ``field_parser.name``, find approximate matches.
        5. For each ``field_parser.get_aliases()``, find approximate matches.

        Each header cell can only be mapped to a single FieldPattern object.

    Warning:
        All ``Other Parameters`` are not yet implemented.

        Passing these arguments does nothing. No errors are raised.

    """

    def __init__(
            self,
            name,
            alias=None,
            alias_include_name=True,
            exact_match=True,
            normalize=None,
    ):
        self.name = name
        self.alias = alias
        self.alias_include_name = alias_include_name

        # These are not set yet.
        self.path = None
        self.sheetname = None
        self.col = None
        self.matched = False

    # def get_aliases(self, include_field_name=False):
    #     """The values compared to when locating the field in a worksheet.
    #
    #     Returns:
    #         set:
    #
    #     See Also:
    #         parameters: :obj:`alias`, :obj:`alias_include_name`
    #     """
    #
    #
    #     # Normalize self.alias to a set
    #     if self.alias is None:
    #         alias = set()
    #     elif isinstance(self.alias, str):
    #         alias = {self.alias}
    #     else:
    #         alias = set(self.alias)
    #
    #     # Logic for returning all_alias:
    #     if len(alias) == 0:
    #         return self.name
    #     elif self.alias_include_name:
    #         alias.add(self.name)
    #     return alias

    @property
    def terms(self) -> List[str]:
        return [self.name]

    def __repr__(self):
        return get_repr(self)  # pragma: no cover


def get_fieldpatterns(fields: Union[None, List[FieldPattern], List[str]]) -> List:
    # Get a clean iterable of FieldPattern objects

    if fields is None:
        return []
    elif isinstance(fields, str):
        return [FieldPattern(fields)]
    # elif isinstance(fields, FieldPattern):
    #     return [fields]

    # If we've gotten here, then we're dealing with an iterable of some sort
    try:
        return [
            field if isinstance(field, FieldPattern) else FieldPattern(field)
            for field in fields
        ]
    except TypeError:
        raise exceptions.InvalidFieldError(fields)


if __name__ == '__main__':
    pass
