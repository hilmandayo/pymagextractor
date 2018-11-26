from collections import namedtuple
import pandas as pd


class CSVRefinedTrackedObjects:
    """A class that will handle the CSV result of a refined tracked detected objects.

    Attributes
    __________

    """
    def __init__(self, csv_source):
        # Set the `index_col` to use the `track_id`.
        self._csv_source = pd.read_csv(csv_source, index_col=1)

        # TODO: Work more on this
        self.max_track_id = self._csv_source.index.max()
        self.min_track_id = self._csv_source.index.min()
        # TODO: Make an interface for to check current track id.
        self.current_track_id = self.min_track_id
        self.iterated = False

    def _increase_track_id(self):
        if self.iterated and self.current_track_id < self.max_track_id:
            self.current_track_id += 1

        # This code will be executed at first call to this method only.
        if not self.iterated:
            self.iterated = True

    def _decrease_track_id(self):
        if self.iterated and self.current_track_id > self.min_track_id:
            self.current_track_id -= 1

    def _get_object(self):
        return self._csv_source.loc[[self.current_track_id]]

    def get_next_object(self):
        self._increase_track_id()
        return self._get_object()

    def get_prev_object(self):
        self._decrease_track_id()
        return self._get_object()

    def close(self):
        # self._csv_source.dispose()
        pass


class CSVOriginalTrackedObjects:
    def __init__(self, csv_source):
        # Set the `index_col` to use the `frame_id`.
        self._csv_source = pd.read_csv(csv_source, index_col=0)

        self.max_frame_id = self._csv_source.index.max()
        self.min_frame_id = self._csv_source.index.min()
        self.current_frame_id = self.min_frame_id

    def get_corresponding_objects(self, refined_tracked_object):
        start = refined_tracked_object.frame_id.min()
        finish = refined_tracked_object.frame_id.max()

        # The pandas slicing will be inclusive
        return self._csv_source.loc[start:finish]

    def close(self):
        # self._csv_source.dispose()
        pass


class CSVDualTrackedObjects:
    def __init__(self, refined: str, original: str):
        self.original_objects = CSVOriginalTrackedObjects(original)
        self.refined_objects = CSVRefinedTrackedObjects(refined)

    def get_next_dual_object(self):
        refined_object = self.refined_objects.get_next_object()
        corresponding_objects = self.original_objects.get_corresponding_objects(refined_object)

        return refined_object, corresponding_objects

    def get_prev_dual_object(self):
        refined_object = self.refined_objects.get_prev_object()
        corresponding_objects = self.original_objects.get_corresponding_objects(refined_object)

        return (refined_object, corresponding_objects)

    def close(self):
        self.refined_objects.close()
        self.original_objects.close()



# TODO: make framework to produce csv as I need.
# TODO: Check if get_next and get_prev method is working properly.
