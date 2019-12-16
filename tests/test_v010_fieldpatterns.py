import pytest
from fuzzytable import exceptions, FuzzyTable, FieldPattern


# 010/1 #####
def test_10_1_fieldpatternerror():
    with pytest.raises(exceptions.InvalidFieldError):
        FuzzyTable(
            name='does not matter',
            path='also does not matter',
            fields=42,  # This raises and error since it's neither string nor FieldPattern
        )


@pytest.mark.parametrize("header_row_seek", [
    True,
    20
])
@pytest.mark.parametrize("fields", [
    None,
    FuzzyTable,
    1,
    [42],
])
#  010/2  #####
def test_10_2_seek_but_no_fields(get_test_path, header_row_seek, fields):

    # GIVEN a table whose headers are NOT in row 1...
    path = get_test_path('csv')

    # WHEN user seeks header row without supplying needed or correct field_names...
    with pytest.raises(exceptions.InvalidFieldError):
        FuzzyTable(
            path=path,
            header_row_seek=header_row_seek,
            fields=fields,
        )


@pytest.mark.parametrize('searchterms_excludename,expected_matchedheader', [
    pytest.param(False, 'first_name', id='include fieldname'),
    pytest.param(True, 'last_name', id='exclude fieldname'),
])
#  010/3  #####
def test_10_3_searchterms_excludename(searchterms_excludename, expected_matchedheader, firstlastnames):

    # GIVEN a table with headers 'first_name' and 'last_name'...
    path = firstlastnames.path

    # WHEN user seeks header row without supplying needed or correct field_names...
    field = FieldPattern(
        name='first_name',
        alias='last_name',
        searchterms_excludename=searchterms_excludename,
    )

    ft = FuzzyTable(
        path=path,
        fields=field,
    )

    actual_matchedheader = ft.fields[0].header

    assert actual_matchedheader == expected_matchedheader


def test_10_4_casesensitive(firstlastnames):

    # GIVEN a table with headers 'first_name' and 'last_name'...
    path = firstlastnames.path

    # WHEN doing exact, but case-insensitive header search...
    expected_fieldnames = 'FIRST_NAME LAST_NAME'.split()
    ft = FuzzyTable(
        path=path,
        fields=expected_fieldnames,
        case_sensitive=False,
    )

    # THEN those fields are successfully found
    actual_fieldnames = [
        field.name
        for field in ft.fields
    ]

    assert actual_fieldnames == expected_fieldnames
