from pymagextractor.models.sessions import ObjectSelect


def test_object_object_id(empty_data_handler):
    dh = empty_data_handler
    os_1 = ObjectSelect(dh)
    os_2 = ObjectSelect(dh)

    assert os_1.object_id == 1
    assert os_2.object_id == 2
