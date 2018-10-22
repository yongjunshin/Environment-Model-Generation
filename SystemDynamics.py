from abc import *

class SystemDynamics(metaclass=ABCMeta):
    def __init__(self, name, stocks):
        self.name = name
        self.stocks = stocks

    def add_stocks(self, stock):
        self.stocks.append(stock)

    @abstractmethod
    def update(self):
        pass

    def get_state(self):
        return [stock.get_state() for stock in self.stocks]

    def completeness_check(self):
        for stock in self.stocks:
            if not stock.completeness_check():
                return False
        return True

    def set_config(self, config):
        for i in range(len(self.stocks)):
            self.stocks[i].set_config(config[i])
