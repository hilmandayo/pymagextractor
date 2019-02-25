# TODO: renaming this -- `d_object`?
class Object:

    def __init__(self):
        self.name = ""
        self.view_list = []

    def search_view(self, view_name):
        """Look for a view by the name"""
        for my_view in self.view_list:
            if my_view.name == view_name:
                return my_view

    def add_view(self, new_view):
        """Add new view"""
        if not self.search_view(new_view.name):
            self.view_list.append(new_view)
            self.view_list.sort(key=lambda x: x.name)
            return True
        else:
            return False

    def delete_view(self, view_selected):
        """Delete view"""
        self.view_list.remove(view_selected)

    def verify(self):
        return self.name
