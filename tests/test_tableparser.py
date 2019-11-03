import pytest
from excelerator import TableParser
from collections import namedtuple


# --- read simple table -------------------------------------------------------

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
def test_table_simple_top(sheetname, fixture_path, expected_fields):

    # GIVEN tabular data whose headers are in row 1...

    # WHEN user reads worksheet with *all* defaults...
    tr = TableParser(
        path=fixture_path,
        worksheet=sheetname,
    )

    # THEN all fields with unique, non-None headers get outputted.
    actual_output = tr.get_fields()
    expected_output = expected_fields
    assert actual_output == expected_output


@pytest.mark.parametrize('worksheet_given', worksheetgivens)
def test_table_simple_top(worksheet_given: WorksheetGiven, fixture_path, expected_fields):

    # GIVEN a worksheet with header in a *known* row...
    sheetname, header_row_num = worksheet_given

    # WHEN user sets *just* the header row...
    tr = TableParser(
        header_row_num=header_row_num,
        path=fixture_path,
        worksheet=sheetname,
    )

    # THEN all fields with unique, non-None headers get outputted.
    actual_output = tr.get_fields()
    expected_output = expected_fields
    assert actual_output == expected_output


def filtered_dict(orig_dict, keys):
    return {key: orig_dict[key] for key in keys}


FieldsAndResult = namedtuple('FieldsAndResult', 'fields expected_field_names')
fields_and_results = [
    FieldsAndResult('first_name last_name last_appearance'.split(),
                    'first_name last_name last_appearance'.split()),
    FieldsAndResult('first_name last_name last_aperants'.split(),
                    'first_name last_name'.split()),
    FieldsAndResult('first_name last_name'.split(),
                    'first_name last_name'.split()),
]


@pytest.mark.parametrize('worksheet_given', worksheetgivens)
@pytest.mark.parametrize('desired_and_actual_fieldnames', fields_and_results)
def test_table_simple_seek_header(
        worksheet_given: WorksheetGiven,
        desired_and_actual_fieldnames: FieldsAndResult,
        fixture_path,
        expected_fields,
):

    # GIVEN a spreadsheet whose header row may/not start in cell 'A1'...
    sheetname, header_row_num = worksheet_given

    # WHEN a user desires a specific set of fields...
    fields = desired_and_actual_fieldnames.fields
    tr = TableParser(
        fields=fields,
        path=fixture_path,
        worksheet=sheetname,
    )

    # THEN the header row is found automatically and only those fields passed
    #   as arguments are returned.
    actual_output = tr.get_fields()
    expected_output = filtered_dict(expected_fields, desired_and_actual_fieldnames.expected_field_names)
    assert actual_output == expected_output
