import pytest
from excelerator import TableReader
from excelerator import exceptions


@pytest.mark.parametrize('sheetname', 'simple_table_left simple_table_right'.split())
def test_table_reader_simple(sheetname, fixture_path):
    tr = TableReader()
    actual_output = tr.read_from(path=fixture_path, sheetname=sheetname)
    expected_output = {
        'first_name': 'Rose Amy River'.split(),
        'last_name': 'Tyler Pond Song'.split(),
        'last_appearance': [2013, 2013, 2015],
    }
    assert actual_output == expected_output


def test_table_reader_invalid_extension(fixture_path):
    path_with_incorrect_extension = fixture_path.parent / 'not_excel.docx'
    tr = TableReader()
    try:
        tr.read_from(path=path_with_incorrect_extension, sheetname='does not matter')
    except exceptions.EXCELeratorError:
        return
    assert False


def test_table_reader_missing_worksheet(fixture_path):
    missing_ws_name = 'missing_ws'
    tr = TableReader()
    try:
        tr.read_from(path=fixture_path, sheetname=missing_ws_name,)
    except exceptions.EXCELeratorError:
        return
    assert False

