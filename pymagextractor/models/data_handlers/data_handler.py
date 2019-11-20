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

    def add_handlers(self, *handlers):
        for handler in handlers:
            self.handlers[handler.ref] = handler

        self.data = {}
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

    def save(self):
        new = {}
        for k, v in self.data.items():
            print(k, v)
            # print("here ")
            # print(len(list(v.values())[0]))
            v["track_id"] = [k for i in range(len(list(v.values())[0]))]
            for kk, vv in v.items():
                r = new.get(kk, None)
                if r is None: r = []
                r.extend(vv)
                new[kk] = r

        print(new)
        pd.DataFrame(new).to_csv(self.input_file, index=False)

    def __iter__(self):
        self.idx += 1

    def load_data(self):
        assert self.input_file.exists()

        ret = pd.read_csv(self.input_file, index_col=0)
        track_ids = ret["track_id"]

        for idx in ret.index:
            gg = ret.iloc[idx]
            print(gg)
        #     temp = {}
        #     for k, v in gg.iteritems():
        #         if k == "track_id":
        #             t_r = int(v)
        #         else:
        #             r = temp.get(k, None)
        #             if r is None:
        #                 r = []
        #                 temp[k] = r
        #             r.append(v)
        #     self.data[t_r] = temp

        # print(self.data)

    def load_object(self):
        # let say the name of the csv itself have the name of the instance...

        sess.TokuteiObject()
