# from fuzzytable import FuzzyTable
#
#
# def test_sheetreader_row_count(names_csv_path):
#
#     # GIVEN a sheet with more than 20 lines...
#     path = names_csv_path
#
#     # WHEN a table is extracted using headerseek of default 20...
#     ft = FuzzyTable(
#         path=path,
#         fields='first_name',
#         header_row_seek=True,
#     )
#
#     # THEN the sheetreader row_count property has to do a separate check for sheet length.
#     assert True
