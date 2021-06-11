import sys
import random
from graph import Graph

import matplotlib.pyplot as plt

##########
# Inputs #
##########
N = int(sys.argv[1])
M = int(sys.argv[2])
P = 10
I = 33
random.seed(sys.argv[-1])

##############
# Processing #
##############
# Graph gen
graph = Graph(N)
graph.connect_tree()
graph.connect_tree()
temp = [i for i in range(N)]
random.shuffle(temp)
for i in temp:
    friends = int(random.normalvariate(4,2))
    while(friends > 0):
        graph.connect_grandchild(i)
        friends -= 1

# Vaccinate
candidates = {i for i in range(N)}
vaccinated = random.sample(candidates,M)

##########
# Prints #
##########
def adj_print():
    # Variables
    print(graph.nodes, graph.edges, M)
    print(P,I)

    # Vaccinated
    print(' '.join(map(str,vaccinated)))

    # Edges
    graph.print_adj()

adj_print()
#print('Source,Target')
#graph.print_edges()

#############################
# Optional degree histogram #
#############################
if sys.argv[3] == "hist":
    import numpy as np
    meow = np.array(graph.deg)
    plt.xlabel("Outdegree")
    plt.ylabel("Nodes")
    plt.title(f"Mean: {meow.mean()} Std:{meow.std()}")
    plt.hist(graph.deg)
    plt.show()
