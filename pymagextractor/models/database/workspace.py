from pymagextractor.models.utils import create_dirs
from . import DataID
import pathlib
import toml


class WorkSpace:
    def __init__(self, workspace, annotations):
        self._workspace_dir = pathlib.Path(workspace)
        self._anns_file_path = annotations
        # Make this better
        assert self._workspace_dir.exists()

    def __getitem__(self, data_id):
        d = dict([(i.name, i) for i in self._workspace_dir.iterdir()])
        if data_id in d.keys():
            return DataID(str(d[data_id]))
        else:
            # TODO: make this better
            raise ValueError

    @property
    def data_ids(self):
        return list(i.name for i in self._workspace_dir.iterdir())

    def new_data_id(self, data_id):
        d = self._workspace_dir / data_id
        create_dirs(d)
        return DataID(str(d))

    @property
    def workspace(self):
        return self._workspace_dir.name

    # TODO: implement appropriate annotations stuff here
    # @property
    # def annotations(self):
    #     with open(self._anns_file) as f:
    #         anns = toml.load(f)

    #     return anns.get(self.workspace, None)

    # def save_annotations(self, ann):
    #     with open(self._anns_file) as f:
    #         anns = toml.load(f)

    #     with open(self._anns_file, "w") as f:
    #         anns[self.workspace] = ann
    #         toml.dump(anns, f)
