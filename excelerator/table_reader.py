from excelerator import utils
from excelerator.worksheet_rows import get_worksheet_row


class TableReader:

    def __init__(self, header_row_num=None):
        self.header_row_num = header_row_num

    def read_from(self, path, sheetname):
        ws = utils.get_worksheet_from_path(path, sheetname)
        result = dict()
        headers = get_worksheet_row(
            worksheet=ws,
            row_int=self.header_row_num,
        )
        for col_num, header in enumerate(headers, 1):
            if header is not None:
                result[header] = utils.get_column(worksheet=ws,
                                                  col_num=col_num,
                                                  row_start=self.records_row_start,
                                                  row_end=ws.max_row)
        return result

    @property
    def header_row_num(self):
        return self._header_row_num

    @header_row_num.setter
    def header_row_num(self, value):
        if value is None:
            self._header_row_num = 1
        else:
            self._header_row_num = int(value)

    @property
    def records_row_start(self):
        return self.header_row_num + 1
