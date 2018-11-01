from views.display_view import DisplayView


class DisplayController:

    def __init__(self, home_controller):
        self.view = DisplayView(self)
        self.home_controller = home_controller

    def run(self):
        self.view.show()
