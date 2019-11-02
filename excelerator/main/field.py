class Field:
    """Defines a single column of Excel data to read.

    Args:
        name (``str``)

        alias (``list`` of ``str``, ``str``, default ``None``)

        alias_include_name (``bool``, default ``True``): If ``True`` (default),
            the ``all_alias`` property returns a set of values
            that includes ``name`` and the contents of ``alias``.
            If ``False``, ``name`` is excluded.
            No effect if ``alias`` is empty.

    Other Parameters:
        exact_match (``bool``, default ``True``)
        normalize (:obj:`normalize.NormalizeBase`, default ``None``)

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

    @property
    def all_alias(self):
        """The values compared to when locating the field in a worksheet.

        Returns:
            set: all

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
    f = Field(
        'hello',
        # alias=mylist,
        alias_include_name=False,
    )
    print(f.all_alias)
