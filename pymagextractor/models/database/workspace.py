from utils import create_dirs
import pathlib


class WorkSpace:
    def __init__(self, workspace):
        self._workspace_dir = pathlib.Path(workspace)
        # Make this better
        assert self._workspace_dir.exists()

        self._data_id_dirs = list(i for i in self._workspace_dir.iterdir())

    def __getitem__(self, data_id):
        pass

    def new_data_id(self, data_id):
        d = self._workspace_dir / data_id
        create_dirs(d)
        self.data_ids_dirs.append(d)
        # return DataID(str(d))
