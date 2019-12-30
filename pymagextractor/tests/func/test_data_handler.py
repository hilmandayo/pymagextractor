from pymagextractor.models.data_handler import DataHandler
import pytest


def test_write_to_dh_single(default_data_handler):
    """Write data to `Data Handler`"""
    dh = default_data_handler
    kwargs = {"object_id":4, "frame_id": 10, "x1": 10, "x2": 20, "x3": 30, "x4": 40}
    dh.add(**kwargs)

    ret = dh.get(kwargs.pop("object_id"))
    for key, val in kwargs.items():
        assert val == ret[key][0]

def test_write_to_dh_multiple(default_data_handler):
    """Write data to `Data Handler`"""
    dh = default_data_handler
    kwargs1 = {"object_id":4, "frame_id": 10, "x1": 10, "x2": 20, "y1": 30, "y2": 40}
    kwargs2 = {"object_id":4, "frame_id": 15, "x1": 13, "x2": 23, "y1": 33, "y2": 43}
    kwargs3 = {"object_id":6, "frame_id": 77, "x1": 89, "x2": 98, "y1": 11, "y2": 18}
    dh.add(**kwargs1)
    dh.add(**kwargs2)
    dh.add(**kwargs3)

    for i, kwargs in enumerate([kwargs1, kwargs2]):
        ret = dh.get(kwargs.pop("object_id"))
        for key, val in kwargs.items():
            assert val == ret[key][i]
    for i, kwargs in enumerate([kwargs3]):
        ret = dh.get(kwargs.pop("object_id"))
        for key, val in kwargs.items():
            assert val == ret[key][i]


def test_save_load_dh_data(complicated_data_handler, capsys):
    dh = complicated_data_handler
    # TODO: How to assert this?
    dh._set_session("default")
    dh.save()

    path = dh.input_file

    new_dh = DataHandler(str(path))
    new_dh.load_data()

    assert new_dh.session == dh.session
    assert dh.data == new_dh.data


def test_load_dh_object(complicated_data_handler):
    dh = complicated_data_handler


def test_get_dh_data():
    pass
