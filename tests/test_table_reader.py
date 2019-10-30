import pytest
from excelerator import TableReader
from excelerator import exceptions
from  collections import namedtuple


# --- path and sheetname errors -----------------------------------------------

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


# --- read simple table -------------------------------------------------------

simple_table_expected_output = {
    'first_name': 'Rose Amy River'.split(),
    'last_name': 'Tyler Pond Song'.split(),
    'last_appearance': [2013, 2013, 2015],
}


WorksheetGiven = namedtuple('WorksheetGiven', 'sheetname header_row_num')
worksheetgivens = [
    WorksheetGiven('table_top_left', 1),
    WorksheetGiven('table_top_right', 1),
    WorksheetGiven('table_bottom_left', 4),
    WorksheetGiven('table_bottom_right', 4),
]


sheetnames_with_headers_in_first_row = [
    wsgiven.sheetname
    for wsgiven in worksheetgivens
    if wsgiven.header_row_num == 1
]
@pytest.mark.parametrize('sheetname', sheetnames_with_headers_in_first_row)
def test_table_simple_top(sheetname, fixture_path):
    """Test the most simple use case - default table interpretation"""
    tr = TableReader()
    actual_output = tr.read_from(path=fixture_path, sheetname=sheetname)
    assert actual_output == simple_table_expected_output


@pytest.mark.parametrize('worksheet_given', worksheetgivens)
def test_table_simple_top(worksheet_given: WorksheetGiven, fixture_path):
    """Test another simple use case - default table interpretation + header_row_num"""
    sheetname, header_row_num = worksheet_given
    tr = TableReader(header_row_num=header_row_num)
    actual_output = tr.read_from(path=fixture_path, sheetname=sheetname)
    assert actual_output == simple_table_expected_output


def without(d, key):
    new_d = d.copy()
    new_d.pop(key)
    return new_d


FieldsAndResult = namedtuple('FieldsAndResult', 'fields expected_result')
fields_and_results = [
    FieldsAndResult('first_name last_name last_appearance'.split(), simple_table_expected_output),
    FieldsAndResult('first_name last_name last_aperants'.split(),
                    without(simple_table_expected_output, 'last_appearance')),
    FieldsAndResult('first_name last_name'.split(),
                    without(simple_table_expected_output, 'last_appearance')),
]


@pytest.mark.parametrize('worksheet_given', worksheetgivens)
@pytest.mark.parametrize('fields_results', fields_and_results)
def test_table_simple_seek_header(worksheet_given: WorksheetGiven, fields_results: FieldsAndResult, fixture_path):

    # GIVEN a spreadsheet whose header row may/not start in cell 'A1'...
    sheetname, header_row_num = worksheet_given

    # WHEN a TableReader is instantiated with a sequence of fields
    fields = fields_results.fields
    tr = TableReader(fields = fields)

    # THEN the header row is found automatically and only those fields passed
    #   as arguments are returned.
    actual_output = tr.read_from(path=fixture_path, sheetname=sheetname)
    expected_output = fields_results.expected_result
    assert actual_output == expected_output
