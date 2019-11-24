from fuzzytable import FuzzyTable
import pytest
from fuzzytable.exceptions import MissingFieldError


@pytest.mark.parametrize('kwargs', [
    {},
    {'name': 'Just a Test'},
])
def test_missingfielderror(firstlastnames, kwargs):

    with pytest.raises(MissingFieldError):
        FuzzyTable(
            path=firstlastnames.path,
            fields='first_name last_name middle_name'.split(),
            missingfieldserror_active=True,
            **kwargs,
        )
