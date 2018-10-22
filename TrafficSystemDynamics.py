from DataAnalyzer import DataAnalyzer
from Flow import Flow
from NumberOfCarInputStock import NumberOfCarInputStock
from NumberOfCarStock import NumberOfCarStock
from SystemDynamics import SystemDynamics


class TrafficSystemDynamics(SystemDynamics):
    def __init__(self, name, inputDataFile):
        # 여기서부터 completeness check 까지는 model generation info file 에서 읽어다가 만드는 함수 필요
        # 8 road stocks generation
        stocks = []
        for i in range(8):
            stocks.append(NumberOfCarStock("[stock] the number of cars of road " + str(i), 0, None))

        # 4 input stocks
        inputStocks = []
        for i in range(4):
            inputStocks.append(NumberOfCarInputStock("[stock] input of road " + str(i * 2), 0, None))

        # 4 flows from 4 inputs stocks to 4 road stocks & binding
        for i in range(4):
            source = i
            target = i * 2
            newFlow = Flow("[flow] input stock " + str(source) + " to stock " + str(target))
            inputStocks[source].add_output_flow(newFlow)
            stocks[target].add_input_flow(newFlow)

        # 4 flows from 4 road stocks to None & binding
        for i in range(4):
            source = i * 2 + 1
            newFlow = Flow("[flow] stock " + str(source) + " to None")
            stocks[source].add_output_flow(newFlow)

        # 4*3 flows from 4 road stocks to 4 road stocks) & binding
        for i in range(4):
            source = i * 2
            for j in range(3):
                target = (source + 1 + (j + 1) * 2) % 8
                newFlow = Flow("[flow] stock " + str(source) + " to stock " + str(target))
                stocks[source].add_output_flow(newFlow)
                stocks[target].add_input_flow(newFlow)

        # stocks binding to system dynamics
        SystemDynamics.__init__(self, name, stocks + inputStocks)
        self.initialize_input_flow_configuration(inputDataFile)
        # completeness check
        # print()
        # print("Total Completeness Check:", roadSystemDynamics.completeness_check())

    def update(self):
        '''
        for stock in self.stocks:
            stock.make_flow()
        for stock in self.stocks:
            stock.update_state()
        '''

        for i in range(8, 12):
            self.stocks[i].make_flow()
        for i in range(0, 8, 2):
            self.stocks[i].update_state()
        for i in range(0, 8, 2):
            self.stocks[i].make_flow()
        for i in range(1, 8, 2):
            self.stocks[i].update_state()
        for i in range(1, 8, 2):
            self.stocks[i].make_flow()

    def initialize_input_flow_configuration(self, input_data_files):
        # TODO: input 식 생성 후 기존 식 삭제
        analyzer = DataAnalyzer()
        input_configs = analyzer.csv_data_to_equation(input_data_files)

        input_configs = [
             [-0.000172471411178, 0.0159890490833, -0.602110974228, 11.7443492102, -124.522704423, 676.349943652,
              -1490.36861775, 648.048901187, 1470.93828307],
             [-3.17924989149e-06, 0.000284027668872, -0.00995312174726, 0.168750874386, -1.30445079083, 1.71270241657,
              28.7888271572, -78.6878691422, -39.5814038074, 338.643855421],
             [-5.81112658562e-07, 6.37419649161e-05, -0.00302446756423, 0.0813760542257, -1.36259198627, 14.5693979154,
              -97.0834098303, 364.528345285, -532.853201384, -229.367239839, 1619.15298156],
             [-3.4254423242e-07, 3.2086845451e-05, -0.00120120525597, 0.022729657215, -0.227258577962, 1.21597639486,
              -5.15912010743, 30.381515264, -66.821398373, -25.9780406881, 323.523340224]
        ]

        system_dynamics_config = []
        for i in range(12):
            if i < 8:
                system_dynamics_config.append(None)
            else:
                system_dynamics_config.append(input_configs[i - 8])

        # [ None * 8 ] + [ eq1, eq2, eq3, eq4]
        self.set_config(system_dynamics_config)
