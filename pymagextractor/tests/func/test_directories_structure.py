import pytest
import pathlib
from pymagextractor.models.database import DataBase
from functools import reduce


data = [{
    "workspaces": ["hilman", "azu", "akihiro"],
    "data_ids": [["tokyo", "kuala lumpur"],
                 ["osaka", "new york"],
                 ["hokkaido", "hong kong"]]
}]

def id_gen(data):
    return f'test'

# --- Based on above parameters, build all the necessary directories --- #
@pytest.fixture(params=data, ids=id_gen, scope='module')
def build_database(request,  # built in
                   workspaces_dir, settings_dir,  # my own fixture
                   # below all will return functions
                   create_workspace_dirs,
                   create_data_id_dirs,
                   create_annotations_dirs,
                   create_data_dirs):
    workspaces = request.param["workspaces"]
    data_ids = request.param["data_ids"]

    # Create necessary workspaces
    workspace_dirs = create_workspace_dirs(workspaces)

    _, data_id_dirs = create_data_id_dirs(workspace_dirs, data_ids)

    flat_data_id_dirs = reduce(lambda a, b: a + b, data_id_dirs)
    create_annotations_dirs(flat_data_id_dirs)
    create_data_dirs(flat_data_id_dirs)

    return workspace_dirs


# --- Based on above parameters, test if all directories related funcs etc.
#     produce the same result as `build_database` fixture --- #
@pytest.mark.parametrize("data", data, ids=id_gen)
def test_database(tmp_path_factory, build_database, data):
    # Simulating a path for the database
    pym = tmp_path_factory.mktemp("pymagextractor")
    db_path = str(pym / "database")
    # the corresponding database object from `build_database` fixture
    gt_db = build_database[0].parent.parent
    # preparing the data
    workspace_names = data["workspaces"]
    workspace_names = data["workspaces"]  # CONT: from here

    # --------------------------------------------------------- #
    # Below shows how to use the Database class.                #
    # --------------------------------------------------------- #

    # Initialize the center database
    db = DataBase(db_path)

    # `db` should already have initialize every directories needed
    assert isinstance(db._workspaces_dir, pathlib.Path); assert db._workspaces_dir.name == list(gt_db.glob("workspaces"))[0].name
    assert isinstance(db._workspaces_dir, pathlib.Path); assert db._settings_dir.name == list(gt_db.glob("settings"))[0].name

    # initializing workspaces
    db.new_workspace()
