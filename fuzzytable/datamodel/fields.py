"""
Fields are the core of the FuzzyTable data model.
They store the data, location, header name, etc.
"""

# --- Standard Library Imports ------------------------------------------------
from typing import Optional, List, Iterable
from abc import ABC, abstractmethod

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable.main.utils import get_repr

# --- Third Party Imports -----------------------------------------------------
# None


class Field(ABC):
    """
    Shared attributes/methods:
    header
    col_num
    name
    matched
    data
    ratio
    __getitem__
    __len__
    """
    pass


class SingleField(Field):
    """
    Represents a single column of your table.

    A single FuzzyTable object will have several SingleField objects, stored as a list in ``FuzzyTable.field_names``.
    SingleField objects are the source of truth for table contents.
    Remove a field from ``FuzzyTable.field_names`` and it disappears from the ``FuzzyTable`` and ``FuzzyTable.records`` views as well.

    >>> import fuzzytable
    >>> ft = fuzzytable.FuzzyTable('birthdays.csv')
    >>> first_name = ft.field_names[0]
    >>> first_name.col_num
    1
    >>> first_name.data
    ['John', 'Typhoid', 'Jane']
    >>> str(first_name)
    "<SingleField 'first_name' 0x10dcce8>"

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
    ) -> None:
        super().__init__()
        # populated during init
        self.header = header
        self.col_num = col_num

        # populated during match with FieldPattern
        self._name = None
        self.matched = False
        self.data = None
        self.ratio = None
        self.cellpattern = None

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

    def __getitem__(self, item):
        return self.data[item]

    def __len__(self):
        return len(self.data)


class MultiField(Field):
    """
    Represents one or more columns of your table.

    """

    def __init__(self, name, fields: List[SingleField]) -> None:
        super().__init__()
        self.name = name
        self.subfields = list(sorted(fields, key=lambda f: f.col_num))
        # self._len = len(subfields)
        # self._header_row = header_row
        # self._row_count = row_count
        self.matched = True
        self.cellpattern = None

    @property
    def header(self):
        return tuple(field.header for field in self.subfields)

    @property
    def data(self):
        return [
            self[i]
            for i in range(len(self))
        ]

    @property
    def ratio(self):
        # return minimum ratio of all subfields
        return min(field.ratio for field in self.subfields)

    def __len__(self):
        return len(self.subfields[0])

    def __getitem__(self, item):
        return tuple(
            field.data[item]
            for field in self.subfields
        )

    @property
    def col_nums(self):
        return [field.col_num for field in self.subfields]

    @property
    def col_num(self):
        return self.col_nums[0]

    @property
    def col_num_last(self):
        return self.col_nums[-1]


class RowField(SingleField):

    def __init__(self, header_row_num, sheet_row_count):
        super().__init__(
            header='row',
            col_num=-1,
        )
        self.data = range(header_row_num + 1, sheet_row_count + 1)


if __name__ == '__main__':
    pass
