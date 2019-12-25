"""Sessions Module.

Here, the session that can be used in `Pymagextractor` is defined.
"""

def normalize_coord(x1, y1, x2, y2, width, height):
    x1 = x1 / width
    x2 = x2 / width
    y1 = y1 / height
    y2 = y2 / height

    return x1, y1, x2, y2


class Session:
    def __init__(self,):
        pass

    def next(self):
        pass

    def previous(self):
        pass

    def save_on_click(self):
        pass



class BBClick(Session):
    def __init__(self, data_handler=None, normalize=False):
        self.data_handler = data_handler
        self.normalize = normalize

    def upon_bb_selection(self, track_id, frame_id, x1, y1, x2, y2):
        pass

    def next(self, track_id, frame_id, x1, y1, x2, y2):
        pass

    def previous(self, track_id, frame_id, x1, y1, x2, y2):
        pass

    def ask_delete(self, track_id, frame_id, x1, y1, x2, y2):
        pass

    def get(self):
        pass
