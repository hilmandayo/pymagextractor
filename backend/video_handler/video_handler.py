from collections import deque
import threading

import cv2

from . import helper


# TODO: Credit to the creator.
# TODO: Test and compare this version with the normal one.
<<<<<<< HEAD
# TODO: REWRITE BACK EVERYTHING!
=======
# CONT: Try to exhaust test this framework
>>>>>>> 3220f8e... A working prototype of cv2 threads.
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

        # This bookkeeping would be in asymmetric format.
        self.Q_frame_start = 0
        self.Q_frame_end = queue_size

        # Dynamic variables.
        self.Q_frame_head = 0
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

    def _refresh_deque(self, old_start, old_end):
        # print("k")
        helper._refresh_deque(self, old_start, old_end)

    def _update(self):
        old_start = self.Q_frame_start
        old_end = self.Q_frame_end
        while self.started:
            if old_start != self.Q_frame_start or old_end != self.Q_frame_end:
                self._refresh_deque(old_start, old_end)

                # print(old_start)
                # print(old_end)
                # print(self.Q_frame_start)
                # print(self.Q_frame_end)
                # print(self.Q_frame_tail)
                # print(self.Q_frame_head)
                old_start = self.Q_frame_start
                old_end = self.Q_frame_end

            if not len(self.Q) >= self.Q.maxlen:
                grabbed, frame = self.cap.read()
                if grabbed:
                    print("I am here")
                    self.Q.append(frame)

                    if self.Q_frame_head is None:
                        self.Q_frame_head = 0
                    self.Q_frame_tail += 1
            else:
                print(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

    def refresh_deque(self, start, end):
        with self.lock:  # Is this needed?
            self.Q_frame_start = start
            self.Q_frame_end = end
            self.Q_frame_head = start
            self.Q_frame_tail = start

    def stop(self):
        self.started = False
        self.thread.join()

    def exit(self):
        self.cap.release()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()
