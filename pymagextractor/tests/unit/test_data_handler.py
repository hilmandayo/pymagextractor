import pytest
from pymagextractor.models.data_handler import Handler, DataHandler


def test_dh_member_access(empty_data_handler):
    dh = empty_data_handler
    x1 = Handler("X1", "x1", False)
    y1 = Handler("Y1", "y1", False)

    dh.add_handlers(x1, y1)

    # test for the name
    # `Object ID` is by default created automatically
    ret = ["Object ID", "X1", "Y1"]
    for handler, r in zip(dh.handlers, ret):
        assert handler.name == r

    # test for the reference
    # `object_id` is the default one
    ret = ["object_id", "x1", "y1"]
    for handler, r in zip(dh.handlers, ret):
        assert handler.ref == r

def test_dh_load(empty_data_handler):
    """Test DataHandler load capability.

    If DataHandler is initiated with an already-there CSV file,
    it will load it.
    """
    dh = empty_data_handler
    x1 = Handler("X1", "x1", False)
    y1 = Handler("Y1", "y1", False)

    dh.add_handlers(x1, y1)

    # test for the name
    # `Track ID` is the default one
    ret = ["Object ID", "X1", "Y1"]
    for handler, r in zip(dh.handlers, ret):
        assert handler.name == r

    # test for the reference
    # `track_id` is the default one
    ret = ["object_id", "x1", "y1"]
    for handler, r in zip(dh.handlers, ret):
        assert handler.ref == r
