from views.display_view import DisplayView


class DisplayController:

    def __init__(self, home_controller):
        self.home_controller = home_controller
        self.view = DisplayView(self)

    def run(self):
        self.view.show()
