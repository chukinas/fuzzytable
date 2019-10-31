"""table_reader docstring"""

# --- Standard Library Imports ------------------------------------------------
from contextlib import contextmanager

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from excelerator import utils
from excelerator import headers


class TableReader:
    """Reads Excel tabular data.

    Instantiating a TableReader object supplies all the rules for how to read tabular data (such as what fields/headers to look for; which row to look in). The TableReader's methods are where you supply the worksheet to be read and how you want the data to be outputted (e.g. as list of records, or dict of fields).

    Args:
         fields (list): A list of fields (str). If supplied, TableReader only outputs data whose headers match a string in this list.
         header_row_num (int or None):  If None (default), headers are assumed to be in row 1, with data starting on row 2. If supplied with an int, this is where the header row is assumed to be.
    """
    # TODO How to specify list of strings?
    # TODO How to specify int or None?

    def __init__(
            self,
            fields=None,
            header_row_num=None,
    ):
        self._ws = None
        self.fields = fields
        self.header_row_num = header_row_num

    def read_from(self, path, sheetname):
        """Output a table.

        Args:
            path (str or Path object): Path to workbook. Raise error if not found.
            sheetname (str): Worksheet name. Raise error if not found.

        Returns:
            dict: Headers as keys, list of data as values.
        """
        ws = utils.get_worksheet_from_path(path, sheetname)
        with self._set_ws(ws):
            result = dict()
            # TODO: fix this outer scope problem:
            _headers = utils.get_worksheet_row(
                worksheet=ws,
                row_int=self.header_row_num,
            )
            for col_num, header in enumerate(_headers, 1):
                if self._valid_header(header):
                    result[header] = utils.get_column(worksheet=ws,
                                                      col_num=col_num,
                                                      row_start=self._records_row_start,
                                                      row_end=ws.max_row)
            return result

    def _valid_header(self, value):
        if self.fields:
            return value in self.fields
        else:
            return value is not None

    @property
    def header_row_num(self):
        if self._ws is not None and self.fields is not None:
            return headers.get_best_match_row_number(
                worksheet=self._ws,
                values=self.fields,
            )
        else:
            return self._header_row_num

    @header_row_num.setter
    def header_row_num(self, value):
        if value is None:
            self._header_row_num = 1
        else:
            self._header_row_num = int(value)

    @property
    def _records_row_start(self):
        return self.header_row_num + 1

    @contextmanager
    def _set_ws(self, value):
        self._ws = value
        yield
        self._ws = None
