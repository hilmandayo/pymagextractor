import pytest
from pymagextractor.models.data_handlers import DataHandler


def test_member_access():
    h = handlers.Handler("Default", "default", False)
    assert (h.name, h.ref, h.button) == ("Default", "default", False)
