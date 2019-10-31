"""table_reader docstring"""

# --- Standard Library Imports ------------------------------------------------
from contextlib import contextmanager
import collections

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from excelerator.main import excel_interface
from excelerator.main import headers


FieldSummary = collections.namedtuple("FieldSummary", "header_name col_num field_name norm_func")


class TableReader:
    """Reads Excel tabular data.

    Instantiating a TableReader object supplies all the rules for how to read tabular data (such as what
    fields/headers to look for; which row to look in). The TableReader's methods are where you supply
    the worksheet to be read and how you want the data to be outputted (e.g. as list of records,
    or dict of fields).

    Args:
         fields (:obj:`list`, default :obj:`None`): A list of fields (str). If supplied, TableReader only
            outputs data whose headers match a string in this list.
         header_row_num (:obj:`int`, default :obj:`None`):  If None (default), headers are assumed to be in row 1, with data starting on
            row 2. If supplied with an int, this is where the header row is assumed to be.
         normalize (:obj:`list` of :obj:`excelerator.normalize.NORM_TYPE()`, default :obj:`None`): No effect if fields arg is None.
            If fields is supplied, then the normalize
            functions are applied to the corresponding field.
            Use normalization functions when you want to guarantee you get the data types you want.

            There are two ways to use them.
            - First, send just

            Note:
            Here's a potential "gotcha". It's important that you always call the function. Example:

            ``
            from excelerator import TableReader, normalize

            tr = TableReader(
            fields='first_name last_name'.split(),
            normalize=normalize.STRING(),
            )
            ``

    Examples:
        >>> from excelerator import TableReader
        >>> tr = TableReader(
                fields='first_name last_name'.split(),
            )
        >>> fields = tr.get_fields(path='path/to/excel.xlsx', sheetname='names')

    """

    def __init__(
            self,
            fields=None,
            header_row_num=None,
            normalize=None,
    ):
        self._ws = None
        self.fields = fields
        self.header_row_num = header_row_num
        self.norm_funcs = normalize

    def get_records(self, path, sheetname):
        """Read the worksheet table with data grouped by record (i.e. rows).

        Args:
            path (str or Path object): Path to workbook. Raise error if not found.
            sheetname (str): Worksheet name. Raise error if not found.

        Returns:
            list: one item per record (row). Each record is represented as a dictionary of fieldname: cellvalue pairs.
        """
        ws = excel_interface.get_worksheet_from_path(path, sheetname)
        with self._set_ws(ws):
            field_summaries = self._get_fieldsummaries()
            result = list()
            for row in range(self._records_row_start, ws.max_row + 1):
                record = dict()
                for field in field_summaries:
                    record[field.header_name] = excel_interface.get_cell_value(
                        worksheet=ws,
                        row=row,
                        col=field.col_num,
                        norm_func=field.norm_func,
                    )
                result.append(record)
        return result

    def get_fields(self, path, sheetname):
        """Read the worksheet table with data grouped by field (i.e. columns).

        keys: field names
        values: list of cell values in that column

        Args:
            path (str or Path object): Path to workbook. Raise error if not found.
            sheetname (str): Worksheet name. Raise error if not found.

        Returns:
            dict: Headers as keys, list of data as values.
        """
        ws = excel_interface.get_worksheet_from_path(path, sheetname)
        with self._set_ws(ws):
            result = dict()
            for field in self._get_fieldsummaries():
                result[field.header_name] = excel_interface.get_column(
                    worksheet=ws,
                    col_num=field.col_num,
                    row_start=self._records_row_start,
                    row_end=ws.max_row,
                    norm_func=field.norm_func,
                )
            return result

    @property
    def header_row_num(self):
        """int: This is the row the TableReader will look for the header row.
            The next row is the first record.

        See the TableReader header_row_num parameter for add'l notes.
        """
        if isinstance(self._header_row_num, int):
            pass
        elif self.fields:
            self._header_row_num = headers.get_best_match_row_number(
                worksheet=self._ws,
                values=self.fields,
            )
        else:
            self._header_row_num = 1
        return self._header_row_num

    @header_row_num.setter
    def header_row_num(self, value):
        if value is None:
            self._header_row_num = value
        elif isinstance(value, int):
            if value >= 1:
                self._header_row_num = value
            else:
                raise ValueError("header row num must be greater than zero")
        else:
            raise TypeError("header row num must be None or int >= 1.")

    @property
    def _records_row_start(self):
        return self.header_row_num + 1

    @contextmanager
    def _set_ws(self, value):
        self._ws = value
        header_row_num = self._header_row_num
        yield
        self._ws = None
        self._header_row_num = header_row_num

    def _get_norm_func(self, field_name):
        def do_nothing(value):
            return value
        if self.fields and self.norm_funcs:
            index = self.fields.index(field_name)
            return self.norm_funcs[index]
        return do_nothing

    def _get_fieldsummaries(self):
        # This method handles the logic of which columns to include.
        # Returns lists of FieldSummary objects.
        field_summaries = list()

        header_names = excel_interface.get_worksheet_row(
            worksheet=self._ws,
            row=self.header_row_num,
        )

        for col_num, header_name in enumerate(header_names, 1):

            # Skip blank headers
            if header_name is None:
                continue

            # field name
            if not self.fields:
                field_name = header_name
            elif header_name in self.fields:
                field_name = header_name
            else:
                continue

            # normalizing function
            norm_func = self._get_norm_func(field_name)

            field_summaries.append(FieldSummary(
                header_name=header_name,
                col_num=col_num,
                field_name=field_name,
                norm_func=norm_func,
            ))

        return field_summaries
