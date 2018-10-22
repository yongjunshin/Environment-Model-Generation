from abc import *


class Stock(metaclass=ABCMeta):
    def __init__(self, name, initial_value):
        self.name = name
        self.state = initial_value
        self.inputFlow = []
        self.outputFlow = []

    @abstractmethod
    def make_flow(self):
        pass

    @abstractmethod
    def set_config(self, config):
        pass

    @abstractmethod
    def get_config(self):
        pass

    @abstractmethod
    def completeness_check(self):
        pass

    def update_state(self):
        self.state = sum([flow.get_state() for flow in self.inputFlow])

    def get_state(self):
        return self.state

    def add_input_flow(self, flow):
        self.inputFlow.append(flow)

    def add_output_flow(self, flow):
        self.outputFlow.append(flow)

    def print_info(self):
        print(self.name, ":", self.state)
        print("\tinput flow")
        for flow in self.inputFlow:
            print("\t\t"+flow.name)
        print("\toutput flow")
        for flow in self.outputFlow:
            print("\t\t" + flow.name)


