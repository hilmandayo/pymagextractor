class TrackList:

    def __init__(self):
        self.tracked_objects = []
        self.current_tracked_object = None

    def add_object(self, new_track_object):
        # TODO: Create exception in case there is a repeated track_id for the Track Object
        self.tracked_objects.append(new_track_object)

    def current_track_object_index(self):
        """Get the current position of the current_tracked_object at the track_objects list """
        if not self.current_tracked_object and not self.tracked_objects:
            return -1  # There is no objects on the track list
        if not self.current_tracked_object and self.tracked_objects:
            return 0
        else:
            self.tracked_objects.index(self.current_tracked_object)

    def current_tracked_object(self):
        """Get current tracked object"""
        index = self.current_track_object_index()
        if index >= 0:
            self.current_tracked_object = self.tracked_objects[index]
            return self.current_tracked_object

    def get_next_object(self):
        """Get next tracked object in the list sequence"""
        index = self.current_track_object_index()
        if index >= 0:
            if len(self.tracked_objects) > (index + 1):
                self.current_tracked_object = self.tracked_objects[index + 1]
            else:
                self.current_tracked_object = self.tracked_objects[0]
            return self.current_tracked_object

    def get_previous_object(self):
        """Get previous tracked object in the list sequence"""
        index = self.current_track_object_index()
        if index >= 0:
            self.current_tracked_object = self.tracked_objects[index - 1]
            return self.current_tracked_object

    def get_all_objects(self, frame_id):
        """Get all the objects that appear on the given frame id"""
        tracks_obj = []
        for to in self.tracked_objects:
            if to.is_on_frame(frame_id):
                tracks_obj.append(to)
        return tracks_obj
