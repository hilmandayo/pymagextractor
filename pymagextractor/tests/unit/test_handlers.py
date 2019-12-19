import pytest
# TODO: handler vs handlers?
from pymagextractor.models.data_handlers import handlers


def test_member_access():
    h = handlers.Handler("Default", "default", False)
    assert (h.name, h.ref, h.button) == ("Default", "default", False)

@pytest.mark.skip(reason="Future implementation")
def test_ref_member():
    """`Handler.ref should be the right default value`"""
    h = handlers.Handler("Default", "d this", False)
    assert (h.name, h.ref, h.button) == ("Default", "d_this", False)
