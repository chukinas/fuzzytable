from fuzzytable import FuzzyTable
import pytest
import collections
from fuzzytable import exceptions


@pytest.mark.parametrize('header_row', [
    None,
    20,
    100
])
###  1  ###
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

    # THEN all desired field_names are extracted.
    actual_output = dict(ft)
    expected_output = dr_who_fields
    assert actual_output == expected_output


###  2  ###
def test_seek_too_few_rows(test_path, dr_who_fields):

    # GIVEN table whose headers are NOT in row 1...
    path = test_path('csv')

    # WHEN user seeks table in too few rows...
    header_seek_rows = 2
    ft = FuzzyTable(
        path=path,
        fields=dr_who_fields.keys(),
        header_row_seek=header_seek_rows,
        name='Whoops!'
    )

    # THEN no field_names are extracted.
    assert len(ft) == 0

    # ALSO
    print(ft)


HeaderError = collections.namedtuple("HeaderError", "header_row, error_type")


@pytest.mark.parametrize('header_row', [
    'hello',
    -1,
    FuzzyTable,
    2.5,
])
###  3  ###
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


@pytest.mark.parametrize("field_names", ['hello'])
###  3  ###
def test_seek_single_field(test_path, field_names):

    # GIVEN a table whose headers are NOT in row 1...
    path = test_path('csv')

    # WHEN user seeks header row and supplies single field_names...
    FuzzyTable(
        path=path,
        header_row_seek=True,
        fields=field_names,
    )

    # THEN nothing breaks
    assert True
