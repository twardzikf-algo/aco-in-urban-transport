# Ant Colony Optimization Algorithm for Urban Transport Simulation

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-no-red.svg)](https://github.com/twardzikf/ecnp-simulation/graphs/commit-activity)

## Description

This project implements an [ACO](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms) algortihm to simulate an optimal vehicle load distribution in a street network. Different setup configurations show the abilities of the system to find alternative solutions when a street is closed as well as to find better solutions when a current one is no longer optimal.

## Configuration

Simulation setup is realised in experimentc.py file which contains apropriate method calls to carry out the simulation as well as quite many ready setups as python dictionaries with following control attributes:

- *ant_number*: amount of ants on the graph
- *node_number*: number of nodes in the graph
- *steps*: amount of steps of simulation
- *src_nodes*: list of start nodes for ants
- *dest_nodes*: list of target nodes for ants
- *alpha*: importance of pheromones in heuristics: 
        pheromone^alpha
- *beta*:  importance of difference of overload in heuristics: 
        costs = base_cost(curvol-maxvol)^beta
- *gamma*: importance of overall cost in heuristic: 
        pheromone^alpha/costs^gamma
- *enhancement_rate*: with which rate are the pheromones enhanced/being laid/how to call it:
        pheromone = pheromone*( 1 + ((maxvol-curvol)/maxvol)*enhancement_rate )
- *evaporation_rate*: with which rate do pheromones evaporate:
        pheromone = pheromone*(1 - evaporation_rate)

- *edges*: list of edges as tupels, works only if custom_graph == True
- *costs*: list of costs: graph_data['costs'][from][to], 
        works only if custom_weights == True
- *max_vols*: list of maximum volumes of edges graph_data['max_vols'][from][to],
        works only if custom_weights == True


**Libraries used: [matplotlib](https://github.com/matplotlib/matplotlib), [networkx](https://github.com/networkx), [numpy](http://www.numpy.org/)**
