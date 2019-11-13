"""
Second major piece of the FuzzyTable data model.
Records class is essentially a view on the data stored in Field objects.
"""

# --- Standard Library Imports ------------------------------------------------
import collections
from typing import List, Dict
import itertools

# --- Intra-Package Imports ---------------------------------------------------
# from fuzzytable.datamodel import Field
from fuzzytable.datamodel.fields import Field, RowField

# --- Third Party Imports -----------------------------------------------------
# None


class Records(collections.abc.Sequence):
    """
    A sequence of dictionaries each representing a row of data.

    >>> import fuzzytable
    >>> ft = fuzzytable.FuzzyTable('birthdays.csv')
    >>> ft.records[1]
    {'first_name': 'Typhoid', 'last_name': 'Mary', 'birthday': '2-Aug-83', 'row': 3}

    Does not support deleting items. That must be done via :obj:`fuzzytable.datamodel.Field`
    """

    def __init__(
        self,
        fields: List[Field],
        header_row_num: int,
        row_count: int,
        include_row_num: bool = True,
    ) -> None:

        self.header_row_num: int = header_row_num
        self._len = row_count - self.header_row_num

        self.fields = None
        self._orig_fields = fields
        self._row_field = RowField(
            header_row_num=self.header_row_num,
            sheet_row_count=self.header_row_num + len(self)
        )
        self.include_row_num = include_row_num  # this has to come after self.field_names and .row_field

    @property
    def include_row_num(self):
        """
        Default ``True``. If ``True``, **all** views will show an additional `row` Field.

        >>> list(ft.keys())
        ['first_name', 'last_name', 'birthday', 'row']
        >>> ft.records.include_row_num = False
        >>> list(ft.keys())
        ['first_name', 'last_name', 'birthday']
        >>> ft.records[1]
        {'first_name': 'Typhoid', 'last_name': 'Mary', 'birthday': '2-Aug-83'}

        note:
            This property needs to be moved to the FuzzyTable class.
        """
        return self._include_row_num

    @include_row_num.setter
    def include_row_num(self, value):
        self._include_row_num = value
        if value:
            fields = list(self._orig_fields)
            fields.append(self._row_field)
            self.fields = fields
        else:
            self.fields = list(self._orig_fields)

    def __getitem__(self, item: int) -> Dict[str, List]:
        record = dict()
        for field in self.fields:
            record[field.name] = field.data[item]
        return record

    def __iter__(self):
        yield from (
            self[index]
            for index in range(len(self))
        )

    def __len__(self):
        return self._len

    def __eq__(self, other):
        empty_dict = dict()
        try:
            for self_record, other_record in itertools.zip_longest(self, other, fillvalue=empty_dict):
                self_dict = dict(self_record)
                other_dict = dict(other_record)
                if self_dict != other_dict:
                    return False
        except TypeError:
            return False
        return True

    # def __repr__(self):
    #     return get_repr(self)  # pragma: no cover
