class DataID:
    def __init__(self, data_id):
        self._data_dir = data_id
        self._ann_dir = data_id.parent.parent / "annotations" / self._data_dir.name
        self._create_corresponding_annotations_dir()

    def _create_corresponding_annotations_dir(self):
        if not self._ann_dir.exists():
            self._ann_dir.mkdir()

    def _set_annotation_setting(self, ann_setting):
        self._ann_setting = {}
        for key, values in ann_setting.items():
            update = []
            for v in values:
                bookkeeping = len(list((self._ann_dir / key / v).glob("*jpg")))
                update.append((v, bookkeeping))
            self._ann_setting[key] = dict(update)

    def set_annotation_setting(self, ann_setting: dict):
        self._set_annotation_setting(ann_setting)
        self._create_annotation_setting()

    @property
    def buffer(self):
        """Return path to video or file of images within the DataID."""
        return str(next(self._data_dir.glob("*.avi")))
