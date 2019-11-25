"""
Simple repr for the major classes
"""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None
from typing import List


def get_repr(self):
    return f"<{self.__class__.__name__} {repr(self.name)} {hex(id(self))}>"


def force_list(value) -> List:
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
        return value
    try:
        return list(value)
    except TypeError:
        return [value]