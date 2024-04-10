
class App():
    def __init__(self, id):
        self.id = id

    def __doc__(self):
        return f"Mi app instance: {self.id}"
