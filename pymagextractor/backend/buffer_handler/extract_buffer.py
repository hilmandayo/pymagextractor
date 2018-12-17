from collections import deque
from typing import Tuple, Union
import threading

from . buffermaster import BufferMaster
from . import extract_buffer_helper as helper


class ExtractBuffer(BufferMaster):
    """A class for video buffer management during the image extraction process.

    This class will handle all stuff related to video buffer. Internally, it
    will load buffer in a sequence in a deque container for a lenght specified
    by the user in another thread. It will find the optimum range of sequence
    of video that it will need to load.

    """
    def __init__(self, src: str, width: int = None, height: int = None,
                 aspect_ratio: bool = False, buffer_len: int = 128):
        """Initialization of class."""
        # TODO: How to better list the parameter above? Should I use
        #       *args and **kwargs? And how the docstring should be?
        super().__init__(src, width, height, aspect_ratio)
        self._buffer_len = buffer_len

        self._dq = deque(maxlen=self.buffer_len)
        self._started = False
        self._lock = threading.Lock()
        self._refreshed = False

        # Bookkeeping stuff. This will all be in asymmetric format.
        self.dq_head_idx = None
        self.dq_tail_idx = 0

    @property
    def buffer_len(self):
        """Return the len of buffer in memory set."""
        return self._buffer_len

    def start(self):
        """Start the threading in the background."""
        if self._started:
            print('[!] Asynchroneous video capturing has already been started.')
            return None
        self._started = True
        self._thread = threading.Thread(target=self._update, args=())
        self._thread.start()
        return self

    def _update(self):
        """Threaded function to be called."""
        while self._started:
            if self._refreshed:
                self._refreshed = False

            if not len(self.dq) > self.dq.maxlen:
                # If we still have room to add another frame...
                grabbed, frame = self.video.read()
                if grabbed:
                    self.dq.append(frame)

                    # Updating index.
                    if self.dq_tail_idx is None:
                        self.dq_head_idx = 0
                    self.Q_frame_tail += 1

    def _refresh_deque(self):
        """Refresh the deque according to `_refresh_start` and `_refresh_end`"""
        # TODO: Koko kara. How to make it truly modular?
        helper._refresh_deque()

    def update_buffer(self, start: Union[int, Tuple[int]], end: Union[int, Tuple[int]]):
        """Update the internal deque holding the buffer.

        The index should be in symmetric order (i.e. [start, end]).
        """
        # TODO: Implement for when a tuple of int is gave.
        if not (isinstance(start, int) and isinstance(end, int)):
            raise NotImplementedError

        start = (start,)
        end = (end,)
        with self._lock:
            self.refresh_start = start
            self.refresh_end = end
            self._refreshed = True

    def exit(self):
        """Release all the resources."""
        super().exit()
        self._started = False
        self.thread.join()
