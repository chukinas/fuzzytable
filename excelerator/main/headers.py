"""These functions mainly help with finding a worksheet's header row."""

# --- Standard Library Imports ------------------------------------------------
from difflib import SequenceMatcher
import statistics

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from excelerator.main import utils


# --- HEADERS -----------------------------------------------------------------

def get_best_match_row_number(worksheet, values, max_row=20):
    """Find the row that best matches a set of values.
    :param worksheet: openpyxl Worksheet object
    :param values: collection of row values you expect to find.
    :param max_row: function searches rows from 1 to max_row
    :return: row number (1-indexed) that best matches the provided values
    """
    last_row = min(max_row, worksheet.max_row)
    rows = [utils.get_worksheet_row(worksheet, row) for row in range(1, last_row + 1)]
    best_index = find_most_similar_string_sequence(values, rows)
    return best_index + 1


# --- STRING ANALYSIS ---------------------------------------------------------

def best_similarity_ratio(value: str, strings: list):  #, return_ratio=False):
    """Return the best match to a given string."""
    string = str(value)
    # if len(strings) == 0:
    #     if return_ratio:
    #         return 0
    #     else:
    #         return None
    ratios = [
        SequenceMatcher(None, string, str(orig_string)).ratio()
        for orig_string in strings
    ]
    max_ratio = max(ratios)
    # if return_ratio:
    #     return max_ratio
    # else:
    #     index = ratios.index(max_ratio)
    #     return strings[index]
    return max_ratio


# def map_one_string_to_another(expected_strings: set, actual_strings: set):
#     """
#     Maps field names to their exact or best matches in pandas dataframe.
#     :param expected_strings: strings for whom we seek the best match
#     :param actual_strings: available strings
#     :return: dict[expected_string] = actual_string
#     """
#
#     # --- Setup ---------------------------------------------------------------
#     result = {}
#
#     # --- Get exact matches ---------------------------------------------------
#     for string in expected_strings & actual_strings:
#         result[string] = string
#     remaining_expected = list(expected_strings - actual_strings)
#     remaining_actual = list(actual_strings - expected_strings)
#
#     # --- Order expected strings by best match --------------------------------
#     def sort_by_match_ratio_then_alphbetical(input_string):
#         ratio = find_most_similar_string(
#             value=input_string,
#             strings=list(remaining_expected),
#             return_ratio=True,
#         )
#         return ratio, input_string
#     remaining_expected.sort(key=sort_by_match_ratio_then_alphbetical)
#
#     # --- Find best match for each remaining string ---------------------------
#     for string in remaining_expected:
#         best_actual = find_most_similar_string(string, remaining_actual)
#         result[string] = best_actual
#         if best_actual is not None:
#             remaining_actual.remove(best_actual)
#
#     # --- Return result -------------------------------------------------------
#     return result


def similarity_between_two_strings(input_strings, output_strings):
    match_ratios = [best_similarity_ratio(string, output_strings) for string in input_strings]
    return statistics.mean(match_ratios)


def find_most_similar_string_sequence(expected_string_sequence, list_of_actual_string_sequences):
    similarity_ratios = [
        similarity_between_two_strings(expected_string_sequence, actual_sequence)
        for actual_sequence in list_of_actual_string_sequences
    ]
    best_ratio = max(similarity_ratios)
    best_index = similarity_ratios.index(best_ratio)
    return best_index


if __name__ == '__main__':
    pass
