import networkx as nx
from math import ceil
import matplotlib.pyplot as plt
from ant import Ant
import numpy as np

"""[IN PROGRESS]"""
"""
[TODO] ceate and print heatmaps, first think how to perform many simulations, maybe extract this functionality 
       somewhere else
       
[TODO]     

[TODO] save data as csv, save graph as png
"""

class Graph:
    """
    Class realizing ACO algorithm on the graph
    
    Attributes:
        - ants: ant colony as a list of Ant objects
        - graph_data: all data about nodes & edges as a dict
        - graph: graph structure as networx graph
        - parameters: setup variables customizing input model
          and manipulating the behavior of the algorithm
        
    Methods:
        - evaporatePheromones(): performs global update on pheromone levels
             Is influenced by evaporation_rate included in parameters
        - performStep(): moves each ant, updates the values on the graph
             and subsequently updates pheromone levels calling evaporatePheromones()
        - performSimulation(): performs full Simulation with parameters 
             given by initialization. After simulating given number of steps
             prints the graph and optionally short summary/current state of the graph
        - showState():
             prints the current state of the graph: all edges inclusive their
             pheromone levels, costs, current and maximum capacities.
        - showGraph():
             prints the graph with edge widths dependent on pheromone level
             and brightnesses of red dependent on maximal capacities
        - showStats(): prints adges with their pheromone level in descending order,
            as well as basic stats such like avg/max/min/sum of number of passes and cost
        
    """
    ants = []

    def __init__(self, parameters):
        """
        Initialize a graph with setup parameters:
            - create a graph with given nodes and edges
            - set initial pheromone levels, costs, initial current volumes
               and maximum volumes for each edge
            - spawn given number of ants
            - set the sources and destinations for all ants
        
        Arguments: 
            - parameters: setup variables customizing input model
              and manipulating the behavior of the algorithm
           
        """
        def getGraphData():
            return { 'pheromones': {},'costs': {},'cur_vol' : {},'max_vol' : {} }

        #set up parameters and graph environment 
        self.parameters = parameters
        
        # create a predefined ladder graph  or a custom graph  with given edges
        if not self.parameters['custom_graph']:
            self.graph = nx.circular_ladder_graph( ceil(self.parameters['node_number']/2))
        else:
            self.graph = nx.Graph()
            self.graph.add_nodes_from([i for i in range(self.parameters['node_number'])])
            self.graph.add_edges_from(parameters['edges'])
            
        #self.graph.remove_edges_from(parameters['edges_to_remove'])
        
        # assign source and destination nodes to each ant
        for k in range(self.parameters['ant_number']):
            src_index = k%min(len(self.parameters['src_nodes']),self.parameters['ant_number']) if k>0 else 0
            dst_index = k%min(len(self.parameters['dst_nodes']),self.parameters['ant_number']) if k>0 else 0
            src_node = self.parameters['src_nodes'][src_index]
            dst_node = self.parameters['dst_nodes'][dst_index]
            self.ants.append(Ant(src_node, dst_node, k))
        
        self.graph_data = {k: getGraphData() for k in range(0, len(self.graph.nodes))}
        
        # assign pheromones, costs, current and maximum capacities to each edge 
        # values are predefined or given i parameters
        for node in self.graph.nodes:
            for edge in self.graph.neighbors(node):
                self.graph_data[node]['pheromones'][edge] = self.parameters['init_pheromon']
                if not self.parameters['custom_weights']:
                    self.graph_data[node]['costs'][edge] = 1
                    self.graph_data[node]['cur_vol'][edge] = 0
                    self.graph_data[node]['max_vol'][edge] = 1
                else: 
                    self.graph_data[node]['costs'][edge] = parameters['costs'][node][edge]
                    self.graph_data[node]['cur_vol'][edge] = 0
                    self.graph_data[node]['max_vol'][edge] = parameters['max_vols'][node][edge]
        
        # fill the networkx graph structure with the data stored in graph_data            
        nx.set_node_attributes(self.graph, self.graph_data)

    def evaporatePheromones(self):
        """
        Decreases pheromone level on each edge by a factor given in parameters
        """
        for u in self.graph.nodes:
            for v in self.graph.neighbors(u):
                if self.graph_data[u]['pheromones'][v] > 0 :
                    self.graph_data[u]['pheromones'][v] -= self.parameters['evaporation_rate'] * self.graph_data[u]['pheromones'][v]
                    self.graph_data[v]['pheromones'][u] -= self.parameters['evaporation_rate'] * self.graph_data[v]['pheromones'][u]


    def performStep(self):
        """
        Moves each ant, updates both graph_data and the networkx graph
        Finally decrements the number of steps left
        """
        for ant in self.ants:
            if self.parameters['steps'] == self.parameters['step_to_reset']:
                for u,v in self.parameters['edges_to_reset']:
                    self.graph_data[u]['pheromones'][v] = 0.0000001
                    self.graph_data[v]['pheromones'][u] = 0.0000001
            nx.set_node_attributes(self.graph, ant.move(self.graph_data, self.parameters))
            self.evaporatePheromones()
        self.parameters['steps'] -= 1

    def performSimulation(self):
        """
        Performs given number of steps.
        Subsequently prints the resulting graph and/or statistics, graph_data
        """
        
        if self.parameters['verbose']:
            print("=====================\nStarting simulation with parameters\n",self.parameters)
            print("=====================\nInitial Graph\n")
            self.showState()
            print("=====================")

        while self.parameters['steps'] > 0:
            if self.parameters['verbose']: print("Performing step")
            self.performStep()
            if self.parameters['verbose']: self.showState()

        if self.parameters['verbose']:
            print("=====================\nFinished Simulation\n\nResult graph:")
            self.showState()
        #self.showGraph(self.parameters['file_name'])
        #self.showState()
        #self.showStats()
        
    
    def showState(self):
        print("[graph]: current state of the graph...........................")
        for node in self.graph.nodes:
            for edge in self.graph.neighbors(node):
                # print only one direction on each edge, since its undirected graph
                if node < edge:
                    phe = self.graph_data[node]['pheromones'][edge]
                    cost = self.graph_data[node]['costs'][edge]
                    cur = self.graph_data[node]['cur_vol'][edge]
                    max = self.graph_data[node]['max_vol'][edge]
                    print("    edge (",node,",",edge,") phe: ",phe," cost: ",cost," curvol: ",cur," maxvol: ",max)

    
    def showStats(self):
        """
        
        """
        print("[graph]: statistics..............................[IN PROGRESS]")
        
        # sort edges accoridng to thier pheromone levels and print them in descending order
        r,t = [],[]
        for node in self.graph.nodes:
            for edge in self.graph.neighbors(node):
                if node < edge:
                    r.append({'from':node,'to':edge,'phe':self.graph_data[node]['pheromones'][edge]})
        
        for k in range(len(self.graph.edges())):
            max_index, max_elem = 0, r[0]
            for i in range(len(r)):
                if( r[i]['phe'] > max_elem['phe']): 
                    max_elem = r[i]
                    max_index = i
            t.append(max_elem)
            del(r[max_index])
            
        # print basic descriptive statistics
        for i in range(len(t)):
            print("    edge (",t[i]['from'],",",t[i]['to'],") phe: ",t[i]['phe'])
        print()
        for ant in self.ants:
            print("    ant nr: ",ant.number," src: ",ant.src_node," dst: ",ant.dst_node," cost: ",ant.cost_sum)
            plt.subplot(int(np.sqrt(len(self.ants))), int(len(self.ants)/np.sqrt(len(self.ants)))+1,ant.number+1)
            plt.plot(range(len(ant.passes)), ant.passes)
        all_costs = [ np.mean(ant.passes) if len(ant.passes)>0 else 1 for ant in self.ants]
        plt.show()
        print()
        print("    sum: ",sum(all_costs)," avg: ",np.mean(all_costs)," min: ",min(all_costs)," max: ",max(all_costs))

    def getSolution(self):
        return np.mean([ np.median(ant.passes) for ant in self.ants if len(ant.passes) > 0])

    def showGraph(self, file_name = ""):
        """
        prints the graph with variable widths accoridng to pheromone levels
        In addition optionally saves the graph as .png to a file, if a non empty 
        name for the file is given
        """
        
        # prepare edges and weights for visualization
        edges = self.graph.edges()
        weights = [self.graph_data[u]['pheromones'][v] for u,v in edges]
        weights_sum = sum(weights)
        weights = [ (w/weights_sum)*50 for w in weights]
        
        # prepare different shades of red to be used to optionally differentiate
        # between edges with different costs
        # to show more informatiion on the same graph
        colors = []
        max_cost = max([self.graph_data[u]['costs'][v] for u,v in edges])
        for u,v in edges:
            if self.graph_data[u]['costs'][v] <= max_cost/32:
                colors.append('#ff7f7f')
                continue
            if self.graph_data[u]['costs'][v] <= max_cost/16:
                colors.append('#ff6666')
                continue
            if self.graph_data[u]['costs'][v] <= max_cost/8:
                colors.append('#ff4c4c')
                continue
            if self.graph_data[u]['costs'][v] <= max_cost/4:
                colors.append('#ff3232')
                continue
            if self.graph_data[u]['costs'][v] <= max_cost/2:
                colors.append('#ff1919')
                continue
            if self.graph_data[u]['costs'][v] <= max_cost:
                colors.append('#ff0000')
                continue
                
        # print the graph 
        pos=nx.circular_layout(self.graph)
        nx.draw( self.graph,pos=pos,node_size=200,node_color='#A8A8A8', with_labels=True,edges=edges, edge_color=colors,edge_cmap=plt.cm.Blues, width=weights)
        if file_name != "":
            path = "img/"+file_name
            plt.savefig(path, format="PNG")
        plt.show()