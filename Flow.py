class Flow:
    def __init__(self, name):
        self.name = name
        self.state = 0

    def set_state(self, value):
        """
        Set state of this flow to a given value
        :param value: value
        :return: None.
        """
        self.state = value

    def get_state(self):
        """
        return value of state of this flow
        :return: the state of this flow
        """
        return self.state
