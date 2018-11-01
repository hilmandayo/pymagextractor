class Object:

    def __init__(self):
        self.name = ""
        self.front = ""
        self.back = ""

    def verify(self):
        return self.name and (self.front or self.back)
