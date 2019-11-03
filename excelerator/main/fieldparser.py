class FieldParser:
    """Optional argument for  :obj:`exclerator.TableParser` :obj:`fields` parameter.

    When using ``FieldParser``, typically you will pass a sequence of them to a
    ``TableParser`` as ``fields`` parameter. The ``TableParser`` generally finds the row in a worksheet that best
    matches each FieldParser object.

    Args:
        name (``str``): Field name.
            Default behavior: TableParser find the header matching this value.
        alias (``str`` or ``list`` thereof, default ``None``):

    Other Parameters:
        approx_match (``bool``, default ``False``): Allows
        normalize (:obj:`normalize.NormalizeBase`, default ``None``)
            This overrides any normalize classes in ``TablerParser`` ``normalize`` parameter.

    Note: When a sequence of ``FieldParser`` objects is passed to a ``TableParser``, \
        each ``FieldParser`` is mapped to a single header cell if possible. \
        This happens in the following order:
        1. Find the header row. See ``TableParser`` parameters for details.
        2. For each ``field_parser.name``, find exact matches.
        3. For each ``field_parser.get_aliases()``, find exact matches.
        4. For each ``field_parser.name``, find approximate matches.
        5. For each ``field_parser.get_aliases()``, find approximate matches.

        Each header cell can only be mapped to a single FieldParser object.

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

    def get_aliases(self, include_field_name=False):
        """The values compared to when locating the field in a worksheet.

        Returns:
            set:

        See Also:
            parameters: :obj:`alias`, :obj:`alias_include_name`
        """


        # Normalize self.alias to a set
        if self.alias is None:
            alias = set()
        elif isinstance(self.alias, str):
            alias = {self.alias}
        else:
            alias = set(self.alias)

        # Logic for returning all_alias:
        if len(alias) == 0:
            return self.name
        elif self.alias_include_name:
            alias.add(self.name)
        return alias


if __name__ == '__main__':
    mylist = set('bye forty'.split())
    f = FieldParser(
        'hello',
        # alias=mylist,
        alias_include_name=False,
    )
    print(f.all_alias)
