from .handlers import Handler
from pathlib import Path
import pandas as pd
from . import handlers as hl
import pymagextractor.models.sessions as sess

# temp mapping
HANDLER = {
    "track_id": hl.TrackID,
    "frame_id": hl.FrameID,
    "x1": hl.X1,
    "x2": hl.X2,
    "y1": hl.Y1,
    "y2": hl.Y2,
}

class DataHandler:
    # represent a csv file
    def __init__(self, input_file):
        self.handlers = {}
        self.input_file = Path(input_file)
        self.data = {}

    # TODO: Repair this according to `hl.*`
    def add_handlers(self, *handlers):
        # for handler in handlers:
        #     self.handlers[handler.ref] = handler
        self.components = []
        for h in handlers:
            self.components.append(h.ref)

        assert "track_id" in self.components

        return self

    def add(self, **kwargs):
        # self.handlers[name].add(*args)
        ret = self.data.get(kwargs["track_id"], None)
        if ret is None:
            ret = {}
        for k, v in kwargs.items():
            if k == "track_id": continue
            r = ret.get(k, None)
            if r is None: r = []
            r.append(v)
            ret[k] = r

        self.data[kwargs["track_id"]] = ret

    def add_on_button_click(self, **kwargs):
        # self.handlers[name].add(*args)
        ret = self.data.get(kwargs["track_id"], None)
        assert not ret is None

        idx = ret["frame_id"].index(kwargs["frame_id"])
        t = ret.get(kwargs["type_"], None)
        if t is None:
            t = [None for i in range(len(ret["frame_id"]))]
            ret[kwargs["type_"]] = t
        t[idx] = kwargs["subtype_"]
        print("printing ret")
        print(ret)

    def save(self):
        new = {}
        for k, v in self.data.items():
            v["track_id"] = [k for i in range(len(list(v.values())[0]))]
            for kk, vv in v.items():
                r = new.get(kk, None)
                if r is None: r = []
                r.extend(vv)
                new[kk] = r

        print(new)
        # pd.DataFrame(new).to_csv(self.input_file, index=False)

    def __iter__(self):
        self.idx += 1

    def load_data(self):
        if not self.input_file.exists(): return

        try:
            ret = pd.read_csv(self.input_file)
        except pd.errors.EmptyDataError:
            return

        track_ids = ret["track_id"]

        for idx, ii in zip(ret.index, track_ids):
            gg = ret.iloc[idx]
            temp = self.data.get(int(ii), None)
            if temp is None:
                temp = {}
                self.data[ii] = temp
            for k, v in gg.iteritems():
                if k == "track_id":
                    continue
                else:
                    r = temp.get(k, None)
                    if r is None:
                        r = []
                        temp[k] = r
                    r.append(v)


    def load_object(self):
        # let say the name of the csv itself have the name of the instance...

        retval = []
        for k, v in self.data.items():
            obj = sess.TokuteiObject()
            obj.load(int(k))
            retval.append(obj)

        retval = None if len(retval) == 0 else retval

        return retval

    def get_objects(self, key, value):
        assert key is not "track_id"

        retval = []
        for k, v in self.data.items():
            if value in v[key]:
                retval.append(k)

        if retval:
            assert len(retval) == 1
            return retval[0]

        return None
