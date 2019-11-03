"""
Fields are the core of the FuzzyTable data model.
They store the data, location, header name, etc.
"""

# --- Standard Library Imports ------------------------------------------------
from typing import Optional, List

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable.main.utils import get_repr

# --- Third Party Imports -----------------------------------------------------
# None


class Field:
    """
    Represents a single column of your table.

    A single FuzzyTable object will have several Field objects, stored as a list in ``FuzzyTable.fields``.
    Field objects are the source of truth for table contents.
    Remove a field from ``FuzzyTable.fields`` and it disappears from the ``FuzzyTable`` and ``FuzzyTable.records`` views as well.

    >>> import fuzzytable
    >>> ft = fuzzytable.FuzzyTable('birthdays.csv')
    >>> first_name = ft.fields[0]
    >>> first_name.col_num
    1
    >>> first_name.data
    ['John', 'Typhoid', 'Jane']
    >>> str(first_name)
    "<Field 'first_name' 0x10dcce8>"

    Attributes:
        name: return ``str``, the unique identifier for this field. Matches the field name you passed to FuzzyTable. Otherwise, return ``header``.
        data: return list of cell values.
        header: return ``str``, the value from the header cell. This may differ from ``name`` if fuzzy matching was specified.
        col_num: return ``int``, column number, 1-indexed. For example, a field extracted from column B has a col_num of 2.
        matched: return ``bool``. True if this field matches a field name passed to the FuzzyTable constructor.
    """

    def __init__(
        self,
        header: str,
        col_num: int,
        name: str = None,
    ) -> None:

        # populated during init
        self.header = header
        self.col_num = col_num

        # populated during match with FieldPattern
        self._name = name
        self.matched = False
        self.data = None

        # populated during later step after all matching is done

    @property
    def name(self):
        if self._name is None:
            return self.header
        else:
            return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def __repr__(self):
        return get_repr(self)  # pragma: no cover


class RowField(Field):

    def __init__(self, header_row_num, sheet_row_count):
        super().__init__(
            header='row',
            col_num=-1,
        )
        self.data = range(header_row_num + 1, sheet_row_count + 1)


if __name__ == '__main__':
    pass
