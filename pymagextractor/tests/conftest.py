import pathlib
import pytest
from pymagextractor.models.data_handler import Handler, DataHandler
# Below is meant to be implemented.

# test_original.csv
# frame_id,track_id,x1,y1,x2,y2
# 8,0,10,10,40,40
# 9,1,10,10,40,40
# 9,2,10,10,40,40
# 10,110,10,40,40
# 11,1,10,10,40,40
# 11,2,10,10,40,40
# 13,2,10,10,40,40
# 13,3,10,10,40,40
# 14,4,10,10,40,40

# test_original.csv
# frame_id,track_id,x1,y1,x2,y2
# 8,0,10,10,40,40
# 9,1,10,10,40,40
# 9,2,10,10,40,40
# 10,110,10,40,40
# 11,1,10,10,40,40
# 11,2,10,10,40,40
# 13,2,10,10,40,40
# 13,3,10,10,40,40
# 14,4,10,10,40,40


@pytest.fixture(autouse=True, scope="session")
def data_center_path_file(tmp_path_factory):
    """
    Create and return `.data_center` pathlib file that will dictate the path
    to `data_center` dir.
    """
    pym = tmp_path_factory.mktemp("pymagextractor")
    ddc = pym / ".data_center"
    ddc.write_text(str(pym / "data_center"))

    return ddc


@pytest.fixture(scope="session")
def data_center_dir(data_center_path_file):
    """Create and return the `data_center` directory."""
    ddc = data_center_path_file
    dc = pathlib.Path(ddc.read_text().split("\n")[0])
    dc.mkdir()

    return dc


@pytest.fixture(scope="session")
def data_dir(data_center_dir):
    """Create and return the `data` dir."""
    dc = data_center_dir
    data = dc / "data"
    data.mkdir()

    return data


@pytest.fixture(scope="session")
def annotations_dir(data_center_dir):
    """Create the annotations dir within the data center."""
    dc = data_center_dir
    ann = dc / "annotations"
    ann.mkdir()

    return ann

@pytest.fixture
def one_default_data_handler():
    dh = DataHandler("/tmp/test.csv")
    track_id = Handler("Track ID", "track_id", False)
    frame_id = Handler("Track ID", "track_id", False)
    x1 = Handler("X1", "x1", False)
    x2 = Handler("X2", "x2", False)
    y1 = Handler("Y1", "y1", False)
    y2 = Handler("Y2", "y2", False)
    dh.add_handlers(
        track_id, frame_id,
        x1, y1,
        x2, y2
        )
    # dh.load_data()
    return dh


def one_default_data_handler():
    pass
