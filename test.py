from copy import deepcopy

from DataAnalyzer import DataAnalyzer
from TrafficEnvGAEngine import TrafficEnvGAEngine
from TrafficSystemDynamics import TrafficSystemDynamics


def criteria_data_generation():
    """
    Generate a target data for GA from a traffic data file.
    Get equation from files and get target data from that equation.
    :return: List of lists that includes target data for GA
    """
    data_analyzer = DataAnalyzer()
    equation = data_analyzer.csv_data_to_equation(["data/g_after_up.csv", "data/g_before_up.csv", "data/g_before_down.csv", "data/g_after_down.csv",
                                                   "data/p_after_up.csv", "data/p_before_up.csv", "data/p_before_down.csv", "data/p_after_down.csv"])

    total_goal = []
    for e in equation:
        goal = []
        for t in range(24):
            set_variable = 0
            for c in range(len(e)):
                set_variable = set_variable + e[-1 - c] * (t ** c)
            goal.append(set_variable)
        total_goal.append(goal)

    return total_goal


input_data = ["data/g_after_up.csv", "data/g_before_down.csv", "data/p_after_up.csv", "data/p_before_down.csv"]
output_data = ["data/g_before_up.csv", "data/g_after_down.csv", "data/p_before_up.csv", "data/p_after_down.csv"]

# traffic system dynamics generation
print("====== model generation =====")
traffic_system_dynamics = TrafficSystemDynamics("traffic system dynamics", input_data)
if not traffic_system_dynamics.completeness_check():
    print('Generated model is not complete')
else:
    print('Generated model is complete')

# showing criteria data
print("\n\n====== showing goal data =====")
print("goal data")
goal = criteria_data_generation()
for g in goal:
    print(g)
print()
print("error in the original data")
print([abs((goal[0][i]+goal[2][i]+goal[4][i]+goal[6][i])-(goal[1][i]+goal[3][i]+goal[5][i]+goal[7][i]))/4 for i in range(24)])

# GA engine generation and search
print("\n\n====== Genetic Algorithm =====")
GA = TrafficEnvGAEngine("GA_config.txt", traffic_system_dynamics)
states, errors = GA.search(output_data)
print("states")
states = [list(i) for i in zip(*states)]
for s in states[:8]:
    print(s)
print()
print("error in the searched model")
print(errors)

data_analyzer = DataAnalyzer()
data_analyzer.show_equation_on_graph(data_analyzer.csv_data_to_equation(output_data))