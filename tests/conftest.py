# --- Standard Library Imports ------------------------------------------------
from pathlib import Path

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
from excelerator.main import utils

test_utils_path = Path(__file__).parent / 'test_files' / "test_utils.xlsx"


@pytest.fixture(scope='session')
def fixture_path():
    return test_utils_path


def get_ws(worksheet_name):
    wb = utils.get_workbook(test_utils_path)
    return utils.get_worksheet_from_path(wb, worksheet_name)


@pytest.fixture(scope='session')
def fixture_get_ws():
    return get_ws


@pytest.fixture(scope='session')
def fixture_wb():
    return utils.get_workbook(test_utils_path)


# TODO do I need all these fixtures?
