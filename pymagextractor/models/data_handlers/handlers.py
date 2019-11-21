class Handler:
    def __init__(self):
        self.name = None    # if used as button, will use this
        self.ref = None     # name for indexing internally
        self.keys = None
        self.data = []


class TrackID(Handler):
    def __init__(self):
        super().__init__()
        self.ref = "track_id"

    def add(self, track_id):
        self.data.append(track_id)

class FrameID(Handler):
    def __init__(self):
        super().__init__()
        self.ref = "frame_id"

    def add(self, frame_id):
        self.data.append(frame_id)


class X1(Handler):
    def __init__(self):
        super().__init__()
        self.ref = "x1"

    def add(self, x1):
        self.data.append(x1)

class X2(Handler):
    def __init__(self):
        super().__init__()
        self.ref = "x2"

    def add(self, x2):
        self.data.append(x2)

class Y1(Handler):
    def __init__(self):
        super().__init__()
        self.ref = "y1"

    def add(self, y1):
        self.data.append(y1)

class Y2(Handler):
    def __init__(self):
        super().__init__()
        self.ref = "y2"

    def add(self, y2):
        self.data.append(y2)


class ObjectClass(Handler):
    def __init__(self, *args):
        super().__init__()
        self.name = "Object Class"
        self.ref = "object"
        self.data = args

    def add(self, obj):
        self.data.append(obj)


class View(Handler):
    def __init__(self, *args):
        super().__init__()
        self.name = "View"
        self.ref = "view"
        self.data = args

    def add(self, view):
        self.data.append(size)
