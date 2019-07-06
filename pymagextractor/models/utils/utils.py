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

    for d in _dirs:
        d.mkdir()
