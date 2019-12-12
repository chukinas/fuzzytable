"""
These are string-matching functions for finding the best-fit header row.
"""

# --- Standard Library Imports ------------------------------------------------
from typing import List, Dict, Optional
from difflib import SequenceMatcher
from collections import namedtuple
from unittest.mock import sentinel  # https://www.revsys.com/tidbits/sentinel-values-python/

# --- Intra-Package Imports ---------------------------------------------------


# --- Third Party Imports -----------------------------------------------------
# None
from fuzzytable import exceptions

BestMatch = namedtuple("BestMatch", "index1 index2 string1 string2 ratio")
NoMatch = sentinel.NoMatch
NoMatch.ratio = 0.0
DefaultValue = sentinel.DefaultValue
BestKey = namedtuple('BestKey', 'name ratio')


def get_best_match(strings1: List[str], strings2: List[str], min_ratio=0.0, case_sensitive=True) -> BestMatch:
    if case_sensitive:
        return get_best_match_case_sensitive(strings1, strings2, min_ratio)
    else:
        best_match_lowercase = get_best_match_case_sensitive(
            strings1=[val.lower() for val in strings1],
            strings2=[val.lower() for val in strings2],
            min_ratio=min_ratio,
        )
        if best_match_lowercase is NoMatch:
            return NoMatch
        else:
            return BestMatch(
                index1=best_match_lowercase.index1,
                index2=best_match_lowercase.index2,
                string1=strings1[best_match_lowercase.index1],
                string2=strings2[best_match_lowercase.index2],
                ratio=best_match_lowercase.ratio,
            )


def get_best_match_case_sensitive(strings1: List[str], strings2: List[str], min_ratio=0.0) -> BestMatch:
    best_match = NoMatch
    for index1, string1 in enumerate(strings1):
        for index2, string2 in enumerate(strings2):
            if string1 == string2:
                return BestMatch(
                    index1=index1,
                    index2=index2,
                    string1=string1,
                    string2=string2,
                    ratio=1.0,
                )
            matcher = SequenceMatcher(None, string1, string2)
            if matcher.quick_ratio() < min_ratio:
                continue
            ratio = matcher.ratio()
            if ratio < min_ratio:
                continue
            elif ratio > best_match.ratio:
                best_match = BestMatch(
                    index1=index1,
                    index2=index2,
                    string1=string1,
                    string2=string2,
                    ratio=ratio,
                )
    return best_match


def get_best_ratio(strings1: List[str], strings2: List[str], min_ratio=0.0) -> float:
    return get_best_match(strings1, strings2, min_ratio).ratio


def _get_approxmatch(search_dict: Dict, target: str, min_ratio=0.0, case_sensitive=True):
    """
    Return dictionary key whose value (a list of strings) best fits the target value.

    Only the dictionary values are matched to the target string.
    """
    best_key = NoMatch
    best_ratio = 0.0
    for key, value in search_dict.items():
        ratio = get_best_match(
            strings1=value,
            strings2=[target],
            min_ratio=min_ratio,
            case_sensitive=case_sensitive,
        ).ratio
        if ratio > best_ratio:
            best_key = BestKey(key, ratio)
            best_ratio = ratio
    return best_key


def _exact_match(search_term, target):
    return search_term == target


def _contains_match(search_term, target):
    return search_term in target


_match_funcs = {
    'exact': _exact_match,
    'contains': _contains_match,
}


def _get_exactmatch_or_containsmatch(search_dict: Dict, target: str, mode: str, case_sensitive=True):
    """The exact-matching version of bestfit_dictkey"""
    match_func = _match_funcs[mode]
    if not case_sensitive:
        target = target.lower()
    for key, search_terms in search_dict.items():
        if not case_sensitive:
            search_terms = (string.lower() for string in search_terms)
        for search_term in search_terms:
            if match_func(search_term, target):
                bestkey = BestKey(key, 1.0)
                return bestkey
    return NoMatch


def get_bestkey(
        search_dict: Dict,
        target: str,
        mode: str,
        default_value,
        case_sensitive=True,
        min_ratio=0.0,
) -> BestKey:
    if mode in 'exact contains'.split():
        bestkey = _get_exactmatch_or_containsmatch(
            search_dict=search_dict,
            target=target,
            mode=mode,
            case_sensitive=case_sensitive,
        )
    else:  # i.e. mode == 'approx'.
        bestkey = _get_approxmatch(
            search_dict=search_dict,
            target=target,
            min_ratio=min_ratio,
            case_sensitive=case_sensitive,
        )

    if bestkey is NoMatch:
        return BestKey(default_value, 0.0)
    else:
        return bestkey


def mode_setter(mode, approx_match, contains_match):
    # API Change: replace this with setter
    if mode in "exact approx contains".split():
        return mode
    elif mode is not DefaultValue and mode is not None:
        raise exceptions.ModeError(mode)
    elif approx_match:
        return 'approx'
    elif contains_match:
        return 'contains'
    else:
        return DefaultValue

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
