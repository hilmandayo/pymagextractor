class Handler:
    def __init__(self):
        pass

class TrackID(Handler):
    def __init__(self, name, *keys):
        self.name = name
        self.data = None

    def add(self, track_id):
        if self.data:
            self.data["track_id"].append(track_id)
        else:
            self.data = {
                "track_id": [track_id],
            }

class FrameID(Handler):
    def __init__(self, name, *keys):
        self.name = name
        self.data = None

    def add(self, frame_id):
        if self.data:
            self.data["frame_id"].append(frame_id)
        else:
            self.data = {
                "frame_id": [frame_id],
            }

class Coordinates(Handler):
    def __init__(self, name, *keys):
        self.keys = keys
        self.name = name
        self.data = None

    def add(self, x1, y1, x2, y2):
        if self.data:
            self.data["x1"].append(x1)
            self.data["y1"].append(y1)
            self.data["x2"].append(x2)
            self.data["y2"].append(y2)
        else:
            self.data = {
                "x1": [x1],
                "y1": [y1],
                "x2": [x2],
                "y2": [y2],
            }

class Object(Handler):
    def __init__(self, name, *keys):
        self.keys = keys
        self.name = name

    def add(self, *objects):
        for o in objects:
            if self.data:
                self.data[o] = [o]
            else:
                self.data[o].append(o)


class Tags(Handler):
    def __init__(self, name, *keys):
        self.keys = keys
        self.name = name

    def add(self, track_id):
        if self.data:
            self.data["track_id"].append(track_id)
        else:
            self.data = {
                "track_id": [track_id],
            }
