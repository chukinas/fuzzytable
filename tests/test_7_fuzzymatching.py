from fuzzytable import FuzzyTable
import pytest


@pytest.mark.parametrize("min_ratio,expected_fieldcount", [
    (None, 1),
    (0.3, 2),
])
# 1  #####
def test_7_1_approx_names(firstlastnames, min_ratio, expected_fieldcount):

    # GIVEN a table with headers 'first_name' and 'last_name'...
    path = firstlastnames.path

    # WHEN the user desires the following slightly different subfields...
    fields = ['first_name', 'given name', 'twas the night before christmas']

    # THEN the first name always matches; last name depends on the min_ratio
    ft = FuzzyTable(
        path=path,
        fields=fields,
        header_row_seek=True,
        name='names',
        approximate_match=True,
        min_ratio=min_ratio,
    )
    actual_field_count = len(ft.fields)
    assert actual_field_count == expected_fieldcount
