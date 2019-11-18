"""
Currently, the SheetPattern class only returns a SheetReader object to
FuzzyTable, which then passes it on to SheetParser.
Later releases will likely see this get added to the API, giving the user more
options for specifying what sheets and how to interact with.
"""

# --- Standard Library Imports ------------------------------------------------
from pathlib import Path

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable.main import sheetreader
from fuzzytable import exceptions

# --- Third Party Imports -----------------------------------------------------
# None

"""
:obj:``

            See Also:
                 :obj:`ws_all`, :obj:`ws_approx_match`, :obj:`ws_raise_error_if_missing`
"""


class SheetPattern:
    """Optional argument for  :obj:`exclerator.FuzzyTable` :obj:`worksheet` parameter.

    The default way of specifying the desired worksheet is to pass a :obj:`str` or :obj:`list` of :obj:`str`
    argument to the :obj:`exclerator.FuzzyTable` :obj:`worksheet` parameter.
    If the worksheet(s) is/are not matched, an exception is raised.
    If you need to alter this behavior, pass a :obj:`WorksheetParser` object instead.

    Args:
        sheetname (:obj:`str`, :obj:`list` of :obj:`str`, :obj:`dict`, default :obj:`None`):
            * If :obj:`None`,
            * If :obj:`str`, then parse the worksheet with this title.
            * If :obj:`list`, then parse the worksheets with these titles.
            * If :obj:`dict`, each key/ratio pair stands for a single worksheet.
              The key is the expected name of the worksheet.
              The ratio is one or more aliases (i.e. alternate sheetnames) that will also be searched for.
        approx_match (:obj:`bool`, default :obj:`False`):
            * If :obj:`True`, for each sheetname (and it's aliases), find the best matching worksheet.
            * If :obj:`False` (default), only exact matches are returned.

            No effect if no :obj:`sheetnames` empty.
        all_worksheets (:obj:`bool`, default :obj:`False`): If :obj:`True`,
            ``sheetnames`` and ``approx_match`` are ignored.
            ``FuzzyTable`` will return a table from each worksheet in the workbook.
        suppress_missing_ws_error (:obj:`bool`, default :obj:`False`): Normally,
            if a worksheet match cannot be matched, an exception is raised. If :obj:`True`,
            no exception is raised. FuzzyTable will return what tables it can.
        path (:obj:`str`, :obj:`pathlib.Path`, default :obj:`None`): Path to workbook.
            If given, overrides ``FuzzyTable``'s ``path`` parameter.

    Note:
        A worksheet can only match with a single sheetname (and its aliases).
        WorksheetParser tries first to match on sheetnames, then by aliases, if given.
        Because order is important, if passing a dict to ``sheetnames``,
        use an ``ordereddict`` to set the relative priority of the sheetnames.
    """

    def __init__(self, path, sheetname=None):

        # CSV
        try:
            path_object = Path(path)
        except TypeError:
            raise exceptions.InvalidFileError(path)
        if path_object.suffix == '.csv':
            self.sheet_reader = sheetreader.CsvReader(path_object)
            return

        # EXCEL
        self.sheet_reader = sheetreader.ExcelReader(path, sheetname)
        # Note: this will raise a custom exception if the openpyxl doesn't accept the path or sheetname
        # This is by design.

    # def __repr__(self):
    #     return get_repr(self)  # pragma: no cover


if __name__ == '__main__':
    pass