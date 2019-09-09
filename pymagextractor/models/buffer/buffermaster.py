"""Implementation of BufferMaster class.

This module will implement the BufferMaster class, intended to be inherited by
any video buffer related class.
"""


import pathlib
import cv2
import imutils


# TODO: Refined the doc (especially about the words "video" and "buffer")
class BufferMaster:
    """A class that should be inherited by every video buffer related class.

    This class will define some basic properties of the video passed to it. All
    of them will be treated as internal attributes which can only be read
    through method call.

    Attributes
    ----------
    _buffer : cv2.VideoCapture
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
        self._buffer = cv2.VideoCapture(src)
        # TODO: A better error.
        if not self._buffer.isOpened():
            raise AssertionError(f'Problem with video file.')

        # Setting the width and height of the video and
        # instantiate the `self._width` and `self._height` accordingly.
        orig_width = self._buffer.get(cv2.CAP_PROP_FRAME_WIDTH)
        orig_height = self._buffer.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # We are trying to determine the `width` and `height value`
        if aspect_ratio:
            # TODO: Implementation of aspect_ratio based on height.
            # TODO: Appropriate error for when both width and height are not given.
            if not width:
                raise ValueError(
                    "When `aspect_ratio` is True, `width` or `height` must be specified.\n"
                    "If both are specified, value of `width` will be used."
                    )

            # h = int(orig_height * (orig_width / width))
            # self._buffer.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            # self._buffer.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
            # self._width = width
            # self._height = h

            # TODO: Make this better
            # This is not very good. Just a quick dirty fix
            ret, frame = self._buffer.read()[1]
            if ret:
                # TODO: Remove dependency with imutils
                f = imutils.resize(frame, width=width)
                height = f.shape[0]
            else:
                raise Exception(f"Problem loading the {src} video file")

        else:
            if width and height:
                # self._buffer.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                # self._buffer.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                # self._width = width
                # self._height = height
                # Everything is set
                pass
            elif width:
                height = orig_height
            elif height:
                width = orig_width

        self._width = width
        self._height = height
        # Instantiate other internal variables.
        self._abs_path = str(src_path.absolute())
        self._parent_path = str(src_path.absolute().parent)
        _buff = str(src_path.name)
        self._buffer_name = _buff[:_buff.rfind('.')]
        self._buffer_format = _buff[:_buff.rfind('.') + 1:]
        self._n_frames = int(self._buffer.get(cv2.CAP_PROP_FRAME_COUNT))
        self._fps = self._buffer.get(cv2.CAP_PROP_FPS)

    @property
    def next_frame(self, rgb=False):
        ret, frame = self._buffer.read()
        if ret:
            frame = cv2.resize(frame, (self._width, self._height))
            if rgb: frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame
        else:
            raise Exception(f"Problem getting the next frame")


    @property
    def path(self):
        """Return the absolute path to the source video file."""
        return self._abs_path

    @property
    def fps(self):
        """Return the fps of the source video file."""
        return self._fps

    @property
    def parent_path(self):
        """Return the parent path to the source video file."""
        return self._parent_path

    @property
    def buffer_name(self):
        """Return the name of the video file."""
        return self._buffer_name

    @property
    def format(self):
        """Return the format of the video file."""
        return self._buffer_format

    @property
    def dims(self):
        """Return the tuple `(w, h)` of current dimensions of the video."""
        return (self._width, self._height)

    @property
    def n_frames(self):
        """Return the number of frames of the video file."""
        return self._n_frames

    @property
    def current_frame_id(self):
        """Return the current ID of the video frame.
        """
        # Since `.get` will give the next frame_id...
        f_id = int(self._buffer.get(cv2.CAP_PROP_POS_FRAMES)) - 1
        if f_id < 0:
            raise ValueError(
                f"Current frame id is {f_id}. "
                f"Perhaps the video is not being read yet..."
                )
        return f_id

    def exit(self):
        """Release all the resources."""
        self._buffer.release()
