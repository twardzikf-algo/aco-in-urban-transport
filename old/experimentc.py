from graph import Graph
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
"""
parameters:
    ant_number: amount of ants on the graph
    node_number: number of nodes in the graph
        !!! in case of ladder graph its already halved up, so here
        the actual number of nodes is meant
    steps: amount of steps of simulation

    src_nodes: list of start nodes for ants
    dest_nodes: list of target nodes for ants

    alpha: importance of pheromones in heuristics: 
        pheromone^alpha
    beta:  importance of difference of overload in heuristics: 
        costs = base_cost(curvol-maxvol)^beta
    gamma: importance of overall cost in heuristic: 
        pheromone^alpha/costs^gamma
    enhancement_rate: with which rate are the pheromones enhanced/being laid/how to call it:
        pheromone = pheromone*( 1 + ((maxvol-curvol)/maxvol)*enhancement_rate )
    evaporation_rate: with which rate do pheromones evaporate:
        pheromone = pheromone*(1 - evaporation_rate)

    edges: list of edges as tupels, works only if custom_graph == True
    costs: list of costs: graph_data['costs'][from][to], 
        works only if custom_weights == True
    max_vols: list of maximum volumes of edges graph_data['max_vols'][from][to],
        works only if custom_weights == True

"""
def getOptimalParameter():
    resolution = 10
    X = []
    Y = []
    Z = []
    A = np.zeros((resolution, resolution))
    for enhancement in range(resolution):
        for evap in range(resolution):
            parameters = {
                'file_name': "example1.png",
                'custom_graph': True,
                'custom_weights': True,
                'ant_number': 1,
                'node_number': 9,
                'steps': 100,
                'src_nodes': [0],
                'dst_nodes': [8],
                'init_pheromon': 1,
                'alpha': 1,
                'beta': 1,
                'gamma': 1,
                'enhancement_rate': enhancement / resolution,
                'evaporation_rate': evap / (resolution * 10),

                'edges': [(0, 1), (0, 2), (1, 3), (1, 4), (2, 4), (2, 5), (3, 6), (4, 6), (4, 7), (6, 8), (7, 8)],
                'edges_to_reset': [],
                'step_to_reset': -1,
                'costs': {0: {0: 1, 1: 2, 2: 10, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
                          1: {0: 2, 1: 1, 2: 0, 3: 1, 4: 2, 5: 0, 6: 0, 7: 0, 8: 0},
                          2: {0: 10, 1: 0, 2: 1, 3: 0, 4: 10, 5: 10, 6: 0, 7: 0, 8: 0},
                          3: {0: 0, 1: 3, 2: 0, 3: 1, 4: 0, 5: 0, 6: 1, 7: 0, 8: 0},
                          4: {0: 0, 1: 2, 2: 10, 3: 0, 4: 1, 5: 0, 6: 10, 7: 2, 8: 0},
                          5: {0: 0, 1: 0, 2: 10, 3: 0, 4: 0, 5: 1, 6: 0, 7: 0, 8: 0},
                          6: {0: 0, 1: 0, 2: 0, 3: 1, 4: 10, 5: 0, 6: 1, 7: 0, 8: 10},
                          7: {0: 0, 1: 0, 2: 0, 3: 0, 4: 2, 5: 0, 6: 0, 7: 1, 8: 2},
                          8: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 10, 7: 2, 8: 1}},

                'max_vols': {0: {0: 1, 1: 2, 2: 10, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
                             1: {0: 2, 1: 1, 2: 0, 3: 1, 4: 2, 5: 0, 6: 0, 7: 0, 8: 0},
                             2: {0: 10, 1: 0, 2: 1, 3: 0, 4: 10, 5: 10, 6: 0, 7: 0, 8: 0},
                             3: {0: 0, 1: 3, 2: 0, 3: 1, 4: 0, 5: 0, 6: 1, 7: 0, 8: 0},
                             4: {0: 0, 1: 2, 2: 10, 3: 0, 4: 1, 5: 0, 6: 10, 7: 2, 8: 0},
                             5: {0: 0, 1: 0, 2: 10, 3: 0, 4: 0, 5: 1, 6: 0, 7: 0, 8: 0},
                             6: {0: 0, 1: 0, 2: 0, 3: 1, 4: 10, 5: 0, 6: 1, 7: 0, 8: 10},
                             7: {0: 0, 1: 0, 2: 0, 3: 0, 4: 2, 5: 0, 6: 0, 7: 1, 8: 2},
                             8: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 10, 7: 2, 8: 1}}
            }

            graph = Graph(parameters)
            graph.performSimulation()
            X.append(evap)
            Y.append(enhancement)
            Z.append(graph.getSolution())
            A[evap, enhancement] = graph.getSolution()
    index = np.unravel_index(np.argmin(A, axis=None), A.shape)
    print(index[0] / (resolution * 10), index[1] / resolution)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(X, Y, Z, linewidth=0.2, antialiased=True)
    plt.show()
    return (index[0] / (resolution * 10)+0.1, index[1] / resolution + 0.01)

def performExperimentc(evap=0.01, enhancement=0.2):
    parameters = {
        'file_name': "example1.png",
        'verbose': True,
        'custom_graph': True,
        'custom_weights': True,
        'ant_number': 100,
        'node_number': 9,
        'steps': 100,
        'src_nodes': [0],
        'dst_nodes': [8],
        'init_pheromon': 1,
        'alpha': 1,
        'beta': 1,
        'gamma': 1,
        'enhancement_rate': enhancement,
        'evaporation_rate': evap ,

        'edges': [(0, 1), (0, 2), (1, 3), (1, 4), (2, 4), (2, 5), (3, 6), (4, 6), (4, 7), (6, 8), (7, 8)],
        'edges_to_reset': [],
        'step_to_reset': -1,
        'costs': {0: {0: 1, 1: 2, 2: 10, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
                  1: {0: 2, 1: 1, 2: 0, 3: 1, 4: 2, 5: 0, 6: 0, 7: 0, 8: 0},
                  2: {0: 10, 1: 0, 2: 1, 3: 0, 4: 10, 5: 10, 6: 0, 7: 0, 8: 0},
                  3: {0: 0, 1: 3, 2: 0, 3: 1, 4: 0, 5: 0, 6: 1, 7: 0, 8: 0},
                  4: {0: 0, 1: 2, 2: 10, 3: 0, 4: 1, 5: 0, 6: 10, 7: 2, 8: 0},
                  5: {0: 0, 1: 0, 2: 10, 3: 0, 4: 0, 5: 1, 6: 0, 7: 0, 8: 0},
                  6: {0: 0, 1: 0, 2: 0, 3: 1, 4: 10, 5: 0, 6: 1, 7: 0, 8: 10},
                  7: {0: 0, 1: 0, 2: 0, 3: 0, 4: 2, 5: 0, 6: 0, 7: 1, 8: 2},
                  8: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 10, 7: 2, 8: 1}},

        'max_vols': {0: {0: 1, 1: 2, 2: 10, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
                     1: {0: 2, 1: 1, 2: 0, 3: 1, 4: 2, 5: 0, 6: 0, 7: 0, 8: 0},
                     2: {0: 10, 1: 0, 2: 1, 3: 0, 4: 10, 5: 10, 6: 0, 7: 0, 8: 0},
                     3: {0: 0, 1: 3, 2: 0, 3: 1, 4: 0, 5: 0, 6: 1, 7: 0, 8: 0},
                     4: {0: 0, 1: 2, 2: 10, 3: 0, 4: 1, 5: 0, 6: 10, 7: 2, 8: 0},
                     5: {0: 0, 1: 0, 2: 10, 3: 0, 4: 0, 5: 1, 6: 0, 7: 0, 8: 0},
                     6: {0: 0, 1: 0, 2: 0, 3: 1, 4: 10, 5: 0, 6: 1, 7: 0, 8: 10},
                     7: {0: 0, 1: 0, 2: 0, 3: 0, 4: 2, 5: 0, 6: 0, 7: 1, 8: 2},
                     8: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 10, 7: 2, 8: 1}}
    }

    graph = Graph(parameters)
    graph.performSimulation()
    #graph.showStats()
    graph.showGraph()

performExperimentc()