"""
SheetParser does the heavy lifting of finding the right header row
and matching each desired field (FieldPattern) to a column.
In the current release, only one SheetParser and one SheetReader is
instantiated per instantiation of FuzzyTable.
Later releases will likely see the option of searching multiple sheets for
the best-fit header row. Then, there will be one SheetParser per sheet.
"""

# --- Standard Library Imports ------------------------------------------------
from collections import namedtuple
from typing import List, Union

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable import exceptions
from fuzzytable import datamodel
from fuzzytable import patterns
from fuzzytable.main import sheetreader
from fuzzytable.main.string_analysis import row_ratio

# --- Third Party Imports -----------------------------------------------------
# None


RowRatio = namedtuple("RowRatio", "row_index ratio")
NEG_INFINITY = float("-inf")


class SheetParser:

    def __init__(
            self,
            sheet_reader: sheetreader.SheetReader,
            fieldpatterns: List[patterns.FieldPattern],
            header_row,
            header_row_seek
    ):

        # --- determine header row --------------------------------------------
        actual_header_row, header_row_ratio = header_row_and_ratio(
            given_header_row=header_row,
            header_row_seek=header_row_seek,
            fieldpatterns=fieldpatterns,
            sheet_reader=sheet_reader,
        )

        # --- collect sheet fields --------------------------------------------
        header_values = sheet_reader[actual_header_row]
        all_ws_fields = [
            datamodel.Field(header=header, col_num=col_num)
            for col_num, header in enumerate(header_values, 1)
            if header
        ]

        # --- find matches ----------------------------------------------------
        if fieldpatterns:
            # Use only those fields matching the desired fields
            for field_pattern in fieldpatterns:
                find_exact_match(field_pattern, all_ws_fields)
        # else:
        #     # Fields weren't speficied. Use all found fields
        #     for ws_field in all_ws_fields:
        #         ws_field.matched = True

        ############################
        #  Fuzzy Table Data Model  #
        ############################

        # --- fuzzy table data model: fields ----------------------------------
        if fieldpatterns:
            self.fields = list(filter(lambda f: f.matched, all_ws_fields))
        else:
            self.fields = all_ws_fields
        data_row_start = actual_header_row + 1
        for field in self.fields:
            data = sheet_reader.get_col(data_row_start, field.col_num)
            field.data = data

        # --- fuzzy table data madel: summary ---------------------------------
        self.sheet_summary = datamodel.Sheet(
            header_row_num=actual_header_row,
            row_count=sheet_reader.row_count,
            ratio=header_row_ratio,
            path=sheet_reader.path,
            sheetname=sheet_reader.sheetname,
        )

        # --- fuzzy table data model: records ---------------------------------
        self.records = datamodel.Records(
            fields=self.fields,
            header_row_num=actual_header_row,
            row_count=sheet_reader.row_count
        )

    # def __repr__(self):
    #     return get_repr(self)  # pragma: no cover


def pos_int(value):
    return bool(isinstance(value, int) and value > 0)


def header_row_and_ratio(
        given_header_row: int,  # The header row number passed to FuzzyTable
        header_row_seek: Union[bool, int],
        fieldpatterns: List[patterns.FieldPattern],
        sheet_reader: sheetreader.SheetReader,
) -> (int, float):

    # --- header row (no seek) --------------------------------------------
    if header_row_seek is False:
        if given_header_row is None:
            actual_header_row_num = 1
        elif pos_int(given_header_row):
            actual_header_row_num = given_header_row
        else:
            raise exceptions.InvalidRowError(given_header_row)
        header_row_str = sheet_reader.get_row_str(actual_header_row_num)
        header_row_ratio = row_ratio(fieldpatterns, header_row_str)
        return actual_header_row_num, header_row_ratio

    # --- header row seek -------------------------------------------------
    if not fieldpatterns:
        raise exceptions.InvalidFieldError(None)

    if header_row_seek is True:
        header_seek_final_row = 20
    elif pos_int(header_row_seek):
        header_seek_final_row = header_row_seek
    else:
        raise exceptions.InvalidSeekError(header_row_seek)

    best_row_num = None
    best_ratio = NEG_INFINITY
    for row_num, row_str in enumerate(sheet_reader.iter_row_str(end_row=header_seek_final_row), 1):
        ratio = row_ratio(fieldpatterns, row_str)
        if ratio > best_ratio:
            best_ratio = ratio
            best_row_num = row_num
    actual_header_row_num = best_row_num
    header_row_ratio = best_ratio
    return actual_header_row_num, header_row_ratio


def find_exact_match(field_pattern: patterns.FieldPattern, ws_fields: List[datamodel.Field]) -> None:
    # If this pattern hasn't already matched a match, find an exact match (if available)
    # If found, updates the state of both the field and the field pattern

    # 20191111: This isn't need yet. Will uncomment when implementing approximate matching.
    # if field_pattern.matched:
    #     return

    for ws_field in filter(lambda f: not f.matched, ws_fields):
        if field_pattern.name == ws_field.header:
            field_pattern.matched = True
            ws_field.matched = True
            ws_field.name = field_pattern.name
            return


if __name__ == "__main__":
    pass
