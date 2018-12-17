"""Implementation of BufferMaster class.

This module will implement the BufferMaster class, intended to be inherited by
any video buffer related class.
"""


import pathlib
import cv2


class BufferMaster:
    """A class that should be inherited by every video buffer related class.

    This class will define some basic properties of the video passed to it. All
    of them will be treated as internal attributes which can only be read
    through method call.

    Attributes
    ----------
    _video : cv2.VideoCapture
        An instance of the video file.

    """
    def __init__(self, src: str, width: int = None, height: int = None,
                 aspect_ratio: bool = False):
        """Initialization of class.

        Parameters
        ----------
        src
            Path to the video file.

        width: , optional
            Optional parameter to resize the width of the video.

        height: , optional
            Optional parameter to resize the height of the video.

        aspect_ratio: , optional
            If `True` and either `width` or `height` parameter is given, video
            will be resized according to the `width` or `height` parameter with
            the aspect ratio is kept. If both of the `width` and `height`
            parameter is given, the video will be resized according to just the
            `width` parameter with the aspect ratio kept.

        Raises
        ------
        FileNotFoundError
            If the path to the video is not valid. 
        AssertionError
            If there is problem with the video file.
        """
        src_path = pathlib.Path(src)

        # Instantiate the video file.
        if not src_path.exists():
            raise FileNotFoundError(f'Cannot find video in the provided path {src}')
        self._video = cv2.VideoCapture(src)
        # TODO: A better error.
        if not self._video.isOpened():
            raise AssertionError(f'Problem with video file.')

        # Setting the width and height of the video and
        # instantiate the `self._width` and `self._height` accordingly.
        orig_width = self._video.get(cv2.CAP_PROP_FRAME_WIDTH)
        orig_height = self._video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if aspect_ratio:
            # TODO: A better error.
            if not width:
                raise
            h = int(orig_height * (orig_width / width))

            self._video.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self._video.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
            self._width = width
            self._height = h
        else:
            if width and height:
                self._video.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                self._video.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                self._width = width
                self._height = height
            elif width:
                self._video.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                self._width = width
                self._height = orig_height
            elif height:
                self._video.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                self._height = height
                self._width = orig_width

        # Instantiate other internal variables.
        self._path = str(src_path.parent)
        _vid = str(src_path.name)
        self._video_name = _vid[:_vid.rfind('.')]
        self._video_format = _vid[:_vid.rfind('.') + 1:]
        self._n_frames = int(self._video.get(cv2.CAP_PROP_FRAME_COUNT))

    @property
    def path(self):
        """Return the path to the source video file."""
        return self._path
 
    @property
    def video(self):
        """Return the name of the video file."""
        return self._video_name

    @property
    def format(self):
        """Return the format of the video file."""
        return self._video_format

    @property
    def n_frames(self):
        """Return the number of frames of the video file."""
        return self._n_frames

    def exit(self):
        """Release all the resources."""
        self._video.release()
