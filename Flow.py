class Flow:
    def __init__(self, name):
        self.name = name
        self.state = 0
        self.state30 = 0
        self.state60 = 0

    def set_state(self, value):
        """
        Set state of this flow to a given value
        :param value: value
        :return: None.
        """
        self.state = value

    def set_state30(self, value):
        """
        Set state30 of this flow to a given value
        :param value: value
        :return: None.
        """
        self.state30 = value

    def set_state60(self, value):
        """
        Set state60 of this flow to a given value
        :param value: value
        :return: None.
        """
        self.state60 = value

    def get_state(self):
        """
        return value of state of this flow
        :return: the state of this flow
        """
        return self.state

    def get_state30(self):
        """
        return value of state of this flow
        :return: the state of this flow
        """
        return self.state30

    def get_state60(self):
        """
        return value of state of this flow
        :return: the state of this flow
        """
        return self.state60
