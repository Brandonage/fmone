# The interface that has to be implemented by an InPlugin


class InPlugin:
    def __init__(self):
        self.buffer = []
        pass

    def collect(self):
        pass

    def pop(self):
        pass
