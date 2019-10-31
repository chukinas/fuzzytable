# --- Standard Library Imports ------------------------------------------------
from pathlib import Path

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
# None


# --- path to excel sheet -----------------------------------------------------

@pytest.fixture(scope='session')
def fixture_path():
    return Path(__file__).parent / 'test_files' / "test_utils.xlsx"


# --- standard set of expected results ----------------------------------------

@pytest.fixture(scope='session')
def expected_fields():
    return {
        'first_name': 'Rose Amy River'.split(),
        'last_name': 'Tyler Pond Song'.split(),
        'last_appearance': [2013, 2013, 2015],
    }


@pytest.fixture(scope='session')
def expected_records(expected_fields):
    keys = expected_fields.keys()
    records_count = 3
    records = list()
    for i in range(records_count):
        record = dict()
        for key in keys:
            record[key] = expected_fields[key][i]
        records.append(record)
    return records
