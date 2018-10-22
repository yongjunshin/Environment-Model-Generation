from copy import deepcopy
from TrafficEnvGAEngine import TrafficEnvGAEngine
from TrafficSystemDynamics import TrafficSystemDynamics


def criteria_data_generation():
    equation = [
     [-0.000172471411178, 0.0159890490833, -0.602110974228, 11.7443492102, -124.522704423, 676.349943652,
      -1490.36861775, 648.048901187, 1470.93828307],
     [-1.00308443955e-06, 0.000109319671245, -0.00511030917602, 0.134225942574, -2.17652896364, 22.4438785859,
      -144.621055537, 532.931223015, -818.252752483, -135.884983131, 1687.82024869],
     [-3.17924989149e-06, 0.000284027668872, -0.00995312174726, 0.168750874386, -1.30445079083, 1.71270241657,
      28.7888271572, -78.6878691422, -39.5814038074, 338.643855421],
     [3.70204557043e-07, -4.30527893412e-05, 0.00207358064481, -0.0530091207001, 0.759046553612, -5.72292919652,
      15.6502621843, 43.4033809984, -251.353170233, 211.970138972, 185.741847391],
     [-5.81112658562e-07, 6.37419649161e-05, -0.00302446756423, 0.0813760542257, -1.36259198627, 14.5693979154,
      -97.0834098303, 364.528345285, -532.853201384, -229.367239839, 1619.15298156],
     [-6.81077097341e-07, 7.05429933723e-05, -0.00312725239443, 0.0786490224715, -1.26071509318, 13.651295323,
      -99.5380490007, 436.79472203, -807.739766424, 63.9682286788, 1491.71184382],
     [-3.4254423242e-07, 3.2086845451e-05, -0.00120120525597, 0.022729657215, -0.227258577962, 1.21597639486,
      -5.15912010743, 30.381515264, -66.821398373, -25.9780406881, 323.523340224],
     [1.10815138667e-06, -0.000127221738881, 0.00611596653591, -0.159159351009, 2.41585005985, -21.3919198483,
      103.592131637, -232.82263525, 188.347476486, -78.1087346542, 400.365041013]
    ]

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


# TODO: 데이터 파일명 수정
input_data = ["data0.csv, data2.csv, data4.csv, data6.csv"]
output_data = ["data1.csv, data3.csv, data5.csv, data6.csv"]

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
# TODO: ga_config_file_to_values 구현 후 파라미터 수정
GA = TrafficEnvGAEngine("GA_config.txt", 200, 10, 0.5, 0.6, 0.8, traffic_system_dynamics)
states, errors = GA.search(output_data)
print("states")
states = [list(i) for i in zip(*states)]
for s in states[:8]:
    print(s)
print()
print("error in the searched model")
print(errors)
