"""
SheetParser does the heavy lifting of finding the right header row
and matching each desired field (FieldPattern) to a column.
In the current release, only one SheetParser and one SheetReader is
instantiated per instantiation of FuzzyTable.
Later releases will likely see the option of searching multiple sheets for
the best-fit header row. Then, there will be one SheetParser per sheet.
"""

# --- Standard Library Imports ------------------------------------------------
from collections import namedtuple, defaultdict
from typing import List, Union

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable import exceptions
from fuzzytable import datamodel
from fuzzytable import patterns
from fuzzytable.main import sheetreader
from fuzzytable.parsers.fieldparser import FieldParser
from fuzzytable.datamodel import MultiField, Field, SingleField

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

        # --- collect sheet field_names --------------------------------------------
        header_values = sheet_reader[actual_header_row]
        all_ws_fields = [
            datamodel.SingleField(header=header, col_num=col_num)
            for col_num, header in enumerate(header_values, 1)
            if header
        ]

        # --- find matches ----------------------------------------------------
        fieldparsers = [FieldParser(fieldpattern, all_ws_fields) for fieldpattern in fieldpatterns]
        while True:
            available_fieldparsers = list(filter(lambda fp: fp.still_seeking, fieldparsers))
            try:
                bestfit_fieldparser = max(available_fieldparsers, key=lambda fp: fp.bestfit_ratio)
            except ValueError:
                # No more available fieldparsers.
                break
            bestfit_fieldparser.assign_bestfit_field()

        # --- fuzzy table data model: field_names ----------------------------------
        if fieldpatterns:
            fields_matched = list(filter(lambda f: f.matched, all_ws_fields))
        else:
            fields_matched = all_ws_fields

        fields_dict = defaultdict(list)
        for field in fields_matched:
            fieldname = field.name
            fields_dict[fieldname].append(field)

        multifield_names = [
            fieldpattern.name
            for fieldpattern in fieldpatterns
            if fieldpattern.multifield
        ]

        single_fields = [
            fieldlist[0]
            for fieldname, fieldlist in fields_dict.items()
            if fieldname not in multifield_names
        ]

        multi_fields = [
            MultiField(fieldname, fieldlist)
            for fieldname, fieldlist in fields_dict.items()
            if fieldname in multifield_names
        ]

        fields = single_fields + multi_fields
        for field in fields:
            assign_data_to_field(field, sheet_reader, actual_header_row)
        self.fields = sorted(fields, key=lambda f: f.col_num)

        ############################
        #  Fuzzy Table Data Model  #
        ############################

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
    """Given the FuzzyTable arguments, return the actual header row (and match ratio)."""

    # --- header row (no seek) --------------------------------------------
    if header_row_seek is False:
        if given_header_row is None:
            actual_header_row_num = 1
        elif pos_int(given_header_row):
            actual_header_row_num = given_header_row
        else:
            raise exceptions.InvalidRowError(given_header_row)
        header_row_str = sheet_reader.get_row_str(actual_header_row_num)
        header_row_ratio = FieldParser.row_ratio(fieldpatterns, header_row_str)
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
        ratio = FieldParser.row_ratio(fieldpatterns, row_str)
        if ratio > best_ratio:
            best_ratio = ratio
            best_row_num = row_num
    actual_header_row_num = best_row_num
    header_row_ratio = best_ratio
    return actual_header_row_num, header_row_ratio


def assign_data_to_field(field, sheet_reader, header_row_num):

    field: MultiField
    if isinstance(field, MultiField):
        for subfield in field.subfields:
            assign_data_to_field(subfield, sheet_reader, header_row_num)
        return

    field: SingleField
    sheet_reader: sheetreader.SheetReader
    # fieldparsers: List[FieldParser]
    # fielparser = fieldparsers.ind
    data_row_start = header_row_num + 1
    data = sheet_reader.get_col(
        start_row=data_row_start,
        col_num=field.col_num,
        cellpatterns=field.cellpattern,
    )
    field.data = data


if __name__ == "__main__":
    pass
