from pymagextractor.gui.views.widgets import BoundingBoxesViewer
import pytest
import numpy as np


@pytest.mark.skip("Need to repair this test")
def test_gui_add_image(bb_viewer):
    bbv, qtbot = bb_viewer

    info = {"track_id": 0, "frame_id": 0}
    image = np.zeros([100, 100], np.uint8)

    bbv.add_image(image, info, 0)

@pytest.mark.skip("Need to repair this test")
def test_gui_add_images_row(bb_viewer, np_array_images_seven):
    bbv, qtbot = bb_viewer
    arrys = np_array_images_seven

    info_list = []
    for i in range(7):
        info = {"track_id": i, "frame_id": i + 3}
        info_list.append(info)

    bbv.add_images_row(arrys[:3], info_list[:3])
    bbv.add_images_row(arrys[3:5], info_list[3:5])
    bbv.add_images_row(arrys[5:], info_list[5:])
