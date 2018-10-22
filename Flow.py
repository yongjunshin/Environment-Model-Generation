class Flow:
    def __init__(self, name):
        self.name = name
        self.state = 0

    def set_state(self, value):
        self.state = value

    def get_state(self):
        return self.state
