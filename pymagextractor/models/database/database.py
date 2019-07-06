from pymagextractor.models.utils import create_dirs
from .workspace import WorkSpace
import pathlib
import cv2


class DataBase:
    def __init__(self, data_base_path):
        dirs = []

        self._db_dir = pathlib.Path(data_base_path)
        dirs.append(self._db_dir)

        self._workspaces_dir = self._db_dir / "workspaces"
        dirs.append(self._workspaces_dir)

        self._settings_dir = self._db_dir / "settings"
        dirs.append(self._settings_dir)

        self._settings_anns_dir = self._settings_dir / "workspaces_annotations"
        dirs.append(self._settings_anns_dir)

        create_dirs(dirs)

    def __len__(self):
        return len(list(db._workspaces_dir.iterdir()))

    @property
    def workspaces(self):
        return list(i.name for i in self._workspaces_dir.iterdir())

    def __getitem__(self, key):
        d = dict([(i.name, i) for i in self._workspaces_dir.iterdir()])
        if key in d.keys():
            return WorkSpace(str(d[key]))
        else:
            # TODO: make this better
            raise ValueError

    def new_workspace(self, name: str):
        ws = self._workspaces_dir / name
        create_dirs(ws)

        ws_anns = self._settings_anns_dir / (name + ".toml")
        ws_anns.write_text("")

        return WorkSpace(str(ws), str(ws_anns))


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
