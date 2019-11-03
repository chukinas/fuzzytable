import pytest
from tests.conftest import get_dr_who_records

###  1  ###
def test_second_record_equality(ft_dr_who_all_fields, dr_who_records):

    # GIVEN a sheet containing the following record...
    expected_second_record = dr_who_records[1]

    # WHEN user successfully extracts all fields from the sheet...
    ft = ft_dr_who_all_fields
    ft.records.include_row_num = False
    actual_second_record = ft.records[1]

    # THEN ft.records and the expected dictionary compare equal.
    assert actual_second_record == expected_second_record


@pytest.mark.parametrize("records_equal", [
    (get_dr_who_records(), True),
    (get_dr_who_records()[0:1], False),
    (list(range(3)), False),
])
@pytest.mark.parametrize("convert_to_dict_list", [
    True,
    False
])
###  2  ####
def test_records_equality(ft_dr_who_all_fields, records_equal, convert_to_dict_list):

    # GIVEN a sheet containing the following table...
    expected_records, compare_equal = records_equal

    # WHEN user successfully extracts all fields from the sheet...
    ft = ft_dr_who_all_fields
    ft.records.include_row_num = False
    # ft.records.include_row_num = False
    actual_records = ft.records
    if convert_to_dict_list:
        actual_records = [
            dict(record)
            for record in actual_records
        ]

    # THEN ft.records and the expected dictionary compare equal.
    if compare_equal:
        assert actual_records == expected_records
    else:
        assert actual_records != expected_records


###  3  ###
def test_fields_dict_equality(ft_dr_who_all_fields, dr_who_fields):

    # GIVEN a sheet containing the following table...
    expected_dict = dr_who_fields
    ft = ft_dr_who_all_fields
    ft.records.include_row_num = False

    # WHEN user casts fuzzy table to dict...
    actual_dict = dict(ft)

    # THEN ft.records and the expected dictionary compare equal.
    assert actual_dict == expected_dict
    # assert list(ft.items()) == dr_who_fields.items()


    # OTHER
    for field in ft.fields:
        str(field)
    print(ft.records.include_row_num)


###  4  ###
def test_records_rows(ft_dr_who_all_fields, dr_who_fields):

    # GIVEN a table with headers in row 4...
    expected_rows = list(range(5, 8))

    # WHEN user accesses records via get_records:
    ft = ft_dr_who_all_fields
    actual_rows = [
        record['row']
        for record in ft.records
    ]

    # THEN the records have the correct row numbers
    assert actual_rows == expected_rows


###  5  ###
def test_records_missing_field(ft_dr_who_some_fields, dr_who_records):

    # GIVEN a sheet containing the following table...
    expected_records = dr_who_records

    # WHEN user extracts only some fields...
    ft = ft_dr_who_some_fields
    actual_records = ft.records

    # THEN ft.records and the expected dictionary compare equal.
    assert actual_records != expected_records
    assert actual_records != [{'a': 1, 'b': 2}]*3


###  6  ###
def test_fuzzytable_keysvaluesitems(ft_dr_who_all_fields, dr_who_fields):

    # GIVEN a table...
    expected_fields = dr_who_fields

    # WHEN user extracts the table with fuzzy table...
    # expected_rows = list(range(5, 8))
    ft = ft_dr_who_all_fields

    # THEN the fuzzy table behaves list a dictionary
    assert list(ft.keys()) == list(expected_fields.keys())
    assert list(ft.values()) == list(expected_fields.values())
    for (ft_keys, ft_values), (exp_keys, exp_values) in zip(ft.items(), expected_fields.items()):
        assert ft_keys == exp_keys
        assert ft_values == exp_values


###  7  ###
def test_fuzzyrecords_len(ft_dr_who_all_fields, dr_who_records):

    # GIVEN a table...
    expected_records = dr_who_records
    expected_record_count = len(expected_records)

    # WHEN user inspects records length
    ft = ft_dr_who_all_fields
    actual_record_count = len(ft.records)

    # THEN the fuzzy table behaves list a dictionary
    assert actual_record_count == expected_record_count
