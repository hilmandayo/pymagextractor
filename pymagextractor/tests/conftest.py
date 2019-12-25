import pathlib
import pytest
from pymagextractor.models.data_handler import Handler, DataHandler


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


@pytest.fixture(scope="function")
def empty_data_handler():
    """Data Handler with no added handler."""
    dh = DataHandler("/tmp/test.csv")
    return dh


@pytest.fixture(scope="function")
def default_data_handler(empty_data_handler):
    dh = empty_data_handler
    frame_id = Handler("Frame ID", "frame_id", False)
    x1 = Handler("X1", "x1", False)
    x2 = Handler("X2", "x2", False)
    y1 = Handler("Y1", "y1", False)
    y2 = Handler("Y2", "y2", False)
    dh.add_handlers(
        frame_id,
        x1, y1,
        x2, y2
        )
    return dh


# TODO: Make the fixture itself is testable?
@pytest.fixture
def complicated_data_handler(default_data_handler):
    dh = default_data_handler

    size_handler = Handler("Size", "size", True, values="small medium big".split())
    dh.add_handlers(size_handler)

    kwargs1 = {"object_id":4, "frame_id": 10, "x1": 10, "x2": 20, "y1": 30, "y2": 40, "size": "small"}
    kwargs2 = {"object_id":4, "frame_id": 15, "x1": 13, "x2": 23, "y1": 33, "y2": 43, "size": "medium"}
    kwargs3 = {"object_id":6, "frame_id": 77, "x1": 89, "x2": 98, "y1": 11, "y2": 18, "size": "big"}
    dh.add(**kwargs1)
    dh.add(**kwargs2)
    dh.add(**kwargs3)

    return dh
