"""FieldParser objects do the hard work of figuring out a FieldPattern's best-fit SingleField."""

# --- Standard Library Imports ------------------------------------------------
from typing import List, Optional, Union
import collections
from unittest.mock import sentinel

# --- Intra-Package Imports ---------------------------------------------------
from fuzzytable.patterns import FieldPattern
from fuzzytable.datamodel import SingleField, MultiField
from fuzzytable.main.utils import get_repr
from fuzzytable.main import string_analysis as strings

# --- Third Party Imports -----------------------------------------------------
# None


# The parser looks once at each field only once.
# It stores the field and it's match ratio here for later reference.
PotentialField = collections.namedtuple("FieldRatio", "field ratio")
NullField = sentinel.NullField
NoMoreFields = PotentialField(field=None, ratio=0.0)


class FieldParser:

    def __init__(self, fieldpattern, fields):

        self.fieldpattern = fieldpattern
        self.matched = False

        field_rankings = []
        for field in reversed(fields):
            # Reversed b/c best matches are pulled off the end.
            # All else being equal, an earlier column is a better match than later column.
            ratio = self._calc_ratio(field)
            if ratio == 0:
                continue  # skip this field; not a good match (ratio likely too low)
            field_ratio = PotentialField(field, ratio)
            field_rankings.append(field_ratio)
        self.field_ratios = sorted(field_rankings, key=lambda fr: fr.ratio)  # ascending
        # Note: all subfields in this list are potential good matches.

    @property
    def bestfit_ratio(self) -> float:
        """Return match ratio with the best-fitting of the remaining subfields."""
        bestfit_fieldratio = self.get_best_fieldratio()
        return 0.0 if bestfit_fieldratio is None else bestfit_fieldratio.ratio

    def get_best_fieldratio(self) -> Optional[PotentialField]:
        # Of all the remaining unmatched Fields, return the best-fit field/ratio tuple

        # Ratio is zero if there are no more subfields available
        try:
            bestfit_fieldratio = self.field_ratios[-1]
        except IndexError:
            return None

        # If the best-match field is already taken,
        # remove it from the list and recurse back thru
        if bestfit_fieldratio.field.matched:
            self.field_ratios.pop()
            return self.get_best_fieldratio()

        # Else, return the best-fit field/ratio tuple
        return bestfit_fieldratio

    def _calc_ratio(self, field: SingleField) -> float:
        bestkey = strings.get_bestkey(
            search_dict={self.name: self.fieldpattern.terms},
            target=field.header,
            mode=self.fieldpattern.mode,
            default_value=None,
            case_sensitive=self.fieldpattern.case_sensitive,
            min_ratio=self.fieldpattern.min_ratio,
        )
        return bestkey.ratio

    @staticmethod
    def row_ratio(fieldpatterns: List[FieldPattern], headers_string: str) -> float:
        """Calculate the average ratio for a potential header row"""
        individual_ratios = (
            FieldParser._fieldpattern_ratio(fieldpattern, headers_string)
            for fieldpattern in fieldpatterns
        )
        total = sum(individual_ratios)
        try:
            average = total / len(fieldpatterns)
        except ZeroDivisionError:
            average = 0.0
        return average

    @staticmethod
    def _fieldpattern_ratio(fieldpattern: FieldPattern, headers_string: str) -> float:
        search_terms = fieldpattern.terms
        if not fieldpattern.case_sensitive:
            search_terms = [
                search_term.lower()
                for search_term in search_terms
            ]
            headers_string = headers_string.lower()
        if fieldpattern.mode == 'approx':
            return strings.get_best_ratio(search_terms, [headers_string])
        else:
            for term in search_terms:
                if term in headers_string:
                    return 1.0
        return 0.0

    def assign_bestfit_field(self) -> None:
        # This is called when a FieldPattern has found a match

        field: Union[SingleField, MultiField] = self.get_best_fieldratio().field
        field.ratio = self.bestfit_ratio
        field.name = self.name
        field.cellpattern = self.fieldpattern.cellpattern

        # Finally, mark both as matched
        field.matched = True
        self.matched = True

    @property
    def still_seeking(self):
        if self.fieldpattern.multifield and self.get_best_fieldratio():
            return True
        if self.matched or self.get_best_fieldratio() is None:
            return False
        return True

    @property
    def name(self):
        return self.fieldpattern.name  # pragma: no cover

    def __repr__(self):
        return get_repr(self)  # pragma: no cover
