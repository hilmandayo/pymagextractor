import pathlib


def create_dirs(dirs):
    if not isinstance(dirs, list):
        dirs = [dirs]

    _dirs = []
    for d in dirs:
        if isinstance(d, str):
            d = pathlib.Path(d)
        elif isinstance(d, pathlib.Path):
            pass
        else:
            # TODO: make a better error report
            raise ValueError
        _dirs.append(d)

    for d in _dirs:
        d.mkdir(exist_ok=True)


def row_length(dict_: dict):
    """Calculate the length of `dict`'s row.

    Given a dict of dict with a fixed length of iterable as its value,
    return the iterable's length.
    """

    outer_key = list(dict_.keys())[0]
    dict_ = dict_[outer_key]
    inner_key = list(dict_.keys())[0]

    return len(dict_[inner_key])
