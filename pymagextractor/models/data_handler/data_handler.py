from .handler import Handler
from pathlib import Path
import pandas as pd
import pymagextractor.models.sessions as sess
from pymagextractor.models.utils import row_length


object_id = Handler("Object ID", "object_id", False)

class DataHandler:
    # represent a csv file
    def __init__(self, input_file, session):
        self.input_file = Path(input_file)
        self.data = {}
        self.handlers = [object_id]
        self.session = None

    def _set_session(self, session):
        if self.session is None:
            self.session = session

    def add_handlers(self, *handlers):
        # TODO: Check for Name similarity too???
        refs = [h.ref for h in self.handlers]
        for handler in handlers:
            if handler.ref in refs:
                continue
            self.handlers.append(handler)

        return self


    def add(self, **kwargs):
        """Add entry and value to object.

        `object_id` will be needed by default. Exception will be raised if is not there.
        """
        try:
            object_id = kwargs.pop("object_id")
        except KeyError as e:
            raise e("Kwargs `object_id` must been pass to `DataHandler.add`")

        # TODO: Make sure passed value is the same defined Handlers
        # TODO: Make sure passed value for certain kwargs are the same with the one
        #       defined in `Handler`
        object_id_data = self.data.get(object_id, None)
        if object_id_data is None:
            object_id_data = {}
            self.data[object_id] = object_id_data

        for key, val in kwargs.items():
            data = object_id_data.get(key, None)
            if data is None:
                data = []
                object_id_data[key] = data
            data.append(val)

    def add_session_object(self, object_):
        self.add(object_id=object_.object_id, frame_id=frame_id,
                 x1=x1, y1=y1, x2=x2, y2=y2)


    def get(self, object_id):
        """Get the saved data with `object_id` as the index."""
        data = self.data.get(object_id, None)
        if data is None:
            raise Exception(f"{object_id} is not yet initialized")

        return data

    def add_on_button_click(self, **kwargs):
        ret = self.data.get(kwargs["object_id"], None)
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
        """Save data to stated csv path during initialization."""
        if self.session is None:
            raise Exception("`session` is not initialized")

        new = {i.ref: [] for i in self.handlers}
        length = row_length(self.data)

        for object_id, values in self.data.items():
            for key, list_value in values.items():
                for v in list_value:
                    new[key].append(v)

            # Add `object_id` with the correct length.
            for i in range(len(list_value)):
                new["object_id"].append(object_id)

        # Write header
        with open(self.input_file, "w") as fout:
            fout.write(f"# SESSION={self.session}\n")
            fout.write(f"\n")
            pd.DataFrame(new).to_csv(fout, index=False)

    def __iter__(self):
        self.idx += 1

    def load_data(self):
        if not self.input_file.exists(): return

        try:
            ret = pd.read_csv(self.input_file)
        except pd.errors.EmptyDataError:
            return

        track_ids = ret["object_id"]

        for idx, ii in zip(ret.index, track_ids):
            gg = ret.iloc[idx]
            temp = self.data.get(int(ii), None)
            if temp is None:
                temp = {}
                self.data[ii] = temp
            for k, v in gg.iteritems():
                if k == "object_id":
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
        assert key is not "object_id"

        retval = []
        for k, v in self.data.items():
            if value in v[key]:
                retval.append(k)

        if retval:
            assert len(retval) == 1
            return retval[0]

        return None
