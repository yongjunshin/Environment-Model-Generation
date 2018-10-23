class SystemDynamicsGene:
    def __init__(self, sd, representation):
        self.sd = sd
        self.representation = representation
        self.set_representation(self.representation)

    def get_representation(self):
        """
        Get Configurations of stocks in this system dynamics
        :return: List of configurations of stock in system dynamics of this gene.
        """
        return [stock.get_config() for stock in self.sd.stocks]

    def set_representation(self, representation):
        """
        Set representation of this Gene.
        And set configurations of stock in system dynamics of this gene based on this representation
        :param representation: List of configurations of stock
        :return: None.
        """
        self.representation = representation
        self.sd.set_config(self.representation)
