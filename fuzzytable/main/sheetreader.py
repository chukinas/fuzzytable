"""
Interface between the csv/excel files and the rest of FuzzyTable
"""

# --- Standard Library Imports ------------------------------------------------
import csv
from contextlib import contextmanager

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable import exceptions

# --- Third Party Imports -----------------------------------------------------
from openpyxl.worksheet.worksheet import Worksheet as openpyxlWorksheet
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException


INFINITY = float("inf")
NEG_INFINITY = float("-inf")


class SheetReader:

    def __init__(self, path, sheetname=None) -> None:
        self.path = path
        self._row_count = None
        self.sheetname = sheetname

    def iter_row(self, start_row=None, end_row=None):
        # Generator Function for looping over rows
        if start_row is None:
            start_row = NEG_INFINITY
        if end_row is None:
            end_row = INFINITY
        with self.get_filereader() as filereader:
            for row_num, row in enumerate(filereader, 1):
                if row_num > end_row:
                    return
                if row_num >= start_row:
                    yield row
        self._row_count = row_num

    def iter_row_str(self, end_row=None):
        # Generator function for looping over row repr's
        for row in self.iter_row(end_row=end_row):
            yield repr(row)

    def get_row_str(self, row_num):
        # Use this only when you only care about this row and no other.
        # When looping to find best fit, use self.iter_row_str instead.
        row = self[row_num]
        return repr(row)

    def get_col(self, start_row, col_num):
        # Return column values as list
        col_index = col_num - 1
        return (
            row[col_index]
            for row in self.iter_row(start_row=start_row)
        )

    @property
    def row_count(self):
        if self._row_count is None:
            for _ in self.iter_row():
                pass  # iter_row populates self._row_count at the end
            return self.row_count
        else:
            return self._row_count

    def __getitem__(self, desired_row_num):
        for cur_row_num, row in enumerate(self.iter_row(), 1):
            if cur_row_num == desired_row_num:
                return row

    @contextmanager
    def get_filereader(self):
        file = open(self.path)
        yield csv.reader(file)
        file.close()

    # def __repr__(self):
    #     return get_repr(self)  # pragma: no cover


class CsvReader(SheetReader):

    def get_col(self, start_row, col_num):
        orig_col = super().get_col(start_row=start_row, col_num=col_num)
        return list(orig_col)


class ExcelReader(SheetReader):

    @contextmanager
    def get_filereader(self):
        try:
            wb = load_workbook(self.path, read_only=True)  # Lazy loader
            ws: openpyxlWorksheet = wb[self.sheetname]
        except InvalidFileException:
            raise exceptions.InvalidFileError(self.path)
        except KeyError:
            # worksheet not found
            raise exceptions.SheetnameError(self.path, self.sheetname)
        yield ws.iter_rows(values_only=True)

    def get_col(self, start_row, col_num):
        orig_col = super().get_col(start_row=start_row, col_num=col_num)
        return [str(val) for val in orig_col]


if __name__ == '__main__':
    # from tests.conftest import get_test_path
    # path = get_test_path('xlsx')
    # si_excel = ExcelReader(path, 'table_bottom_right')
    # with si_excel.get_filereader() as iter_rows:
    #     for row in iter_rows:
    #         print(type(repr(row)))
    pass
