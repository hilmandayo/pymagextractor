from collections import namedtuple
import pandas as pd


DualObject = namedtuple('DualObject', 'refined correspond frame')
TrackedObject = namedtuple('TrackedObject', 'frame_id track_id x1 y1 x2 y2')


class RefinedTrackedObjects:
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
        self._csv_source.close()


class OriginalTrackedObjects:
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
        self._csv_source.close()


class DualTrackedObjects:
    def __init__(self, refined: str, original: str):
        self.original_objects = OriginalTrackedObjects(original)
        self.refined_objects = RefinedTrackedObjects(refined)

    def get_next_dual_object(self):
        refined_object = self.refined_objects.get_next_object()
        corresponding_objects = self.original_objects.get_corresponding_objects(refined_object)

        # TODO: Test for possibility of Series instances
        dual_object = DualTrackedObject(refined_object, corresponding_objects)

        return dual_object

    def get_prev_dual_object(self):
        refined_object = self.refined_objects.get_prev_object()
        corresponding_objects = self.original_objects.get_corresponding_objects(refined_object)

        # TODO: Test for possibility of Series instances
        dual_object = DualTrackedObject(refined_object, corresponding_objects)

        return dual_object

    def close(self):
        self.refined_objects.close()
        self.original_objects.close()



class DualTrackedObject:
    def __init__(self, refined_object: pd.DataFrame, corresponding_objects: pd.DataFrame):
        if not isinstance(refined_object, pd.DataFrame):
            raise TypeError(
                f'`refined_object` if a type of {type(refined_object)}. Only accept type of `pd.DataFrame`.'
            )
        if not isinstance(corresponding_objects, pd.DataFrame):
            raise TypeError(
                f'`corresponding_object` if a type of {type(corresponding_object)}. Only accept type of `pd.DataFrame`'
            )
        self.refined_object = refined_object
        self.corresponding_objects = corresponding_objects

    def __getitem__(self, i: int) -> pd.Series:
        ref = self.refined_object.iloc[i]
        ref = TrackedObject(ref[0], ref.name, ref[1], ref[2], ref[3], ref[4])
        j = ref.frame_id

        corrs = []
        try:
            corr = self.corresponding_objects.loc[[j]]
            for c in corr.itertuples():
                corrs.append(TrackedObject(c.Index, c.track_id, c.x1, c.y1, c.x2, c.y2))
        except KeyError:
            corrs.append(None)

        return DualObject(ref, corrs)

    def __len__(self):
        return len(self.refined_object)

# TODO: make framework to produce csv as I need.
# TODO: Check if get_next and get_prev method is working properly.
