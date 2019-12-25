"Users code"

from .sessions import BBClick
from itertools import count

class ObjectSelect(BBClick):
    _ids = count(1)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Object Select"
        self._finish = False
        self.object_id = next(self._ids)

    def upon_bb_selection(self, object_id, frame_id, x1, y1, x2, y2, delete=False):
        if self.normalize:
            x1 = x1 / self.normalize[0]
            x2 = x2 / self.normalize[0]
            y1 = y1 / self.normalize[1]
            y2 = y2 / self.normalize[1]

        if delete:
            print("Delete")

        self.frame_id = frame_id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.data_handler.add_session_object(self)
        # self.save(x1, y1, x2, y2, self.object_id, frame_id)
        return self
        # self.save(x1, y1, x2, y2)
        # if not self._finish:
        #     self.x1 += 0.1
        #     print(self.x1)

        #     if self.x1 > 0.8:
        #         self.save()
        #         self.finish()


    def save(self, x1, y1, x2, y2, object_id, frame_id):
        if self.data_handler:
            self.data_handler.add(object_id=object_id, frame_id=frame_id,
                                  x1=x1, y1=y1, x2=x2, y2=y2)

    def save_on_button_click(self, frame_id, type_, subtype_):
        self.data_handler.add_on_button_click(
            object_id=self.object_id, frame_id=frame_id, type_=type_, subtype_=subtype_
            )

    def finish(self):
        self._finish = True

    def load(self, object_id):
        self.object_id = object_id
