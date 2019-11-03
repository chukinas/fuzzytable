from fuzzytable.patterns import FieldPattern


###  1  ###
def test_fieldpattern_repr():
    field_pattern = FieldPattern('the name')
    representation = repr(field_pattern)
    print(representation)
