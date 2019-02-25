# TODO: What is view?
class View:

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
