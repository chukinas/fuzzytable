from excelerator import utils
from excelerator.worksheet_rows import get_worksheet_row


class TableReader:

    @staticmethod
    def read_from(path, sheetname):
        ws = utils.get_worksheet_from_path(path, sheetname)
        result = dict()
        headers = get_worksheet_row(
            worksheet=ws,
            row_int=1,
        )
        for col_num, header in enumerate(headers, 1):
            if header is not None:
                result[header] = utils.get_column(ws, col_num, 2, ws.max_row)
        return result
