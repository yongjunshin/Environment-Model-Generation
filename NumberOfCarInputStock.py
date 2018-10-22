from Stock import Stock


class NumberOfCarInputStock(Stock):
    def __init__(self, name, initial_value, output_flow_config):
        Stock.__init__(self, name, initial_value)
        self.outputFlowConfig = output_flow_config
        self.time = 0

    def make_flow(self):
        set_variable = 0
        for i in range(len(self.outputFlowConfig)):
            set_variable = set_variable + self.outputFlowConfig[-1-i]*(self.time**i)

        for output in self.outputFlow:
            output.set_state(set_variable)

        self.time = self.time + 1

    def set_config(self, config):
        if config is not None:
            self.outputFlowConfig = config

    def get_config(self):
        return self.outputFlowConfig

    def completeness_check(self):
        if len(self.outputFlow) <= 0:
            print(self.name + ': no output flow')
            return False
        # self.print_info()
        # print('completeness check -', self.name, ": True")
        return True
