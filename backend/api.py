from collections import namedtuple
import time

import pandas as pd

from video_handler import FramesBuffer
from csv_handler import csv_handler


DualObject = namedtuple('DualObject', 'frames refined correspond')
TrackedObject = namedtuple('TrackedObject', 'frame_id track_id x1 y1 x2 y2')


# TODO: How the inner state of video_handler should be?
class DualTrackedObjects:
    def __init__(self, fb: FramesBuffer, refined: str, original: str):
        self.csvdto = csv_handler.CSVDualTrackedObjects(refined, original)
        self.fb = fb.start()

    def get_next_dual_object(self):
        refined, correspond = self.csvdto.get_next_dual_object()
        return self._get_object(refined, correspond)

    def get_prev_dual_object(self):
        refined, correspond = self.csvdto.get_prev_dual_object()
        return self._get_object(refined, correspond)

    def _get_object(self, refined, correspond):
        start, end = refined.frame_id.min(), refined.frame_id.max() + 1  # Asymmetric.
        if end - start >= 128:
            # Temporary solution for overflow
            end = 128 + start
        self.fb.refresh_deque(start, end)

        # TODO: ABUNAI!
        time.sleep(2)
        frames = self.fb.get_frames(start, end)

        # TODO: Test for possibility of Series instances
        dual_object = DualTrackedObject(frames, refined, correspond)
        return dual_object

    def close(self):
        self.fb.stop()
        self.csvdto.close()


class DualTrackedObject:
    def __init__(self, frames, refined_object: pd.DataFrame, corresponding_objects: pd.DataFrame):
        if not isinstance(refined_object, pd.DataFrame):
            raise TypeError(
                f'`refined_object` if a type of {type(refined_object)}. Only accept type of `pd.DataFrame`.'
            )
        if not isinstance(corresponding_objects, pd.DataFrame):
            raise TypeError(
                f'`corresponding_object` if a type of {type(corresponding_object)}. Only accept type of `pd.DataFrame`'
            )
        self.refined_object = refined_object
        self.offset = self.refined_object.frame_id.min()
        self.corresponding_objects = corresponding_objects
        self.frames = frames

    def __getitem__(self, i: int) -> DualObject:
        # Temporary for overflow solution.
        if i >= 128:
            i = 127
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

        start = j.min() - self.offset
        end = j.max() - self.offset + 1
        # TODO: Need to understand and possibly modify this.
        frames = self.frames[start:end]

        return DualObject(frames, ref, corrs)

    def __len__(self):
        return len(self.refined_object)
