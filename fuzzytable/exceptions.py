# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None


# --- Custom Exceptions ------------------------------------------------------
class FuzzyTableError(Exception):
    """
    Standard fuzzytable exception
    """
    pass


class InvalidFileError(FuzzyTableError):
    """
    Raised if FuzzyTable was passed a ``path`` that it cannot handle.
    """
    def __init__(self, path):
        message = f"{repr(path)} is not a valid path."
        super().__init__(message)


class SheetnameError(FuzzyTableError, KeyError):
    """
    Raised if an excel workbook is missing the ``sheetname`` worksheet.
    """
    def __init__(self, path, sheetname):
        message = f"Excel workbook {repr(path)} does not contain worksheet {repr(sheetname)}"
        super().__init__(message)


class InvalidRowError(FuzzyTableError, LookupError):
    """
    Raised if FuzzyTable was passed an invalid ``header_row`` argument.

    Valid ``header_row`` arguments include:
        - None
        - positive (non-zero) integer
    """
    def __init__(self, row_num):
        message = f"header_row must be a positive, non-zero integer. You entered {row_num}."
        super().__init__(message)


class InvalidFieldError(FuzzyTableError):
    """
    Raised in either of these cases:

    Scenario 1:
        - FuzzyTable ``header_row_seek`` is True
        - FuzzyTable ``fields`` parameter is empty

    Scenario 2:
        - FuzzyTable was passed an invalid ``fields`` argument.

    Valid ``fields`` arguments:
        - string
        - FieldPattern instance
        - sequence of the above (in combination also acceptable)
    """
    def __init__(self, fields):
        if fields is None:
            message = f"Fields argument must be supplied if header_row_seek. You entered {fields}."
        else:
            message = f"Fields must be a string, FieldPattern instance, or iterable thereof. You entered {fields}."
        super().__init__(message)


class InvalidSeekError(FuzzyTableError, TypeError):

    """
    Raised if FuzzyTable was passed an invalid ``header_seek`` argument.

    Valid ``header_seek`` arguments:
        - boolean
        - positive (non-zero) integer
    """
    def __init__(self, header_seek_param):
        message = f"header_seek must be True or a positive integer. You entered {header_seek_param}."
        super().__init__(message)


class InvalidRatioError(FuzzyTableError):
    """
    Raised if FuzzyTable was passed an invalid ``min_ratio`` argument.

    ``min_ratio`` must be a float between 0 and 1.
    """
    def __init__(self, min_ratio):
        message = f"FuzzyTable min_ratio must be a number 0 < x < 1. You passed {min_ratio}"
        super().__init__(message)


class CellPatternError(FuzzyTableError, TypeError):
    """
    Raised if FieldPattern was passed an invalid ``cellpatterns`` argument.

    Valid cellpattern arguments include:
        - a subclass of CellPattern or an instance thereof
        - any callable
        - a sequence of the above
    """
    def __init__(self, value):
        message = f"Cell patterns must a subclass or instance of fuzzytable.patterns.cellpattern.CellPattern or a callable. You passed {repr(value)} instead."
        super().__init__(message)


class MissingFieldError(FuzzyTableError):
    """
    Raised if the following are true:
        - at least one desired field was passed to FuzzyTable
        - FuzzyTable missingfielderror_active was set to True.
        - one or more of the desired fields wasn't found
    """
    def __init__(self, missingfieldnames, fuzzytablename=None):
        if fuzzytablename is None:
            message = f"Error: the table is missing fields {repr(missingfieldnames)}"
        else:
            message = f"Error: the {repr(fuzzytablename)} table is missing fields {repr(missingfieldnames)}."
        super().__init__(message)


class UninstantiatededCellPatternError(FuzzyTableError):
    """
    Some cell patterns must be instantiated prior to passing to a FieldPattern.
    """
    def __init__(self, cellpattern_class):
        message = f"The {repr(cellpattern_class)} must be instantiated before being passed to a FieldPattern."


class ModeError(FuzzyTableError):
    """
   Raised if a CellPattern was passed an invalid ``mode`` argument.

   Valid cellpattern ``mode`` arguments are:
       - ``exact``
       - ``approx``
       - ``contains``
   """

    def __init__(self, mode):
        valid_entries = 'exact approx contains'.split()
        message = f"Cell pattern `mode` argument must be one of {valid_entries}. You passed {repr(mode)} instead."
        super().__init__(message)
