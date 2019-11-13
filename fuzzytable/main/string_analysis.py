"""
These are string-matching functions for finding the best-fit header row.
"""

# --- Standard Library Imports ------------------------------------------------

# --- Intra-Package Imports ---------------------------------------------------


# --- Third Party Imports -----------------------------------------------------
# None


# try:
#     from fuzzywuzzy import fuzz
#     usefuzzwuzzy = True
# except ImportError:
#     usefuzzwuzzy = False
# from difflib import SequenceMatcher


#
# SequenceMatcher()
# if sought is None:
#     return None
# # with warnings.catch_warnings():
# #     # I don't want the user seeing a message about Levenshtein
# #     # https://stackoverflow.com/questions/14463277/how-to-disable-python-warnings
# #     warnings.simplefilter("ignore")
# return fuzz.token_set_ratio(sought, str2)


#
# # --- STRING ANALYSIS ---------------------------------------------------------
#
# def best_similarity_ratio(value: str, strings: list):  #, return_ratio=False):
#     """Return the best match to a given string."""
#     string = str(value)
#     # if len(strings) == 0:
#     #     if return_ratio:
#     #         return 0
#     #     else:
#     #         return None
#     ratios = [
#         SequenceMatcher(None, string, str(orig_string)).ratio()
#         for orig_string in strings
#     ]
#     max_ratio = max(ratios)
#     # if return_ratio:
#     #     return max_ratio
#     # else:
#     #     index = ratios.index(max_ratio)
#     #     return strings[index]
#     return max_ratio
#
#
# # def map_one_string_to_another(expected_strings: set, actual_strings: set):
# #     """
# #     Maps field names_generator to their exact or best matches in pandas dataframe.
# #     :param expected_strings: strings for whom we seek the best match
# #     :param actual_strings: available strings
# #     :return: dict[expected_string] = actual_string
# #     """
# #
# #     # --- Setup ---------------------------------------------------------------
# #     result = {}
# #
# #     # --- Get exact matches ---------------------------------------------------
# #     for string in expected_strings & actual_strings:
# #         result[string] = string
# #     remaining_expected = list(expected_strings - actual_strings)
# #     remaining_actual = list(actual_strings - expected_strings)
# #
# #     # --- Order expected strings by best match --------------------------------
# #     def sort_by_match_ratio_then_alphbetical(input_string):
# #         ratio = find_most_similar_string(
# #             ratio=input_string,
# #             strings=list(remaining_expected),
# #             return_ratio=True,
# #         )
# #         return ratio, input_string
# #     remaining_expected.sort(key=sort_by_match_ratio_then_alphbetical)
# #
# #     # --- Find best match for each remaining string ---------------------------
# #     for string in remaining_expected:
# #         best_actual = find_most_similar_string(string, remaining_actual)
# #         result[string] = best_actual
# #         if best_actual is not None:
# #             remaining_actual.remove(best_actual)
# #
# #     # --- Return result -------------------------------------------------------
# #     return result

if __name__ == "__main__":
    pass
