from PySide2 import QtWidgets as qtw
from pymagextractor.models.buffer.video import Video
import pytest


@pytest.fixture(scope="function")
def video(encoded_video):
    video = Video(str(encoded_video))
    return video


def test_next_frame(video):
    for i in range(10):
        frame = video._next_frame_slot()

        id_1 = frame.frame_id

        assert i == id_1

def test_jump_frame(video):
    for i in range(0, 10, 2):
        frame = video._jump_frame_slot(i)

        id_1 = frame.frame_id

        print(i, id_1)
        # assert i == id_1

def test_previous_frame(video):
    video._jump_frame_slot(10)

    # for i in range(10, 0, -1):
        # frame = video._previous_frame_slot()

        # id_1 = frame.frame_id

        # assert i == id_1
