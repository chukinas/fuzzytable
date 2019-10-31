from excelerator import TableReader


def test_get_records(fixture_path, expected_records):

    # GIVEN tabular data whose headers are *some*where in the first 20 rows...
    sheetname = 'table_top_right'

    # WHEN user default-reads worksheet and gets records...
    tr = TableReader()
    actual_output = tr.get_records(
        path=fixture_path,
        sheetname=sheetname
    )

    # THEN all fields with unique, non-None headers get outputted as list of dicts.
    expected_output = expected_records
    assert actual_output == expected_output
