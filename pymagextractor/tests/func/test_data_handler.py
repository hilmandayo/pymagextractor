from pymagextractor.models import data_handlers
import pytest


@pytest.fixture
def one_data_handlers():
    return data_handlers.DataHandler

def test_add_handlers(one_data_handlers):
    pass
