"""
Sheet is the third piece of the datamodel.
It stores basic information about the sheet that the table was read from.
"""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None


# --- Third Party Imports -----------------------------------------------------
# None


class Sheet:
    """
    Container for sheet metadata, e.g. path, header row number, number of rows, etc

    >>> import fuzzytable
    >>> ft = fuzzytable.FuzzyTable('birthdays.csv')
    >>> ft.sheet.header_row_num
    1
    >>> ft.sheet.header_ratio
    0.0
    >>> ft.sheet.row_count
    4
    >>> ft.sheet.path
    WindowsPath('birthdays.csv')
    >>> ft.sheet.sheetname
    None

    Attributes:
        header_row_num: ``int`` row number, 1-indexed.
        header_ratio: ``float`` percent match between desired field names and the found headers. ``0.0`` if no field names were specified.
        row_count: ``int`` total number of rows in the worksheet.
        path: ``pathlib.Path`` object. ``str(path)`` to convert to string.
        sheetname: ``str`` name of worksheet if excel.
    """

    def __init__(self, header_row_num, row_count, ratio, path, sheetname):
        self.header_row_num = header_row_num
        self.header_ratio = ratio
        self.row_count = row_count
        self.path = path
        self.sheetname = sheetname

    # def __repr__(self):
    #     return get_repr(self)  # pragma: no cover
