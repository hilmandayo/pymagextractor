from queue import Queue
import threading

import cv2


# TODO: Credit to the creator.
# TODO: Test and compare this version with the normal one.
# TODO: REWRITE BACK EVERYTHING!
class VideoCaptureAsync:
    def __init__(self, src=0, width=None, height=None, queue_size=128):
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.Q = Queue(maxsize=queue_size)
        # self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.lock = threading.Lock()

        self.Q_frame_start = None
        self.Q_frame_end = 0

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

    def _refresh_queue(self, old_start, old_end):
        if self.Q_frame_end >= old_end:
            pass  # cont from here

    def _update(self):
        old_start = self.Q_frame_start
        old_end = self.Q_frame_end
        while self.started:
            if old_start != self.Q_frame_start or old_end != self.Q_frame_end:
                self._refresh_queue(old_start, old_end)

                old_start = self.Q_frame_start
                old_end = self.Q_frame_end

            if not self.Q.full():
                grabbed, frame = self.cap.read()
                if grabbed:
                    self.Q.put(frame)

                    if self.Q_frame_start is None:
                        self.Q_frame_start = 0
                    self.Q_frame_end += 1

    def refresh_queue(self, start, end):
        with self.lock:  # Is this needed?
            self.Q_frame_start = start
            self.Q_frame_end = end

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
            grabbed = self.grabbed
        return grabbed, frame

    def stop(self):
        self.started = False
        self.thread.join()

    def exit(self):
        self.cap.release()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()


# Continue:
# 1) Make sure how threading works
# 2) Make a really good plan
# 3) Check about lock
# 4) Make sure of case too high of start and end
