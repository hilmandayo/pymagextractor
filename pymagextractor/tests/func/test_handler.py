from pymagextractor.models.data_handler import Handler
import pytest


@pytest.mark.parametrize("name, ref, button", [("Track ID", "track_id", None),
                                               ("Frame ID", "frame_id", False),
                                               ("X1", "x1", True),
                                               ("Y1", "y1", True)])
def test_handler_inits(name, ref, button):
    if button is None:
        handler = Handler(name, ref)
        button = False
    else:
        handler = Handler(name, ref, button)

    h = handler
    assert (h.name, h.ref, h.button) == (name, ref, button)
