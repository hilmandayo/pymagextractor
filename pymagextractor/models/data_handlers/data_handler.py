from .handlers import Handler
from pathlib import Path
import pandas as pd

class DataHandler:
    # represent a csv file
    def __init__(self, input_file):
        self.handlers = {}
        self.input_file = Path(input_file)
        if self.input_file.exists():
            self.load_data()

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
        ret = pd.read_csv(self.input_file, index_col=False)
        print(ret)
