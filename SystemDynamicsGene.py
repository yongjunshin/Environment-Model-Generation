class SystemDynamicsGene:
    def __init__(self, sd, representation):
        self.sd = sd
        self.representation = representation
        self.set_representation(self.representation)

    def get_representation(self):
        return [stock.get_config() for stock in self.sd.stocks]

    def set_representation(self, representation):
        self.representation = representation
        self.sd.set_config(self.representation)
