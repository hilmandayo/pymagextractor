notation.values


    def save(self):
        with open(str(self._path), "w") as f:
            toml.dump(self._anns, f)



class AnnotationSetting:
    def __init__(self, name: str, annotation: dict):
        self._ann = annotation
        self._name = name

    def __str__(self):
        s = "Object: '{}'\nViews: {}\n"
        ret = ""
        for k, v in self._ann.items():
            ret += s.format(k, v)
        return ret.strip()

    @property
    def name(self):
        return self._name

    @property
    def values(self):
        return self._ann

    def add(self, key, values):
        # TODO: Repair this... what if None is passed?
        v = self._ann.get(key, None)
        if v is None:
            v = []
            self._ann[key] = v
        if isinstance(values, str):
            v.append(values)
        elif isinstance(values, list):
            v.extend(values)

    def remove(self, key, values=None):
        # TODO: Repair this...
        if values is None:
            self._ann.pop(key)
        else:
            if isinstance(values, str):
                self._ann[key].remove(values)
            elif isinstance(values, list):
                for v in values:
                    self._ann[key].remove(v)
            else:
                raise ValueError
