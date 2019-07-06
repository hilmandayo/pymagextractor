from pymagextractor.models.utils import create_dirs
import pathlib


class DataID:
    def __init__(self, data_id: str):
        self._data_id_dir = pathlib.Path(data_id)
        dirs = []

        self._data_dir = self._data_id_dir / "data"
        dirs.append(self._data_dir)
        self._ann_dir = self._data_id_dir / "annotations"
        dirs.append(self._ann_dir)

        create_dirs(dirs)

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
