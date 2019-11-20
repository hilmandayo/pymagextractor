"Users code"

from .sessions import BBClick


class Follow(BBClick):
    def __init__(self, x1, y1, x2, y2, frame_id, data_handlers=None, normalize=None):
        super().__init__(data_handlers=data_handlers, normalize = normalize)
        self.name = "Follow"
        self._finish = False
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


    def next(self, frame_id, x1, y1, x2, y2, delete=False):
        if not self._finish:
            self.x1 += 0.1
            print(self.x1)

            if self.x1 > 0.8:
                self.save()
                self.finish()


    def save(self):
        print(f"Save as {self.x1}, {self.x2}, {self.y1}, {self.y2}")


    def finish(self):
        self._finish = True
