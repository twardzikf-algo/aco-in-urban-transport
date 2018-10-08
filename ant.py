import numpy as np

class Ant:
    """
    Class realizing single ant functionality
    
    Attributes:
        *** operational attributes ***
        - number: oridnal number of an ant
        - node_memory: current edge in form of list of two nodes
        - src_node:  start and first target node of an ant
        - dst_node: second target node of an ant
        
        *** statistical attributes ***
        - cost_sum: statistical measure: 
        - passes: counter of times an ant reached one of its destination node
    
    Methods:
        - findNext(graph_data, parameters) -> next_node: 
            determines next node for the ant to move to
        - depositPheromones(graph_data, parameters) -> graph_data: 
            updates pheromones on the current edge and returns updated graph_data
        - move(graph_data, parameters) -> graph_data:
            moves an Ant to the next edge determined by findNext() and updated appriopriately 
            data in graph_data, finally returns updated graph_data
        - showState(): 
            prints the curruent state of an ant (all of its attributes values)
        - showFindNext(graph_data, probs, next_node): 
            prints all data relevant in context of findNext() for debugging purposes
        
    """
    def __init__(self, src_node, dst_node, number):
        
        self.number= number
        self.node_memory = [src_node,src_node]
        self.src_node = src_node
        self.dst_node = dst_node
        
        self.passes = []
        self.cost_sum = 0.0
           
    def findNext(self, graph_data, parameters):
        """
        Determines the next node for the ant to move to based 
        on the pheromones on an edge: the more pheromones the better an edge
        
        Arguments: 
            graph_data: all data about nodes & edges as a dict
            parameters: dict of all steering parameters
            
        Return:
            next_node: id of the node that has been chosen as the next to go
        """
        
        # extract pheromone values for all candidates for next_node
        pheromones = list(graph_data[self.node_memory[-1]]['pheromones'].values())
        
        # find the index of the last visited node respective to the order of the pheromones list
        if self.node_memory[0] != self.node_memory[-1] and self.node_memory[-1]!= self.dst_node :
            prev_node = list(graph_data[self.node_memory[-1]]['pheromones'].keys()).index(self.node_memory[0])
        else:    
            prev_node = -1
            
        # calculate probability for each candidate
        probs = []
        for i in range(len(pheromones)):
            if len(pheromones)==1: # if there is only one possible candidate, take it
                probs.append(1)
            elif prev_node==i: # if the candidate was visited in last move, do not take it
                probs.append(0)
            else:
                probs.append(pow(pheromones[i],parameters['alpha'])) 
                
        # convert probabilites list to an array and normalize probabilities such that their sum equals 1
        probs = np.asarray( probs )
        probs = probs/sum(probs)
        
        # determine next node for the ant to move to
        next_node = np.random.choice(list(graph_data[self.node_memory[-1]]['pheromones'].keys()), p=probs)
        #self.showFindNext(graph_data, probs, next_node)
        return next_node
    
    def depositPheromones(self, graph_data, parameters ):
        """
        Deposits pheromones on current edge
        increase factor is equal ((max_vol - cur_vol)/max_vol))*enhancement_rate 
        and is inversely proportional in current volume of an edge
        
        Arguments:
            graph_data: all data about nodes & edges as a dict
            parameters: dict of all steering parameters  
            
        Return:
            graph_data: with updated pheromone levels
        """
        # extract current and maximum capacity for current edge
        cur_vol = graph_data[self.node_memory[0]]['cur_vol'][self.node_memory[-1]]
        max_vol = graph_data[self.node_memory[0]]['max_vol'][self.node_memory[-1]]
        neighbors = len(graph_data[self.node_memory[-1]]['cur_vol'])
        
        # add costs for current edge to the overall sum  for statistics
        self.cost_sum += graph_data[self.node_memory[0]]['costs'][self.node_memory[-1]]
        
        # deposite pheromones only if there is capacity available on current edge and it is not a dead end
        if cur_vol <= max_vol and neighbors > 1:
            pheromone = graph_data[self.node_memory[0]]['pheromones'][self.node_memory[-1]]
            cost = graph_data[self.node_memory[0]]['costs'][self.node_memory[-1]] +1
            growth = (pheromone/cost)*((max_vol-cur_vol)/(max_vol+1))*parameters["enhancement_rate"]
            graph_data[self.node_memory[0]]['pheromones'][self.node_memory[-1]] += growth
            graph_data[self.node_memory[-1]]['pheromones'][self.node_memory[0]] += growth
        
        return graph_data
    
    def move(self, graph_data, parameters):
        """
        Executes the move of an ant based on the heuristics function
        
        Arguments:
            graph_data: all data about nodes & edges as a dict
            enhancement_rate: by how much should be the pheromone increase 
            after visiting an edge
            
        Return: 
            graph_data: with updated pheromon and current capacity (!) values             
        """
        nextNode = self.findNext(graph_data, parameters)
        
        # decrement current capacity on current edge only if
        # it is not initial state and capaciy is greater than zero
        if self.node_memory[-1]!=self.node_memory[0] and graph_data[self.node_memory[0]]['cur_vol'][self.node_memory[-1]] > 0:
                graph_data[self.node_memory[0]]['cur_vol'][self.node_memory[-1]] -= 1
                graph_data[self.node_memory[-1]]['cur_vol'][self.node_memory[0]] -= 1
        
        self.node_memory.append(nextNode)
        self.node_memory.pop(0)

        # update pheromones on the current edge
        graph_data = self.depositPheromones(graph_data, parameters)
        
        # increment current volume on the new current edge
        graph_data[self.node_memory[0]]['cur_vol'][self.node_memory[-1]] += 1
        graph_data[self.node_memory[-1]]['cur_vol'][self.node_memory[0]] += 1
        
        if (self.node_memory[-1] == self.dst_node ):
            self.src_node, self.dst_node = self.dst_node, self.src_node
            self.passes.append(self.cost_sum)
            self.cost_sum = 0.0

        if(parameters['verbose']):
            print("Ant ", self.number, " - took (",self.node_memory[-1],",",self.node_memory[0],")")
           
        return graph_data
    
    def showState(self):
        """
        Prints current state of an ant.
        """
        print("[ant]: current state of the ant...............................")
        print("    ant nr: ",self.number," node_memory: ", self.node_memory," src: ",self.src_node," dst: ",self.dst_node)
        
    def showFindNext(self, graph_data, probs, next_node):
        """
        Prints all data relevant in context of findNext():
            - current edge 
            - all possible adge candidates
            - their costs
            - their current and maximum volumes
            - their probabilities
            - decision that was undertaken
        
        Arguments:
            graph_data:
            probs: array of probabilites for all candidates
            next_node: the candidate chosen by findNext()
            
        """
        probs = list(probs)
        pheromones = list(graph_data[self.node_memory[-1]]['pheromones'].values())
        costs = list(graph_data[self.node_memory[-1]]['costs'].values())
        cur_vol = list(graph_data[self.node_memory[-1]]['cur_vol'].values())
        max_vol = list(graph_data[self.node_memory[-1]]['max_vol'].values())
        print("[ant]: I ( ant nr",self.number,")am at edge (",self.node_memory[0],",",self.node_memory[-1],") and I can choose between: ")
        for i in list(graph_data[self.node_memory[-1]]['pheromones'].keys()):
            print("    edge (",self.node_memory[-1],",",i,") phe: ", pheromones.pop(0)," cost: ",costs.pop(0),"cur_vol: ",cur_vol.pop(0)," max_vol: ",max_vol.pop(0)," prob: ",probs.pop(0))
        print("    I decided to take edge (",self.node_memory[-1],",",next_node,")")