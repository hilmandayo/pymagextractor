class TrackedObject:

    def __init__(self, track_id):
        self.track_id = track_id
        self.detections = []

    def add_detection(self, detection):
        self.detections.append(detection)

    def remove_detection(self, detection):
        self.detections.remove(detection)

    def frames(self):
        """All the frames that the tracked object appeared"""
        frames_id = []
        for d in self.detections:
            frames_id.append(d.frame_id)
        return frames_id

    def is_on_frame(self, frame_id):
        """Check if tracked object appeared on the given frame id"""
        return frame_id in self.frames()

    def detection_on_frame(self, frame_id):
        """Get the Detection Object on the given frame_id"""
        for d in self.detections:
            if frame_id == d.frame_id:
                return d
