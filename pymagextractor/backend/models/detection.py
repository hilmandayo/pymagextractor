class Detection:

    def __init__(self, frame_id, x1, y1, x2, y2):
        self.frame_id = frame_id
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def coordinates(self):
        return self.x1, self.y1, self.x2, self.y2

    def rect(self, ratio):
        return self.x1*ratio, self.y1*ratio, (self.x2-self.x1)*ratio, (self.y2-self.y1)*ratio
