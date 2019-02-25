"""Implementation of TrackedObject class."""


#TODO: object into d_object?
class TrackedObject:
    """A class that encapsulated the information of a single object instance.

    A single tracked object will possibly be detected across multiple frames.
    All of those information, which will be stored as instances of
    `Detection` class will be stored here.
    """
    def __init__(self, track_id):
        self.track_id = track_id
        self.detections = []

    def add_detection(self, detection):
        """Add a Detection Object in detection list"""
        self.detections.append(detection)

    def remove_detection(self, detection):
        """Remove a Detection Object from detection list"""
        self.detections.remove(detection)

    def number_of_frames(self):
        """Get how many frames the tracked object is shown"""
        return len(self.detections)

    def frames_sequence(self):
        """All the frames that the tracked object appeared"""
        frames_id = []
        for d in self.detections:
            frames_id.append(d.frame_id)
        return frames_id

    def is_on_frame(self, frame_id):
        """Check if tracked object appeared on the given frame id"""
        return frame_id in self.frames_sequence()

    def detection_on_frame(self, frame_id):
        """Get the Detection Object on the given frame_id"""
        for d in self.detections:
            if frame_id == d.frame_id:
                return d
