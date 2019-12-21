import pytest
from pymagextractor.models.data_handler import Handler, DataHandler


def test_member_access(one_default_data_handler):
    d_hd = one_default_data_handler
