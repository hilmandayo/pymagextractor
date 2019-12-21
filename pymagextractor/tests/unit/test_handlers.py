import pytest
# TODO: handler vs handlers?
from pymagextractor.models.data_handler import Handler


def test_member_access():
    h = Handler("Default", "default", False)
    assert (h.name, h.ref, h.button) == ("Default", "default", False)

@pytest.mark.skip(reason="Future implementation")
def test_ref_member():
    """`Handler.ref should be the right default value`"""
    h = Handler("Default", "d this", False)
    assert (h.name, h.ref, h.button) == ("Default", "d_this", False)
