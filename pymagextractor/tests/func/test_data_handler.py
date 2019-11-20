from pymagextractor.models import data_handlers
import pytest


@pytest.fixture
def one_default_data_handlers():
    dh = data_handlers.DataHandler("/tmp/test.csv")
    dh.add_handlers(
        data_handlers.handlers.TrackID(), data_handlers.handlers.FrameID(),
        data_handlers.handlers.X1(), data_handlers.handlers.Y1(),
        data_handlers.handlers.X2(), data_handlers.handlers.Y2(),
        )
    return dh

def test_add_handlers(one_default_data_handlers):
    dh = one_default_data_handlers
    # dh.add(x1=20, y1=20, x2=20, y2=20, track_id=3, frame_id=15, )
    # dh.add(x1=22, y1=22, x2=22, y2=22, track_id=2, frame_id=15, )
    # dh.add(x1=22, y1=22, x2=22, y2=22, track_id=3, frame_id=15, )
    # dh.add("x1", 20)
    # dh.add("y1", 20)
    # dh.add("x2", 30)
    # dh.add("y2", 30)
    # dh.add("track_id", 3)
    # dh.add("frame_id", 15)
    # dh.add("object", "left")

    # dh.add("x1", 21)
    # dh.add("y1", 21)
    # dh.add("x2", 31)
    # dh.add("y2", 31)
    # dh.add("track_id", 4)
    # dh.add("frame_id", 20)
    # dh.add("object", "left")

    # dh.save()
