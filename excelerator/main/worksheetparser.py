# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None

"""
:obj:``

            See Also:
                 :obj:`ws_all`, :obj:`ws_approx_match`, :obj:`ws_raise_error_if_missing`
"""

# Note: there is a to do warning in worksheetparser.rst

# TODO is there a better term than "Parser"? It's really the TableParser that's the only parser.
#   WS and Field are really a big set of options, attributes.


class WorksheetParser:
    """Optional argument for  :obj:`exclerator.TableParser` :obj:`worksheet` parameter.

    The default way of specifying the desired worksheet is to pass a :obj:`str` or :obj:`list` of :obj:`str`
    argument to the :obj:`exclerator.TableParser` :obj:`worksheet` parameter.
    If the worksheet(s) is/are not found, an exception is raised.
    If you need to alter this behavior, pass a :obj:`WorksheetParser` object instead.

    Args:
        sheetnames (:obj:`str`, :obj:`list` of :obj:`str`, :obj:`dict`, default :obj:`None`):
            * If :obj:`None`,
            * If :obj:`str`, then parse the worksheet with this title.
            * If :obj:`list`, then parse the worksheets with these titles.
            * If :obj:`dict`, each key/value pair stands for a single worksheet.
              The key is the expected name of the worksheet.
              The value is one or more aliases (i.e. alternate sheetnames) that will also be searched for.
        approx_match (:obj:`bool`, default :obj:`False`):
            * If :obj:`True`, for each sheetname (and it's aliases), find the best matching worksheet.
            * If :obj:`False` (default), only exact matches are returned.

            No effect if no :obj:`sheetnames` empty.
        all_worksheets (:obj:`bool`, default :obj:`False`): If :obj:`True`,
            ``sheetnames`` and ``approx_match`` are ignored.
            ``TableParser`` will return a table from each worksheet in the workbook.
        suppress_missing_ws_error (:obj:`bool`, default :obj:`False`): Normally,
            if a worksheet match cannot be found, an exception is raised. If :obj:`True`,
            no exception is raised. TableParser will return what tables it can.
        path (:obj:`str`, :obj:`pathlib.Path`, default :obj:`None`): Path to workbook.
            If given, overrides ``TableParser``'s ``path`` parameter.

    Note:
        A worksheet can only match with a single sheetname (and its aliases).
        WorksheetParser tries first to match on sheetnames, then by aliases, if given.
        Because order is important, if passing a dict to ``sheetnames``,
        use an ``ordereddict`` to set the relative priority of the sheetnames.
    """

    def __init__(
            self,
            sheetnames=None,
            approx_match=False,
            all_worksheets=False,
            suppress_missing_ws_error=False,
            path=None,
    ):
        self.all_worksheets = all_worksheets
        self.approx_match = approx_match
        self.suppress_excetions = suppress_missing_ws_error
        self.sheetname = sheetnames
        self.path = path
