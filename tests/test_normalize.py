import collections
import pytest
from excelerator import TableParser
from excelerator import normalize as n

normalize_params = list()

NormalizeParam = collections.namedtuple("NormalizeParam", "norm_func expected_output")


normalize_params.append(NormalizeParam(norm_func=n.INTEGER(), expected_output=[
    0,
    2,
    5,
    6,
    457,
    525,
    663,
    663,
    2019,
    None,
    None,
    1,
    1,
    123,
    19,
    20,
    20,
    30,
    4,
    None,
    30,
    None,
    0,  # bool False
    1,
    None,  # blank space
]))


# TODO docs - dates, bools, None convert to ''
normalize_params.append(NormalizeParam(norm_func=n.STRING(), expected_output=[
    '0',
    '2',
    '5',
    '6',
    '457',
    '525.4',
    '663.5',
    '663.6',
    '',
    'two spaces left',
    'two spaces right',
    '1',
    '1, 2, 3',
    '123 456 78hi',
    '19twenty3',
    '20 8',
    '20 manager',
    '30 manager',
    '4',
    'hello, good bye',
    'helper 30',
    'stringLettersOnly',
    '',  # bool False
    '',
    '',  # blank space
]))

normalize_params.append(NormalizeParam(norm_func=n.INTEGER_LIST(), expected_output=[
    [0],
    [2],
    [5],
    [6],
    [457],
    [525],
    [663],
    [663],
    [2019, 10, 18, 0, 0, 0],  # datetime
    [],
    [],
    [1],
    [1, 2, 3],
    [123, 456, 78],
    [19, 3],
    [20, 8],
    [20],
    [30],
    [4],  # '4
    [],
    [30],
    [],
    [0],  # bool False
    [1],
    [],  # blank space
]))

# TODO append more test cases (e.g. STRING_LIST)


@pytest.mark.parametrize('normalize_param', normalize_params)
def test_normalize(fixture_path, normalize_param: NormalizeParam):

    # GIVEN a field with a variety of data types...
    sheetname = 'normalize'
    header = 'values'

    # WHEN an EXCELerator normalize function is applied to the field...
    tr = TableParser(
        fields=[header],  # TODO make sure header_row_num overrides fields list
        normalize=[normalize_param.norm_func],  # TODO make sure this also works as a single norm func
        path=fixture_path,
        worksheet=sheetname,
    )

    # THEN
    actual_output = tr.get_fields()
    expected_output = {header: normalize_param.expected_output}
    assert actual_output == expected_output
