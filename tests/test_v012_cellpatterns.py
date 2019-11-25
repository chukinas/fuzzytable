import pytest
from tests import v012_params as p
from fuzzytable import FuzzyTable, FieldPattern, exceptions, cellpatterns

@pytest.mark.parametrize('fields,expected_values,csv_or_excel', [
    pytest.param(p.def_fields, p.def_csv_expected_values, '.csv', id='default cellpatterns'),
    pytest.param(p.def_fields, p.def_excel_expected_values, '.xlsx', id='default cellpatterns'),
    pytest.param(p.int_fields, p.int_expected_values, '', id='integer'),
    pytest.param(p.str_fields, p.str_expected_values, '', id='string'),
    pytest.param(p.str_field_instantiated, p.str_expected_values, '.csv', id='string (instantiated)'),
    pytest.param(p.intlist_fields, p.intlist_expected_values, '', id='integerlist'),
    pytest.param(p.float_fields, p.float_expected_values, '', id='float'),
    pytest.param(p.wordlist_fields, p.wordlist_expected_values, '', id='wordlist'),
    pytest.param(p.bool_fields, p.bool_expected_values, '', id='boolean'),
    pytest.param(p.digit_fields, p.digit_expected_values, '', id='digit'),
    pytest.param(p.stringchoice_fields, p.stringchoice_expected_values, '', id='choice'),
    pytest.param(p.stringchoice_dict_fields, p.stringchoice_dict_expected_values, '', id='choice/dict'),
    pytest.param(p.stringchoice_dict_usekeys_fields, p.stringchoice_dict_expected_values, '', id='choice/dict/keys'),
])
@pytest.mark.parametrize('filename,kwargs', [
    pytest.param('data_pattern.csv', {}, id='csv'),
    pytest.param('test.xlsx', {'sheetname': 'data_pattern'}, id='excel'),
])
# 012/1 #####
def test_cellpatterns(test_files_dir, fields, expected_values, filename, kwargs, csv_or_excel):

    # evaluate csv- or excel-only tests:
    if csv_or_excel not in filename:
        pytest.skip(f"This is a {csv_or_excel}-only test")

    path = test_files_dir / filename
    ft = FuzzyTable(
        path=path,
        fields=fields,
        **kwargs,
    )
    actual_values = ft['values']
    # for value in values:
    #     if not isinstance(value, str):
    #         assert False
    assert actual_values == expected_values


@pytest.mark.parametrize('fieldpattern_kwargs,exception', [
    pytest.param({'name': 'doesnotmatter', 'cellpattern': 'This is not a cellpattern'},
                 exceptions.CellPatternError, id='CellPatternError'),
    pytest.param({'name': 'doesnotmatter', 'cellpattern': cellpatterns.StringChoice, },
                 exceptions.UninstantiatededCellPatternError, id='UninstantiatededCellPatternError'),
])
# 012/2 #####
def test_cellpatternerror(fieldpattern_kwargs, exception):
    with pytest.raises(exception):
        FieldPattern(**fieldpattern_kwargs)
