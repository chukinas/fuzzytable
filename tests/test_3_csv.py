from fuzzytable import FuzzyTable
import pytest
import collections
from fuzzytable import exceptions
from fuzzytable import FieldPattern
from fuzzytable import datamodel




@pytest.mark.parametrize('kwargs,expected_fieldcount', [
    pytest.param({'header_row': 4, 'name': 'firstlastname'}, 2, id='header row correctly set'),
    pytest.param({'header_row_seek': 2}, 0, id='header row below search range'),
])
# 1  #####
def test_seek_too_few_rows(firstlastnames_startrow4, kwargs, expected_fieldcount):
    # WHEN user seeks table in too few rows...
    ft = FuzzyTable(
        path=firstlastnames_startrow4.path,
        fields=firstlastnames_startrow4.fields.keys(),
        **kwargs,
    )

    # THEN no field_names are extracted.
    actual_fieldcount = len(ft)
    assert actual_fieldcount == expected_fieldcount

    # ALSO
    print(ft)


HeaderError = collections.namedtuple("HeaderError", "header_row, error_type")


@pytest.mark.parametrize('header_row', [
    'hello',
    -1,
    FuzzyTable,
    2.5,
])
# 3  #####
def test_header_row_errors(get_test_path, dr_who_fields, header_row):
    header_error: HeaderError

    # GIVEN a table whose headers are NOT in row 1...
    path = get_test_path('csv')

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
    except exceptions.InvalidRowError:
        assert True
    else:
        assert False


@pytest.mark.parametrize("field_names", ['hello'])
# 4  #####
def test_seek_single_field(get_test_path, field_names):

    # GIVEN a table whose headers are NOT in row 1...
    path = get_test_path('csv')

    # WHEN user seeks header row and supplies single field_names...
    FuzzyTable(
        path=path,
        header_row_seek=True,
        fields=field_names,
    )

    # THEN nothing breaks
    assert True


# 5  #####
def test_user_generated_fieldpatterns(firstlastnames):

    # GIVEN a set of user-generated fieldpatterns...
    fields = [
        FieldPattern(
            name='something totally different',
            alias='first name',
            approximate_match=True,
        ),
        FieldPattern(
            name='last_name',
            alias=['last name', 'LastName'],
        )
    ]

    # WHEN they are passed to FuzzyTable...
    names = FuzzyTable(
        path=firstlastnames.path,
        fields=fields,
        header_row_seek=True,
        name='names',
    )

    # THEN the same two subfields are found.
    actual_field_count = len(names)
    expected_field_count = len(firstlastnames.fields)
    assert actual_field_count == expected_field_count


# 6  #####
def test3_6_compare_fieldnames(first_names):

    # GIVEN a table whose headers are NOT in row 1...
    kwargs = {
        'path': first_names.path,
        'header_row_seek': True,
        'fields': first_names.fieldnames,
    }

    # WHEN user seeks header row...
    ft = FuzzyTable(**kwargs)

    # THEN all desired field_names are extracted.
    actual_fieldnames = list(ft.keys())
    expected_fieldnames = first_names.fieldnames
    assert actual_fieldnames == expected_fieldnames


# 7  #####
def test3_7_multifield(first_names):

    # GIVEN a table containing three headers similar to 'name'...
    path = first_names.path

    # WHEN user extracts these columns into a single multifield...
    min_ratio = 0.3
    fields = [
        'id',
        FieldPattern('name', multifield=True, min_ratio=min_ratio),
    ]
    ft = FuzzyTable(
        path=path,
        approximate_match=True,
        fields=fields,
        header_row_seek=True,
    )

    # THEN both fields are extracted.
    actual_fieldnames = list(ft.keys())
    expected_fieldnames = 'id name'.split()
    assert actual_fieldnames == expected_fieldnames

    # THEN the 'name' field contains three subfields.
    # namefield = ft.get_field('name')
    name_field: datamodel.MultiField = ft.get_field('name')
    actual_name_count = len(name_field.subfields)
    expected_name_count = 3
    assert actual_name_count == expected_name_count

    # THEN the 'name' field's last column is 4:
    actual_namefield_finalcol = name_field.col_num_last
    expected_namefield_finalcol = 4
    assert actual_namefield_finalcol == expected_namefield_finalcol

    # THEN the 'name' multifield's data can be accessed as a dict:
    actual_firstrow_names = name_field[0]
    expected_firstrow_names = tuple('frank susan james'.split())
    assert actual_firstrow_names == expected_firstrow_names
    assert actual_firstrow_names == name_field.data[0]

    # THEN the 'id' singlefield's data can be accessed as a dict:
    id_field = ft.get_field('id')
    actual_firstrow_id = id_field[0]
    expected_firstrow_id = 0
    assert actual_firstrow_id == expected_firstrow_id

    # THEN the len of both fields are equal
    len_id = len(id_field)
    len_name = len(name_field)
    assert len_id == len_name == 3

    assert name_field.header == ('name 2', 'name 1', 'name 3')

    assert name_field.ratio >= min_ratio
