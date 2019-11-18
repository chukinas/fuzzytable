import pytest
from fuzzytable import exceptions, FuzzyTable
from fuzzytable.main.fuzzytable import FuzzyTable


# 010/1 #####
def test_fieldpatternerror():
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
def test_seek_but_no_fields(get_test_path, header_row_seek, fields):

    # GIVEN a table whose headers are NOT in row 1...
    path = get_test_path('csv')

    # WHEN user seeks header row without supplying needed or correct field_names...
    with pytest.raises(exceptions.InvalidFieldError):
        FuzzyTable(
            path=path,
            header_row_seek=header_row_seek,
            fields=fields,
        )
