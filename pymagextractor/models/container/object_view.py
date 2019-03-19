# TODO: What is view?
"""Represent the image of one of the views of an object saved. For example there is an object you want to save: a car,
so for the car there are many views, front view, back view, side view e etc"""


class ObjectView:
    def __init__(self, t_object):
        self.belong = t_object
        self.name = ""
        self.path = ""

    def verify(self):
        # it must has a name and a path
        if (not self.name) or (not self.path):
            print("missing")
            return False
        # verify name
        name_verify = True  # the name must be unique
        for object_view in self.belong.view_list:
            if self.name == object_view.name:
                name_verify = False
                print("name problem")

        return name_verify
