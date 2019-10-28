from excelerator import TableReader


def test_table_reader_simple():
    tr = TableReader()
    actual_output = tr.read_from()
    expected_output = {
        'first_name': 'Rose Amy River'.split(),
        'last_name': 'Tyler Pond Song'.split(),
        'last_appearance': [2013, 2013, 2015],
    }
    assert actual_output == expected_output
