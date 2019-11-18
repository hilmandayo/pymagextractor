from .handlers import Handler
from pathlib import Path
import pandas as pd

class DataHandler:
    # represent a csv file
    def __init__(self, name, input_file):
        self.name = name
        self.handlers = {}
        self.input_file = input_file

    def add_handlers(self, handler):
        self.handlers[handler.name] = handler

    def add(self, name, *args):
        self.handlers[name].add(*args)

    def save(self):
        ret = {}
        this = [self.handlers["track_id"].data,
                self.handlers["frame_id"].data,
                self.handlers["coords"].data,]

        for t in this:
            for k, v in t.items():
                ret[k] = v
        pd.DataFrame(ret).to_csv(self.input_file, index=False)

    def __iter__(self):
        self.idx += 1
