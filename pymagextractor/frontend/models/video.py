import cv2


class Video:

    def __init__(self):
        self.path = ""
        self.cv = None
        self.fps = 30  # Normally 30 frames per second
        self.length_frames = 0

    def set_path(self, path):
        self.path = path
        self.cv = cv2.VideoCapture(self.path)
        self.fps = self.cv.get(cv2.CAP_PROP_FPS)
        self.length_frames = int(self.cv.get(cv2.CAP_PROP_FRAME_COUNT))
