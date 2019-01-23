import pandas as pd
from pymagextractor.backend.models.detection import Detection
from pymagextractor.backend.models.tracked_object import TrackedObject
from pymagextractor.backend.models.track_list import TrackList


def CSVHandler(csv_source):
    """Method to parse a CSV file and create a TrackList"""
    csv = pd.read_csv(csv_source)

    # Get all the tracks ids at the CSV
    all_track_ids = list(set(csv['track_id']))

    track_list = TrackList()

    for track_id in all_track_ids:
        # Create Track Object
        track_obj = TrackedObject(track_id)
        for row in csv.loc[csv['track_id'] == track_id].values.tolist():
            # Create Detection
            frame_id = row[0]
            x1 = row[2]
            y1 = row[3]
            x2 = row[4]
            y2 = row[5]
            d = Detection(frame_id, x1, y1, x2, y2)
            track_obj.add_detection(d)
        # Add Track Object in the Track List
        track_list.add_object(track_obj)

    return track_list
