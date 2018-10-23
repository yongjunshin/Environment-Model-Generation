from Stock import Stock


class NumberOfCarStock(Stock):
    def __init__(self, name, initial_value, output_flow_config):
        Stock.__init__(self, name, initial_value)
        self.outputFlowConfig = output_flow_config

    def make_flow(self):
        """
        Make an output flow based on this stock's output configuration
        :return: None
        """
        for i in range(len(self.outputFlow)):
            set_variable = self.state * (self.outputFlowConfig[i]/sum(self.outputFlowConfig))
            self.outputFlow[i].set_state(set_variable)

    def set_config(self, config):
        """
        Set configuration to a given configuration.
        :param config: configuration that
        :return: None
        """
        if config is not None:
            self.outputFlowConfig = config

    def get_config(self):
        """
        Returns output configuration of this Stock
        :return: Output Configuration of this Stock
        """
        return self.outputFlowConfig

    def completeness_check(self):
        """
        Check completeness of output flow of this stock.
        Return False, if there is 0 or less elements in both input and outputFlow, otherwise return True.
        :return: Completeness of both input and output flow of this stock.
        """
        if len(self.inputFlow) <= 0:
            print(self.name + ': no input flow')
            return False
        if len(self.outputFlow) <= 0:
            print(self.name + ': no output flow')
            return False
        # self.print_info()
        # print('completeness check -', self.name, ": True")
        return True
