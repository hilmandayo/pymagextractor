"""Implementation of TrackList class."""


# TODO: Rename to TrackedList?
class TrackList:
    """stores all of the detection information from a single (possibly CSV) file.

    Every detection stored here will be based on their track_id (0-based index).
    """
    NO_SELECTION = -1
    FIRST_OBJECT = 0

    def __init__(self):
        self.tracked_objects = []
        self.index = self.NO_SELECTION  # Tracked objects list index

    def add_object(self, new_track_object):
        # TODO: Create exception in case there is a repeated track_id for the Track Object
        self.tracked_objects.append(new_track_object)

    def get_current_object(self):
        """Get current selected object"""
        if self.index == self.NO_SELECTION:
            return None
        else:
            return self.tracked_objects[self.index]

    def get_next_object(self):
        """Get next tracked object in the list sequence"""
        if self.index < len(self.tracked_objects)-1:
            self.index += 1
        else:
            self.index = self.NO_SELECTION
        return self.get_current_object()

    def get_previous_object(self):
        """Get previous tracked object in the list sequence"""
        if self.index == self.NO_SELECTION:
            self.index = len(self.tracked_objects) - 1
        elif self.index == self.FIRST_OBJECT:
            self.index = self.NO_SELECTION
        else:
            self.index -= 1
        return self.get_current_object()

    def get_all_objects(self, frame_id):
        """Get all the objects that appear on the given frame id"""
        tracks_obj = []
        for to in self.tracked_objects:
            if to.is_on_frame(frame_id):
                tracks_obj.append(to)
        return tracks_obj

    def is_object_selected(self):
        """If at the moment there is any object selected"""
        return self.index != self.NO_SELECTION
