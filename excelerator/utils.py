""""""
# TODO Fill in docstring

# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import openpyxl
from openpyxl.utils.exceptions import InvalidFileException

# --- Intra-Package Imports ---------------------------------------------------
from excelerator import exceptions


def get_workbook(path):
    try:
        return openpyxl.load_workbook(path, data_only=True)
    except (FileNotFoundError, InvalidFileException):
        raise exceptions.EXCELeratorError(f"\nError: '{path} ' is not a valid excel path.")


def get_worksheet_from_workbook(workbook, worksheet_name):
    try:
        return workbook[worksheet_name]
    except KeyError:
        raise exceptions.EXCELeratorError(f"\nError: Workbook does not contain a '{worksheet_name}' worksheet")


def get_worksheet_from_path(path, sheetname):
    workbook = get_workbook(path)
    return get_worksheet_from_workbook(workbook, sheetname)


def get_column(worksheet, col_num, row_start, row_end):
    return [
        worksheet.cell(row, col_num).value
        for row in range(row_start, row_end + 1)
    ]
