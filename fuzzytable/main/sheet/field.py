from excelerator.main.fieldparser import FieldParser


class Field:

    def __init__(self, header, header_row_num, col_num):
        self.header = header

        self.col_num = col_num
        self.header_row_num = header_row_num
        self.field_seeker = None
        self.data = None

    @property
    def still_available(self):
        if self.field_seeker is None:
            return True
        else:
            return False

    # --- field seeker --------------------------------------------------------
    @property
    def field_seeker(self):
        return self._field_seeker

    @field_seeker.setter
    def field_seeker(self, value):
        self._field_seeker: FieldParser = value
        self._field_seeker.found = True
