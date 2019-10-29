import pytest
from excelerator import TableReader
from excelerator import exceptions


simple_table_expected_output = {
    'first_name': 'Rose Amy River'.split(),
    'last_name': 'Tyler Pond Song'.split(),
    'last_appearance': [2013, 2013, 2015],
}


@pytest.mark.parametrize('sheetname', 'table_top_left table_top_right'.split())
def test_table_simple_top(sheetname, fixture_path):
    """Test the most simple use case - default table interpretation"""
    tr = TableReader()
    actual_output = tr.read_from(path=fixture_path, sheetname=sheetname)
    assert actual_output == simple_table_expected_output


@pytest.mark.parametrize('sheetname', 'table_bottom_left table_bottom_right'.split())
def test_table_simple_top(sheetname, fixture_path):
    """Test another simple use case - default table interpretation + header_row_num"""
    tr = TableReader(header_row_num=4)
    actual_output = tr.read_from(path=fixture_path, sheetname=sheetname)
    assert actual_output == simple_table_expected_output


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

