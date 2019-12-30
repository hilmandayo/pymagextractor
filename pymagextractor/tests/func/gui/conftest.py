from pymagextractor.gui.views.widgets import BoundingBoxesViewer
import pytest
import numpy as np

@pytest.fixture(scope="function")
def bb_viewer(qtbot):
    bbv = BoundingBoxesViewer()
    qtbot.addWidget(bbv)
    return bbv, qtbot


@pytest.fixture(scope="session")
def np_array_images_seven():
    arrays = []
    for i in range(7):
        arrays.append(np.zeros([300, 300, 3], np.uint8))

    return arrays
