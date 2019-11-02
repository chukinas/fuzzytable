from excelerator import exceptions
from excelerator.main.table_reader import TableReader
import pytest

# --- errors during instantiation ---------------------------------------------


@pytest.mark.parametrize('io', [
    (None, None),
    (-1, ValueError),
    (0, ValueError),
    (1,None),
    (5,None),
    ('a', TypeError),
    (4.0, TypeError),
])
def test_bad_row_num(io):
    value, expected_error = io
    try:
        TableReader(header_row_num=value)
        actual_error = None
    except ValueError:
        actual_error = ValueError
    except TypeError:
        actual_error = TypeError
    assert actual_error == expected_error


# --- path and sheetname errors -----------------------------------------------

def test_table_reader_invalid_extension(fixture_path):

    # GIVEN a file path with an invalid (i.e. not excel) extension...
    path_with_incorrect_extension = fixture_path.parent / 'not_excel.docx'

    # WHEN user try to read from that file path...
    tr = TableReader(
        path=path_with_incorrect_extension,
        sheetname='does not matter'
    )
    try:
        tr.get_fields()

    # THEN raise an error
    except exceptions.ExceleratorError:
        return  # i.e. PASS the test
    assert False


def test_table_reader_missing_worksheet(fixture_path):

    # GIVEN an Excel worksheet that doesn't contain the desired worksheet name...
    missing_ws_name = 'missing_ws'

    # WHEN user tries to read from this non-existent worksheet...
    tr = TableReader(
        path=fixture_path,
        sheetname=missing_ws_name,
    )
    try:
        tr.get_fields()

    # THEN raise an error
    except exceptions.ExceleratorError:
        return  # i.e. PASS the test
    assert False
