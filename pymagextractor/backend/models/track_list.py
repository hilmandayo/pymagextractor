class TrackList:

    def __init__(self):
        self.tracked_objects = []
        self.current_tracked_object = None
        self.index = 0

    def add_object(self, new_track_object):
        # TODO: Create exception in case there is a repeated track_id for the Track Object
        self.tracked_objects.append(new_track_object)

    def get_next_object(self):
        """Get next tracked object in the list sequence"""
        if self.index < len(self.tracked_objects):
            self.current_tracked_object = self.tracked_objects[self.index]
            self.index += 1
        else:
            self.index = 0
            self.current_tracked_object = None
        return self.current_tracked_object

    def get_previous_object(self):
        """Get previous tracked object in the list sequence"""
        if self.index == 1:
            self.index -= 1
            self.current_tracked_object = None
        if self.index == 0:
            self.index = len(self.tracked_objects)
            self.current_tracked_object = self.tracked_objects[self.index - 1]
        else:
            self.index -= 1
            self.current_tracked_object = self.tracked_objects[self.index - 1]
        return self.current_tracked_object

    def get_all_objects(self, frame_id):
        """Get all the objects that appear on the given frame id"""
        tracks_obj = []
        for to in self.tracked_objects:
            if to.is_on_frame(frame_id):
                tracks_obj.append(to)
        return tracks_obj

    def is_object_selected(self):
        """If at the moment there is any object selected"""
        return self.current_tracked_object is not None
