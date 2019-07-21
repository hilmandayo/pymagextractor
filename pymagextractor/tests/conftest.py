import pathlib
import pytest


@pytest.fixture(scope="module")
def database_path_file(tmp_path_factory):
    """
    Create and return `.data_center` pathlib file that will dictate the path
    to `data_center` dir.
    """
    pym = tmp_path_factory.mktemp("pymagextractor")
    db = pym / ".database"
    db.write_text(str(pym / "database"))

    return db


@pytest.fixture(scope="module")
def database_dir(database_path_file):
    """Create and return the `database` directory object."""
    db = database_path_file
    dc = pathlib.Path(db.read_text().split("\n")[0])
    dc.mkdir()

    return dc


@pytest.fixture(scope="module")
def workspaces_dir(database_dir):
    """Create and return the settings directory objects."""
    workspaces_dir = database_dir / "workspaces"
    workspaces_dir.mkdir()

    return workspaces_dir


@pytest.fixture(scope="module")
def settings_dir(database_dir):
    """Create and return the settings directory objects."""
    # TODO: Make it flexible
    settings = database_dir / "settings"
    settings.mkdir()

    # TODO: put on its own fixture
    (settings / "workspaces_annotations").mkdir()

    return settings


@pytest.fixture(scope="module")
def create_workspace_dirs(workspaces_dir):
    """Return a function that can make workspace directories."""
    def _create_workspace_dirs(dirs):
        ret = []
        for d in dirs:
            d = workspaces_dir / d
            d.mkdir()
            ret.append(d)
        return ret

    return _create_workspace_dirs


@pytest.fixture(scope="module")
def create_data_id_dirs(workspaces_dir):
    """Return a function that can create data_id_dirs."""
    def _create_data_id_dirs(workspace_dirs, data_id_names):
        data_id_dirs = []
        for w, d_ids in zip(workspace_dirs, data_id_names):
            D = []
            for d_id in d_ids:
                d = w / d_id
                d.mkdir()
                D.append(d)
            data_id_dirs.append(D)

        return workspace_dirs, data_id_dirs

    return _create_data_id_dirs


@pytest.fixture(scope="module")
def create_annotations_dirs(workspaces_dir):
    """Return a function that can create annotations directories in each data id."""
    # TODO: Possibly, make this a pure fixture?
    def _create_annotations_dirs(data_id_dirs):
        anns_dirs = []
        for d in data_id_dirs:
            anns_dir = d / "annotations"
            anns_dir.mkdir()
            anns_dirs.append(anns_dir)
        return anns_dirs

    return _create_annotations_dirs


@pytest.fixture(scope="module")
def create_data_dirs(workspaces_dir):
    """Return a function that can create data directories in each data id."""
    # TODO: Possibly, make this a pure fixture?
    def _create_data_dirs(data_id_dirs):
        data_dirs = []
        for d in data_dirs:
            data_dir = d / "data"
            data_dir.mkdir()
            data_dirs.append(data_dir)
        return data_dirs

    return _create_data_dirs
