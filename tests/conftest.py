# --- Standard Library Imports ------------------------------------------------
from pathlib import Path
import csv

# --- Third Party Imports -----------------------------------------------------
import pytest
from fuzzytable import FuzzyTable
import names

# --- Intra-Package Imports ---------------------------------------------------
pass


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "simple: When a code change breaks everything, runs the tests marked as simple to start. "
    )



# --- path to excel sheet -----------------------------------------------------
test_files_path = Path(__file__).parent / 'test_files'

def get_test_path(extension=None):
    if extension is None:
        extension = 'xlsx'
    filename = f"test.{extension}"
    path = test_files_path / filename
    return path

@pytest.fixture(scope='session')
def test_path():
    return get_test_path


# --- standard set of expected results ----------------------------------------

dr_who_fields_list = {
    'first_name': 'Rose Amy River'.split(),
    'last_name': 'Tyler Pond Song'.split(),
    'last_appearance': '2013 2013 2015'.split(),
}


@pytest.fixture(scope='session')
def dr_who_fields():
    return dr_who_fields_list


def fields_to_records(fields):
    records = list()
    i = 0
    while True:
        try:
            records.append({
                key: values[i]
                for key, values in fields.items()
            })
        except IndexError:
            break
        i += 1
    return records


def get_dr_who_records():
    keys = dr_who_fields_list.keys()
    records_count = 3
    records = list()
    for i in range(records_count):
        record = dict()
        for key in keys:
            record[key] = dr_who_fields_list[key][i]
        records.append(record)
    return records


@pytest.fixture(scope='session')
def dr_who_records(dr_who_fields):
    return get_dr_who_records()


# --- names_generator -------------------------------------------------------------------

class NamesFixture:

    def __init__(self, record_count=5):
        self.fields = self.get_fields(record_count)
        self.records = fields_to_records(self.fields)
        self.path = self.get_path(self.records)

    @staticmethod
    def get_fields(record_count):
        return {
            'first_name': [names.get_first_name() for _ in range(record_count)],
            'last_name': [names.get_last_name() for _ in range(record_count)]
        }

    @staticmethod
    def get_path(records):
        temp_dir = test_files_path / 'temp'
        temp_dir.mkdir(exist_ok=True)
        names_path = temp_dir / 'names.csv'
        names_path.touch()
        with open(str(names_path), "w", newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames='first_name last_name'.split())
            csvwriter.writeheader()
            csvwriter.writerows(records)
        return names_path


@pytest.fixture(scope='function')
def names_fixture():
    return NamesFixture()


# --- fuzzy tables ------------------------------------------------------------
def ft_dr_who(field_names):
    path = get_test_path('csv')
    return FuzzyTable(
        path=path,
        header_row_seek=True,
        fields=field_names,
    )


@pytest.fixture(scope='function')
def ft_dr_who_all_fields(dr_who_fields):
    return ft_dr_who(dr_who_fields)


@pytest.fixture(scope='function')
def ft_dr_who_some_fields():
    field_names = 'first_name last_name'.split()
    return ft_dr_who(field_names)


if __name__ == "__main__":
    pass
