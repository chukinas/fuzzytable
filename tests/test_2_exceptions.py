from fuzzytable import exceptions
from fuzzytable.main.fuzzytable import FuzzyTable
import pytest
from tests import conftest


# --- path and sheetname errors -----------------------------------------------
@pytest.mark.parametrize('path', [
    conftest._get_test_path('docx'),  # file of wrong type
    conftest._get_test_path('wrong'),  # non-existent file
    conftest._get_test_path().parent,  # dir (no file)
    0,
])
# 1 #####
def test_invalidpaths(path):

    # GIVEN a file path with an invalid (i.e. not excel) extension...
    # (path parameter)

    # WHEN user try to read from that file path...
    try:
        FuzzyTable(path=path)

    # THEN raise an error
    except exceptions.InvalidFileError:
        assert True
    else:
        assert False


# 2  #####
def test_excel_missing_worksheet(get_test_path):

    # GIVEN an Excel worksheet that doesn't contain the desired worksheet name...
    missing_ws_name = 'missing_ws'

    # WHEN user tries to read from this non-existent worksheet...
    try:
        FuzzyTable(
            path=get_test_path(),
            sheetname=missing_ws_name,
        )

    # THEN raise an error
    except exceptions.SheetnameError:
        assert True
    else:
        assert False


# 3  #####
def test_error_from_invalid_headerseek(get_test_path):

    # GIVEN a valid path...
    path = get_test_path('csv')

    # WHEN instantiates fuzzytable with
    #   valid field_names argument but
    #   invalid header_seek argument...
    try:
        FuzzyTable(
            path=path,
            fields='hello bye'.split(),
            header_row_seek=[1, 2, 3],
        )

    # THEN InvalidSeekError is raised.
    except exceptions.InvalidSeekError:
        assert True
    else:
        assert False


@pytest.mark.parametrize("minratio", ['a string', -234, 1.1,])
@pytest.mark.parametrize("fieldnames", [None, 'first_name'])
# 4  #####
def test_invalid_min_ratio(fieldnames, minratio, firstlastnames):

    # GIVEN invalid min_ratio argument...
    min_ratio = minratio

    # WHEN fuzzytable is instantiated...
    # THEN an exception is raised.
    with pytest.raises(exceptions.InvalidRatioError):
        FuzzyTable(
            path=firstlastnames.path,
            fields=fieldnames,
            min_ratio=min_ratio,
        )
