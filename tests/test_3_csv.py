from fuzzytable import FuzzyTable
import pytest
import collections
from fuzzytable import exceptions


# --- header seek ----------------------------------------------------------1/5
@pytest.mark.parametrize('header_row', [
    None,
    20,
    100
])
def test_csv(test_path, dr_who_fields, header_row):

    # GIVEN a table whose headers are NOT in row 1...
    path = test_path('csv')

    # WHEN user seeks header row...
    fields = dr_who_fields.keys()
    ft = FuzzyTable(
        path=path,
        header_row_seek=True,
        fields=fields,
        header_row=header_row
    )

    # THEN all desired fields are extracted.
    actual_output = dict(ft)
    expected_output = dr_who_fields
    assert actual_output == expected_output


# --- header seek stop too early -------------------------------------------2/5
def test_seek_too_few_rows(test_path, dr_who_fields):

    # GIVEN table whose headers are NOT in row 1...
    path = test_path('csv')

    # WHEN user seeks table in too few rows...
    header_seek_rows = 2
    ft = FuzzyTable(
        path=path,
        fields=dr_who_fields.keys(),
        header_row_seek=header_seek_rows,
    )

    # THEN no fields are extracted.
    assert len(ft) == 0


# --- header_row errors ----------------------------------------------------3/5
HeaderError = collections.namedtuple("HeaderError", "header_row, error_type")


@pytest.mark.parametrize('header_row', [
    'hello',
    -1,
    FuzzyTable,
    2.5,
])
def test_header_row_errors(test_path, dr_who_fields, header_row):
    header_error: HeaderError

    # GIVEN a table whose headers are NOT in row 1...
    path = test_path('csv')

    # WHEN user gives an invalid header_row value,
    # regardless of the bool value of header_row_seek...
    fields = dr_who_fields.keys()
    try:
        FuzzyTable(
            path=path,
            fields=fields,
            header_row=header_row,
        )

    # THEN InvalidRowError is raised.
    except (exceptions.InvalidRowError):
        assert True
    else:
        assert False


# --- header seek + single field -------------------------------------------5/5
@pytest.mark.parametrize("fields", ['hello'])
def test_seek_single_field(test_path, fields):

    # GIVEN a table whose headers are NOT in row 1...
    path = test_path('csv')

    # WHEN user seeks header row and supplies single fields...
    FuzzyTable(
        path=path,
        header_row_seek=True,
        fields=fields,
    )

    # THEN nothing breaks
    assert True
