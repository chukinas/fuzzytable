import pytest
from fuzzytable import FuzzyTable
from collections import namedtuple


# --- inputs ------------------------------------------------------------------

# simple 4x3 table located in different corners of the worksheet
WorksheetGiven = namedtuple('WorksheetGiven', 'sheetname header_row_num')
worksheetgivens = [
    WorksheetGiven('table_top_left', 1),
    WorksheetGiven('table_top_right', 1),
    WorksheetGiven('table_bottom_left', 4),
    WorksheetGiven('table_bottom_right', 4),
]

# The same tables, but only those in the first row
sheetnames_with_headers_in_first_row = [
    wsgiven.sheetname
    for wsgiven in worksheetgivens
    if wsgiven.header_row_num == 1
]


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

###  1  ###
@pytest.mark.parametrize('sheetname', sheetnames_with_headers_in_first_row)
def test_excel_simple(sheetname, test_path, dr_who_fields):

    # GIVEN tabular data whose headers are in row 1...
    path = test_path()

    # WHEN user reads worksheet with *all* defaults...
    ft = FuzzyTable(
        path=path,
        sheetname=sheetname,
    )

    # THEN all fields with unique, non-None headers get outputted.
    ft_dict = dict(ft)
    actual_output = dict(ft)
    expected_output = dr_who_fields
    assert actual_output == expected_output


@pytest.mark.parametrize('worksheet_given', worksheetgivens)
###  2  ###
def test_excel_given_row(worksheet_given: WorksheetGiven, test_path, dr_who_fields):

    # GIVEN a worksheet with header in a *known* row...
    sheetname, header_row_num = worksheet_given

    # WHEN user sets *just* the header row...
    tr = FuzzyTable(
        path=test_path(),
        sheetname=sheetname,
        header_row=header_row_num,
    )

    # THEN all fields with unique, non-None headers get outputted.
    actual_output = dict(tr)
    expected_output = dr_who_fields
    assert actual_output == expected_output


@pytest.mark.parametrize('worksheet_given', worksheetgivens)
@pytest.mark.parametrize('desired_and_actual_fieldnames', fields_and_results)
###  3  ###
def test_table_simple_seek_header(
        worksheet_given: WorksheetGiven,
        desired_and_actual_fieldnames: FieldsAndResult,
        test_path,
        dr_who_fields,
):

    # GIVEN a spreadsheet whose header row may/not start in cell 'A1'...
    sheetname, header_row_num = worksheet_given

    # WHEN a user desires a specific set of fields...
    fields = desired_and_actual_fieldnames.fields
    ft = FuzzyTable(
        path=test_path(),
        sheetname=sheetname,
        fields=fields,
        header_row_seek=True,
    )

    # THEN the header row is matched automatically and only those fields passed
    #   as arguments are returned.
    actual_output = dict(ft)
    expected_output = filtered_dict(dr_who_fields, desired_and_actual_fieldnames.expected_field_names)
    assert actual_output == expected_output
