"""
Simple repr for the major classes
"""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None


def get_repr(self):
    return f"<{self.__class__.__name__} {repr(self.name)} {hex(id(self))}>"





