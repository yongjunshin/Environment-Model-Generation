import numpy as np
import csv
import matplotlib.pyplot as plt


class DataAnalyzer:
    def __init__(self):
        pass

    def csv_data_to_equation(self, files):
        """
        read files and return equation lists
        :param files: list of file names
        :return: list of equation constants list
        """
        equations = []
        for data_file in files:
            data_list = open(data_file, 'r')
            csv_reader = csv.reader(data_list)

            data_set = np.array([])
            time_set = np.array([])

            for line in csv_reader:
                if int(line[0]) < 6:
                    for i in range(24):
                        sss = line[i + 1].replace(',', '')
                        if sss != '-' and sss != '':
                            data_set = np.append(data_set, [int(sss)])
                            time_set = np.append(time_set, [i])

            LIMIT = 10
            DIV = 5
            tot_point = [0] * LIMIT

            for i in range(DIV):
                test_from = int(i * len(time_set) / DIV)
                test_to = int((i + 1) * len(time_set) / DIV)

                time_training = np.append(time_set[:test_from], time_set[test_to:])
                data_training = np.append(data_set[:test_from], data_set[test_to:])

                time_test = time_set[test_from:test_to]
                data_test = data_set[test_from:test_to]

                for i in range(LIMIT):
                    coeffs = np.polyfit(time_training, data_training, i + 1)
                    p = np.poly1d(coeffs)

                    yhat = p(time_test)
                    ssres = np.sum((data_test - yhat) ** 2)

                    tot_point[i] += ssres

            target = tot_point.index(np.min(tot_point))

            equations.append(np.polyfit(time_set, data_set, target + 1))

        return equations

    def show_equation_on_graph(self, equation):
        """
        draw given equation on graph and show the graph
        :param equation: list of equation constants in decreasing order of degree
        :return: None, pop up a graph
        """
        x = []
        i = 1
        while i <= 23:
            x.append(i)
            i += 0.05
        for single_equation in equation:
            d_function = np.poly1d(single_equation)
            y = d_function(x)
            plt.plot(x, y)
        plt.show()
