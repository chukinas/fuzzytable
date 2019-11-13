"""
This is the library's API class. It delegates the heavy lifting to SheetParser.
After instantiation / data extraction, the FuzzyTable object acts like a
dictionary and is the main way for the user to interact with the extracted data.
The user can interact with the data in three other ways:
- field_names
- records
- sheet
"""

# --- Standard Library Imports ------------------------------------------------
import collections
import reprlib
from pathlib import Path
from typing import Union, Optional, List

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable.patterns import SheetPattern
from fuzzytable.patterns.fieldpattern import get_fieldpatterns
from fuzzytable.parsers.sheetparser import SheetParser


# --- Third Party Imports -----------------------------------------------------
# None


class Initial(object):
    pass


INITIAL = Initial()


FieldSummary = collections.namedtuple("FieldSummary", "header_name col_num field_name norm_func")
# This class for internal use. It stores information about each field to make data output simpler.


class FuzzyTable(collections.abc.Mapping):
    """Extract a table from a spreadsheet.

    This is the main class of fuzzytable. Instantiate it to extract the data.
    Then interact with the extracted table in one of four ways:

    - :obj:`~fuzzytable.FuzzyTable` as a dictionary (keys are field names; values are column data)
    - :obj:`FuzzyTable.records<fuzzytable.datamodel.Records>`: sequence of records represented as dictionaries.
    - List of :obj:`FuzzyTable.field_names<fuzzytable.datamodel.Field>` objects.
    - :obj:`FuzzyTable.sheet<fuzzytable.datamodel.Sheet>`: additional worksheet attributes (e.g. header row number, path).

    See tutorials:

    - :ref:`Standard Usage<tutstandard>`
    - :ref:`Data Model<tutdatamodel>`

    Args:
        path (path-like :obj:`str`, :obj:`pathlib.Path` object): Must be a valid csv or excel file.
        sheetname (``str``, default ``None``): Must be supplied if ``path`` is an excel file.
        header_row (:obj:`int` >=1, default :obj:`None`): Row number m where
            FuzzyTable expects the headers to be.

            * ``None``: m = 1
            * ``int``: m = header_row
        header_row_seek (:obj:`bool`, ``int`` >= 1, default :obj:`False`):If Truthy:
            ignore header_row. Instead, FuzzyTable seeks the best fit header row within the first n rows.

            * ``int``: n = header_row_seek
            * other truthy value: n = 20
        fields (:obj:`str` or iterable thereof, default :obj:`None`)
            * ``None``: extract field_names for each non-``None`` cell in header row.
            * ``str`` or iterable thereof: extract matching field_names matching a cell in the header row.
        approximate_match (``bool``, default False): If True, fields will match if they are at
            least 60% similar to the field names supplied. This cutout value can be set with min_ratio
        min_ratio (``float``, default None): The minimum similarity threshold for matching headers.
            Must be float 0.0 < x <= 1.0

    Attributes:
        records: Return :obj:`~fuzzytable.datamodel.Records` object, a generator yielding records (rows), each represented as a dictionary.
        fields: Return list of :obj:`~fuzzytable.datamodel.Field` objects, with such attributes as ``name``, ``header``, ``data``, ``col_num``.
        sheet: Return :obj:`~fuzzytable.datamodel.Sheet` object, whose attributes store additional metadata about the worksheet.

    Raises:
        :obj:`fuzzytable.exceptions.FuzzyTableError`:
            This is the module base exception. It is never itself raised,
            but you can use it to catch all exceptions raised by the FuzzyTable class.
            See :doc:`exceptions` for all other exceptions raised by FuzzyTable.
    """


    def __init__(
            self,
            path: Union[str, Path],
            sheetname: Optional[str] = None,
            fields: Optional[Union[List[str], str]] = None,
            header_row: Optional[int] = None,
            header_row_seek: Union[bool, int] = False,
            name: Optional[str] = None,
            approximate_match=False,
            min_ratio=None,
    ):

        sheet_reader = SheetPattern(path, sheetname).sheet_reader
        field_patterns = get_fieldpatterns(fields, approximate_match, min_ratio)
        sheet_parser = SheetParser(sheet_reader, field_patterns, header_row, header_row_seek)

        self.name = name
        self.fields = sheet_parser.fields
        self.sheet = sheet_parser.sheet_summary
        self.records = sheet_parser.records

        self._fields_dict = {
            field.name: field.data
            for field in self.fields
        }

    def __len__(self):
        return len(self._fields_dict)

    def __getitem__(self, item):
        # Return the data from a specified field
        return self._fields_dict[item]

    def __iter__(self):
        yield from self._fields_dict

    def keys(self):
        """Like ``dict.keys()``.
        Return a generator yielding field names."""
        return (key for key in self)

    def values(self):
        """Like ``dict.values()``.
        Return a generator yielding column data."""
        return (self[key] for key in self.keys())

    def items(self):
        """Like ``dict.items()``.
        Return a generator yielding field name / column data tuples."""
        return zip(self.keys(), self.values())

    def __repr__(self):
        name = self.__class__.__name__
        if self.name is not None:
            name += repr(self.name)
        fieldnames = list(self.keys())
        fieldsrepr = reprlib.repr(fieldnames)
        obj_id = hex(id(self))
        return f"<{name} {fieldsrepr} {obj_id}>"
