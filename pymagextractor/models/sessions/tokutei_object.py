"Users code"

from .sessions import BBClick


class TokuteiObject(BBClick):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Tokutei"
        self._finish = False

    def upon_bb_selection(self, track_id, frame_id, x1, y1, x2, y2, delete=False):
        if self.normalize:
            x1 = x1 / self.normalize[0]
            x2 = x2 / self.normalize[0]
            y1 = y1 / self.normalize[1]
            y2 = y2 / self.normalize[1]

        if delete:
            print("Delete")

        self.save(x1, y1, x2, y2, track_id, frame_id)
        return self
        # self.save(x1, y1, x2, y2)
        # if not self._finish:
        #     self.x1 += 0.1
        #     print(self.x1)

        #     if self.x1 > 0.8:
        #         self.save()
        #         self.finish()


    def save(self, x1, y1, x2, y2, track_id, frame_id):
        if self.data_handler:
            self.data_handler.add("track_id", track_id)
            self.data_handler.add("frame_id", frame_id)
            self.data_handler.add("coords", x1, y1, x2, y2)

    def save_on_button_click(self):
        self.save()

    def finish(self):
        self._finish = True
