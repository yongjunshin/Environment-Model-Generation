from Stock import Stock


class NumberOfCarStock(Stock):
    def __init__(self, name, initial_value, output_flow_config):
        Stock.__init__(self, name, initial_value)
        self.outputFlowConfig = output_flow_config

    def make_flow(self):
        for i in range(len(self.outputFlow)):
            set_variable = self.state * (self.outputFlowConfig[i]/sum(self.outputFlowConfig))
            self.outputFlow[i].set_state(set_variable)

    def set_config(self, config):
        if config is not None:
            self.outputFlowConfig = config

    def get_config(self):
        return self.outputFlowConfig

    def completeness_check(self):
        if len(self.inputFlow) <= 0:
            print(self.name + ': no input flow')
            return False
        if len(self.outputFlow) <= 0:
            print(self.name + ': no output flow')
            return False
        # self.print_info()
        # print('completeness check -', self.name, ": True")
        return True
