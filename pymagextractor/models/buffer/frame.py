import warnings

class Frame:
    # TODO: standardized the name image to frame?
    def __init__(self, image, frame_id,):
        if isinstance(image, int):
            warnings.warn('WARNING. The `Frame` class signature `(self, frame_id, image)` is deprecated.\n'
                          'In future release, `(self, image, frame_id)` will be used.')
            image, frame_id = frame_id, image

        self.image = image
        self.frame_id = frame_id
