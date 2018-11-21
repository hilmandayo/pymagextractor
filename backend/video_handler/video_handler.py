from collections import deque
import threading

import cv2

from . import helper


# TODO: Credit to the creator.
# TODO: Test!
# TODO: How to taiou the one with bigger buffer?
class VideoCaptureAsync:
    def __init__(self, src=0, width=None, height=None, queue_size=128):
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.Q = deque(maxlen=queue_size)
        # self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.lock = threading.Lock()

        self.refreshed = False
        # This bookkeeping would be in asymmetric format.
        self.refresh_start = None
        self.refresh_end = None
        self.Q_frame_head = None  # TODO: 0 is better?
        self.Q_frame_tail = 0

    # Not needed?
    def set(self, var1, var2):
        self.cap.set(var1, var2)

    def start(self):
        if self.started:
            print('[!] Asynchroneous video capturing has already been started.')
            return None
        self.started = True
        self.thread = threading.Thread(target=self._update, args=())
        self.thread.start()
        return self

    def _refresh_deque(self, new_start, new_end, old_head, old_tail):
        helper._refresh_deque(self, new_start, new_end, old_head, old_tail)

    def _update(self):
        while self.started:
            if self.refreshed:
                old_head, old_tail = self.Q_frame_head, self.Q_frame_tail
                new_start, new_end = self.refresh_start, self.refresh_end
                self._refresh_deque(new_start, new_end, old_head, old_tail)
                self.refreshed = False

            if not len(self.Q) >= self.Q.maxlen:
                grabbed, frame = self.cap.read()
                if grabbed:
                    self.Q.append(frame)

                    if self.Q_frame_head is None:
                        self.Q_frame_head = 0
                    self.Q_frame_tail += 1
            # else:
            #     print(len(self.Q))

    def refresh_deque(self, start, end):
        with self.lock:
            self.refresh_start = start
            self.refresh_end = end
            self.refreshed = True

    def stop(self):
        self.started = False
        self.thread.join()

    def exit(self):
        self.cap.release()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()
