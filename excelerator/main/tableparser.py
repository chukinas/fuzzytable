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
# This class for internal use. It stores information about each field to make data output simpler.

#  :obj: ``


class TableParser:
    """Parses excel data.

    Pulling data from an excel sheet is a 2-step process.
    First, instantiate a TableReader object. The arguments you supply define how the data will be parsed.
    Second, call one of the TableReader's *get* methods
    (e.g. :obj:`get_records()` or :obj:`get_fields()`) to output the data in the desired format.

    Args:
        worksheet (:obj:`str`, ``excelerator.WorksheetParser``, \
            :obj:`openpyxl.worksheet.worksheet.Worksheet`, or :obj:`list` thereof):
            * If :obj:`str`, parse the worksheet with this title.
            * If ``WorksheetParser``, similar to ``str``, but will additional options.
            * If :obj:`Worksheet`, parse this openpyxl worksheet object.
              Overrides ``path`` parameter.

            ``list`` may contain a combination of the above types. This will return multiple tables.
            Todo:
                Only :obj:`str` is currently implemented. Need to implement the rest.
        fields (:obj:`str`, ``excelerator.FieldParser`` or :obj:`sequence` thereof, default :obj:`None`)
            * If ``None``, generate fields for each non-``None`` cell found in ``header_row_num`` row.
            * If ``str``, TableParser looks for cell with this exact value and returns the data below it.
            * If ``FieldParser``, like ``str`` but with additional options.
              See :obj:`excelerator.FieldParser` for details.

            ``sequence`` may contain multiple types of the above.
            Todo:
                Only ``list`` of :obj:`str` is currently implemented. Need to implement the rest.
        header_row_num (:obj:`int`, default :obj:`None`):
            * If ``None`` (default), headers are assumed to be in row 1, with data starting on row 2.
            * If ``int``, this is where the header row is assumed to be.
        seek_header_row (:obj:`bool`, ``int``, default :obj:`False`):
            * If ``True``, override ``header_row_num``. If ``worksheet``,
              find the best match row in the first ``potential_header_rows`` rows.
              Otherwise, use the first non-None row.
            * If ``False``, headers row = ``header_row_num``.
        potential_header_rows (:obj:`int`, default :obj:`20`): If ``seek_header_row``,
            this is the number of rows that TableParser will look through
            to find the best match header_row_num.
        path (:obj:`str`, :obj:`pathlib.Path`, default :obj:`None`): Path to workbook.
        normalize (:obj:`list` of :obj:`excelerator.normalize.NormalizeBase`, default :obj:`None`):
            No effect if `fields` is `None`.
            If fields is supplied, then the normalize functions are applied to the corresponding field.
            Use normalization functions when you want to guarantee you get the data types you want.

    Other Parameters:
        approximate_match (`bool` / default `True`):
        detailed_output
        aliases (``list`` of ``str``, ``list`` of ``list`` of ``str``, default ``None``)
        aliases_only (``bool``, default ``False``): fdsafdsa

    Todo:
        Implement ``Other Parameters``.

    Raises:
        :obj:`excelerator.exceptions.ExceleratorError`: stuff
                if file not found or if file wrong type or
                if sheetname not found
        FileNotFound: if file not found

    Example:
        >>> from excelerator import TableParser
        >>> tr = TableParser(
                fields='first_name last_name'.split(),
            )
        >>> fields = tr.get_fields(path='path/to/excel.xlsx', sheetname='names')
    """

    def __init__(
            self,
            worksheet,
            path=None,
            fields=None,
            header_row_num=None,
            normalize=None,
            seek_header_row=False,
            potential_header_rows=20,
            approximate_match=False,
    ):
        self._ws = None
        self.fields = fields
        self.header_row_num = header_row_num
        self.norm_funcs = normalize
        self.sheetname = worksheet  # TODO rename to sheetnames
        self.path = path

    def get_records(self):
        """Group tabular data by record (i.e. rows).

        Returns:
            list: one item per record (row). Each record is represented as a dictionary of fieldname: cellvalue pairs.
        """
        with self._set_ws():
            field_summaries = self._get_fieldsummaries()
            result = list()
            for row in range(self._records_row_start, self._ws.max_row + 1):
                record = dict()
                for field in field_summaries:
                    record[field.header_name] = excel_interface.get_cell_value(
                        worksheet=self._ws,
                        row=row,
                        col=field.col_num,
                        normalize=field.norm_func,
                    )
                result.append(record)
        return result

    def get_fields(self):
        """Group tabular data by field (i.e. columns).

        keys: field names

        values: list of cell values in that column

        Returns:
            dict: Headers as keys, list of data as values.
        """
        with self._set_ws():
            result = dict()
            for field in self._get_fieldsummaries():
                result[field.header_name] = excel_interface.get_column(
                    worksheet=self._ws,
                    col_num=field.col_num,
                    row_start=self._records_row_start,
                    row_end=self._ws.max_row,
                    norm_func=field.norm_func,
                )
            return result

    @property
    def header_row_num(self):
        """int: This is the row the TableParser will look for the header row.
            The next row is the first record.

        See the TableParser header_row_num parameter for add'l notes.
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
    def _set_ws(self):
        self._ws = excel_interface.get_worksheet_from_path(self.path, self.sheetname)
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
