from abc import *


class SystemDynamics(metaclass=ABCMeta):
    def __init__(self, name, stocks):
        self.name = name
        self.stocks = stocks

    def add_stocks(self, stock):
        """
        Add a stock to this system dynamics model.
        :param stock: stock that wanted to add to this System Dynamics model.
        :return: None.
        """
        self.stocks.append(stock)

    @abstractmethod
    def update(self):
        pass

    def get_state(self):
        """
        Get state of stocks in this system dynamics model.
        :return: the list of values of state of stock in this system dynamics model.
        """
        return [stock.get_state() for stock in self.stocks]

    def get_state30(self):
        """
        Get state of stocks in this system dynamics model.
        :return: the list of values of state of stock in this system dynamics model.
        """
        return [stock.get_state30() for stock in self.stocks]

    def get_state60(self):
        """
        Get state of stocks in this system dynamics model.
        :return: the list of values of state of stock in this system dynamics model.
        """
        return [stock.get_state60() for stock in self.stocks]

    def completeness_check(self):
        """
        Check completeness of input and output flow of stocks in this system dynamics model.
        Return False, if at least one stock doesn't have completeness, otherwise return True.
        :return: Completeness of flow of stocks in this system dynamics model.
        """
        for stock in self.stocks:
            if not stock.completeness_check():
                return False
        return True

    def set_config(self, config):
        """
        Set configuration of stocks in this system dynamics model.
        Set configuration of stock to each element of list 'config'
        :param config: list of configurations
        :return: None
        """
        for i in range(len(self.stocks)):
            self.stocks[i].set_config(config[i])

    def set_config30(self, config):
        """
        Set configuration30 of stocks in this system dynamics model.
        Set configuration30 of stock to each element of list 'config'
        :param config: list of configurations
        :return: None
        """
        for i in range(len(self.stocks)):
            self.stocks[i].set_config30(config[i])

    def set_config60(self, config):
        """
        Set configuration60 of stocks in this system dynamics model.
        Set configuration60 of stock to each element of list 'config'
        :param config: list of configurations
        :return: None
        """
        for i in range(len(self.stocks)):
            self.stocks[i].set_config60(config[i])
