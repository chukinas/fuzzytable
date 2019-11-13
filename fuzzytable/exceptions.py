# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None


# --- Custom Exceptions ------------------------------------------------------
class FuzzyTableError(Exception):
    """Standard fuzzytable exception"""
    pass


class InvalidFileError(FuzzyTableError):
    def __init__(self, path):
        message = f"{repr(path)} is not a valid path."
        super().__init__(message)


class SheetnameError(FuzzyTableError, KeyError):
    def __init__(self, path, sheetname):
        message = f"Excel workbook {repr(path)} does not contain worksheet {repr(sheetname)}"
        super().__init__(message)


class InvalidRowError(FuzzyTableError, LookupError):
    def __init__(self, row_num):
        message = f"header_row must be a positive, non-zero integer. You entered {row_num}."
        super().__init__(message)


class InvalidFieldError(FuzzyTableError):
    def __init__(self, fields):
        if fields is None:
            message = f"Fields argument must be supplied if header_row_seek. You entered {fields}."
        else:
            message = f"Fields must be a string or iterable thereof. You entered {fields}."
        super().__init__(message)


class InvalidSeekError(FuzzyTableError, TypeError):
    def __init__(self, header_seek_param):
        message = f"header_seek must be True or a positive integer. You entered {header_seek_param}."
        super().__init__(message)


class InvalidRatioError(FuzzyTableError):
    def __init__(self, min_ratio):
        message = f"FuzzyTable min_ratio must be a number gt 0, lt 1. You passed {min_ratio}"
        super().__init__(message)
