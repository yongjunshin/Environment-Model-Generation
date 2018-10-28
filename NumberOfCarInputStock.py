from Stock import Stock


class NumberOfCarInputStock(Stock):
    def __init__(self, name, initial_value, output_flow_config):
        Stock.__init__(self, name, initial_value)
        self.outputFlowConfig = output_flow_config
        self.time = 0
        self.time30 = 0
        self.time60 = 0

    def make_flow(self):
        """
        Make an output flow based on this stock's output configuration
        :return: None
        """
        set_variable = 0
        for i in range(len(self.outputFlowConfig)):
            set_variable = set_variable + self.outputFlowConfig[-1-i]*(self.time**i)

        for output in self.outputFlow:
            output.set_state(set_variable)

        self.time = self.time + 1

    def make_flow30(self):
        """
        Make an output flow based on this stock's output configuration
        :return: None
        """
        set_variable = 0
        for i in range(len(self.outputFlowConfig)):
            set_variable = set_variable + self.outputFlowConfig[-1-i]*(self.time30**i)

        for output in self.outputFlow:
            output.set_state30(set_variable)

        self.time30 = self.time30 + 1

    def make_flow60(self):
        """
        Make an output flow based on this stock's output configuration
        :return: None
        """
        set_variable = 0
        for i in range(len(self.outputFlowConfig)):
            set_variable = set_variable + self.outputFlowConfig[-1-i]*(self.time60**i)

        for output in self.outputFlow:
            output.set_state60(set_variable)

        self.time60 = self.time60 + 1

    def set_config(self, config):
        """
        Set configuration to a given configuration.
        :param config: configuration that
        :return: None
        """
        if config is not None:
            self.outputFlowConfig = config

    def set_config30(self, config):
        """
        Set configuration to a given configuration.
        :param config: configuration that
        :return: None
        """
        if config is not None:
            print(config)
            self.outputFlowConfig = config

    def set_config60(self, config):
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
        Return False, if there is 0 or less elements in outputFlow, otherwise return True.
        :return: Completeness of output flow of this stock.
        """
        if len(self.outputFlow) <= 0:
            print(self.name + ': no output flow')
            return False
        # self.print_info()
        # print('completeness check -', self.name, ": True")
        return True
