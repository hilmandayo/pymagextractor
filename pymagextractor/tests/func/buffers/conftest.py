import pytest
import numpy as np
import cv2


size = (300, 300, 3)
length = 256

@pytest.fixture(scope="session")
def make_black_video():
    black = np.zeroes(size, np.uint8)
    # TODO: save the video


@pytest.fixture(scope="session")
def make_white_video():
    white = np.fill(255, size, np.uint8)
    # TODO: save the video


# TODO: emulate video with pure numpy array
@pytest.fixture(scope="session")
def encoded_video(data_dir):
    video_path = data_dir / "video.mp4"
    video_str = str(video_path)
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = cv2.VideoWriter(video_str, fourcc, 15, size[:2], True)

    black = np.zeros(size, np.uint8)
    for i in range(length):
        b = black.copy()

        writer.write(b)
    writer.release()

    yield video_path

    video_path.unlink()
