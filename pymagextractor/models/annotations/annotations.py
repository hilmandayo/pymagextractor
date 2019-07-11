from pymagextractor.models.utils import create_dirs
from copy import deepcopy
import pathlib
import toml


class Annotations:
    def __init__(self, name: str, annotations_setting: dict, annotations_dir: str):
        self._name = name
        self._anns_setting = annotations_setting
        self._anns_dir = annotations_dir

        dirs = []
        for k, v in self._anns_setting.items():
            dirs.append(self._anns_dir / k)
        create_dirs(dirs)


    def __str__(self):
        s = "Object: '{}'\nViews: {}\n"
        ret = ""
        for k, v in self._anns_setting.items():
            ret += s.format(k, v)
        return ret.strip()

    @property
    def name(self):
        return self._name

    @property
    def values(self):
        return self._anns_setting

    def save(self, object_, view, frame_id, object_id, x1, y1, x2, y2):
        file_ = self._anns_dir / object_ / f"bb_{view}.csv"
        with open(file_, "a") as f:
            w = f"{view}, {frame_id}, {object_id}, {x1}, {y1}, {x2}, {y2}\n"
            f.write(w)


# class DataCenter:
#     def __init__(self, data_base_path):
#         self._db = pathlib.Path(data_base_path)
#         self._create_dirs_structure()

#     def _create_dirs_structure(self):
#         if not self._db.exists():
#             self._db.mkdir()

#         self._data_dir = self._db / "data"
#         if not self._data_dir.exists():
#             self._data_dir.mkdir()

#         self._anns = self._db / "annotations"
#         if not self._anns.exists():
#             self._anns.mkdir()

#         self._settings = self._db / ".settings"
#         if not self._settings.exists():
#             self._settings.mkdir()

#     @property
#     def data_center(self):
#         return self._db

#     @property
#     def data_ids(self):
#         return [i.name for i in self._data_dir.iterdir()]

#     def __getitem__(self, key):
#         # TODO: filter for hidden dirs
#         d = dict([(i.name, i) for i in self._data_dir.iterdir()])
#         if key in d.keys():
#             return DataID(d[key])
#         else:
#             # TODO: make this better
#             raise ValueError


# TODO: Track all of the existing annotations and the one that
# we only one to save.
# class DataID:
#     def __init__(self, data_id):
#         self._data_dir = data_id
#         self._ann_dir = data_id.parent.parent / "annotations" / self._data_dir.name
#         self._create_corresponding_annotations_dir()

#     def _create_corresponding_annotations_dir(self):
#         if not self._ann_dir.exists():
#             self._ann_dir.mkdir()

#     def _set_annotation_setting(self, ann_setting):
#         self._ann_setting = {}
#         for key, values in ann_setting.items():
#             update = []
#             for v in values:
#                 bookkeeping = len(list((self._ann_dir / key / v).glob("*jpg")))
#                 update.append((v, bookkeeping))
#             self._ann_setting[key] = dict(update)

#     def set_annotation_setting(self, ann_setting: dict):
#         self._set_annotation_setting(ann_setting)
#         self._create_annotation_setting()

#     @property
#     def buffer(self):
#         """Return path to video or file of images within the DataID."""
#         return str(next(self._data_dir.glob("*.avi")))

#     def _create_annotation_setting(self):
#         # TODO: repair this
#         if self._ann_setting is None:
#             raise RuntimeError

#         for key, values in self._ann_setting.items():
#             pd = self._ann_dir / key
#             pd.mkdir(exist_ok=True)
#             # TODO: Improve this (csv head)
#             for v in values.keys():
#                 d = pd / f"{v}"
#                 f = pd / f"{v}.csv"

#                 d.mkdir(exist_ok=True)
#                 if not f.exists():
#                     f.write_text("")

#     def save(self, image, index: list, meta=None):
#         i1, i2 = index
#         d = self._ann_dir / i1 / i2
#         image_name = str(d / f"{str(self._ann_setting[i1][i2])}.jpg")
#         cv2.imwrite(image_name, image)

#         self._ann_setting[i1][i2] += 1
