from abc import *


class Stock(metaclass=ABCMeta):
    def __init__(self, name, initial_value):
        self.name = name
        self.state = initial_value
        self.state30 = initial_value
        self.state60 = initial_value
        self.inputFlow = []
        self.outputFlow = []

    @abstractmethod
    def make_flow(self):
        pass

    @abstractmethod
    def make_flow30(self):
        pass

    @abstractmethod
    def make_flow60(self):
        pass

    @abstractmethod
    def set_config(self, config):
        pass

    @abstractmethod
    def set_config30(self, config):
        pass

    @abstractmethod
    def set_config60(self, config):
        pass

    @abstractmethod
    def get_config(self):
        pass

    @abstractmethod
    def completeness_check(self):
        pass

    def update_state(self):
        """
        Update the value of state of this stock based on input flow.
        Add all values of input flow and update it to state.
        :return: None.
        """
        self.state = sum([flow.get_state() for flow in self.inputFlow])

    def update_state30(self):
        """
        Update the value of state of this stock based on input flow.
        Add all values of input flow and update it to state.
        :return: None.
        """
        self.state30 = sum([flow.get_state30() for flow in self.inputFlow])

    def update_state60(self):
        """
        Update the value of state of this stock based on input flow.
        Add all values of input flow and update it to state.
        :return: None.
        """
        self.state60 = sum([flow.get_state60() for flow in self.inputFlow])

    def get_state(self):
        """
        Return the value of state of this stock
        :return: the value of state of this stock
        """
        return self.state

    def get_state30(self):
        """
        Return the value of state of this stock
        :return: the value of state of this stock
        """
        return self.state30

    def get_state60(self):
        """
        Return the value of state of this stock
        :return: the value of state of this stock
        """
        return self.state60

    def add_input_flow(self, flow):
        """
        Add input flow to this Stock.
        :param flow: input flow that wanted to add to this stock.
        :return: None.
        """
        self.inputFlow.append(flow)

    def add_output_flow(self, flow):
        """
        Add output flow to this Stock.
        :param flow: output flow that wanted to add to this stock.
        :return: None.
        """
        self.outputFlow.append(flow)

    def print_info(self):
        """
        Print information of this stock.
        Print its name, input flows and output flows.
        :return: None. Print some lines to console.
        """
        print(self.name, ":", self.state)
        print("\tinput flow")
        for flow in self.inputFlow:
            print("\t\t"+flow.name)
        print("\toutput flow")
        for flow in self.outputFlow:
            print("\t\t" + flow.name)


