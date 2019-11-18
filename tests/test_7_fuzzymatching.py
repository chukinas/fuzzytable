from fuzzytable import FuzzyTable
import pytest


@pytest.mark.parametrize("minratio,fieldcount", [
    (None, 1),
    (0.3, 2),
])
# 1  #####
def test_approx_names(firstlastnames, minratio, fieldcount):

    # GIVEN a table with headers 'first_name' and 'last_name'...
    path = firstlastnames.path
    min_ratio, expected_field_count = (minratio, fieldcount)

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
    assert actual_field_count == expected_field_count
