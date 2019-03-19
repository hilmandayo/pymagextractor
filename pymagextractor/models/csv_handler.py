# Maybe make this a module full of certain types of format to tracked object?
import pandas as pd
from pymagextractor.models.container.detection import Detection
from pymagextractor.models.container.tracked_object import TrackedObject
from pymagextractor.models.container.track_list import TrackList


# TODO: Model a test unit func based on this converter.
def CSVHandler(csv_source):
    """Method to parse a CSV file and create a TrackList."""
    csv_file = pd.read_csv(csv_source)

    # Get all the tracks ids at the CSV
    all_track_ids = list(set(csv_file['track_id']))

    track_list = TrackList()

    for track_id in all_track_ids:
        # Create Track Object
        track_obj = TrackedObject(track_id)
        for row in csv_file.loc[csv_file['track_id'] == track_id].values.tolist():
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
