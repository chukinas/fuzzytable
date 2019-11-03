from fuzzytable import exceptions
from fuzzytable.main.fuzzytable import FuzzyTable
import pytest
from tests import conftest



# --- errors during instantiation ---------------------------------------------


# @pytest.mark.parametrize('io', [
#     (None, None),
#     (-1, ValueError),
#     (0, ValueError),
#     (1,None),
#     (5,None),
#     ('a', TypeError),
#     (4.0, TypeError),
# ])
# def test_bad_row_num(io):
#     header_row_num, expected_error = io
#     try:
#         FuzzyTable(
#             header_row=header_row_num,
#             source="does not matter"
#         )
#         actual_error = None
#     except ValueError:
#         actual_error = ValueError
#     except TypeError:
#         actual_error = TypeError
#     assert actual_error == expected_error


# --- path and sheetname errors -----------------------------------------------
@pytest.mark.parametrize('path', [
    conftest.get_test_path('docx'),  # file of wrong type
    conftest.get_test_path('wrong'),  # non-existent file
    conftest.get_test_path().parent,  # dir (no file)
    0,
])
###  1  ###
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


###  2  ###
def test_excel_missing_worksheet(test_path):

    # GIVEN an Excel worksheet that doesn't contain the desired worksheet name...
    missing_ws_name = 'missing_ws'

    # WHEN user tries to read from this non-existent worksheet...
    try:
        FuzzyTable(
            path=test_path(),
            sheetname=missing_ws_name,
        )

    # THEN raise an error
    except exceptions.SheetnameError:
        assert True
    else:
        assert False


@pytest.mark.parametrize("header_row_seek", [
    True,
    20
])
@pytest.mark.parametrize("fields", [
    None,
    FuzzyTable,
    1
])
###  3  ###
def test_seek_but_no_fields(test_path, header_row_seek, fields):

    # GIVEN a table whose headers are NOT in row 1...
    path = test_path('csv')

    # WHEN user seeks header row without supplying needed or correct fields...
    try:
        FuzzyTable(
            path=path,
            header_row_seek=header_row_seek,
            fields=fields,
        )

    # THEN InvalidFieldError is raised.
    except (exceptions.InvalidFieldError):
        assert True
    else:
        assert False


###  4  ###
def test_error_from_invalid_headerseek(test_path):

    # GIVEN a valid path...
    path = test_path('csv')

    # WHEN instantiates fuzzytable with
    #   valid fields argument but
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
