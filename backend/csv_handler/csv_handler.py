import pandas as pd


class TrackedObjects:
    """A class that will handle the CSV result of a tracked detected objects.

    Attributes
    __________

    """
    def __init__(self, csv_source):
        # Set the `index_col` to use the `track_id`.
        self._csv_source = pd.read_csv(csv_source, index_col=1)

        # Make the `n_objects` it exclusive.
        self.n_objects = self._csv_source.index.max() + 1
        # This is so that `get_next_object` will be 0 when we are first starting.
        self.current_object_id = self._csv_source.index.min() - 1

    def _increase_object_id(self):
        if self.current_object_id < self.n_objects - 1:
            self.current_object_id += 1
        else:
            # TODO: Add things to be done here.
            pass

    def _decrease_object_id(self):
        if self.current_object_id > 0:
            self.current_object_id -= 1
        else:
            # TODO: Add things to be done here.
            pass

    def _get_object(self):
        return self._csv_source.loc[self.current_object_id]

    def get_next_object(self):
        self._increase_object_id()
        return self._get_object()

    def get_prev_object(self):
        self._decrease_object_id()
        return self._get_object()

    def close(self):
        pass


class DualTrackedObjects:
    def __init__(self, orig_objects, refined_objects):
        self.orig_objects = orig_objects
        self.refined_objects = refined_objects
        self.dual_objects = (self.orig_objects, self.refined_objects)

    def get_next_dual_object(self):
        for d_o in self.dual_objects:
            d_o.get_next_object()

    def get_prev_dual_object(self):
        for d_o in self.dual_objects:
            d_o.get_prev_object()
