from queue import PriorityQueue
from Graph import *
from math import sqrt

class map_state() :
    ## f = total estimated cost
    ## g = cost so far
    ## h = estimated cost to goal
    def __init__(self, location="", mars_graph=None,
                 prev_state=None, g=0,h=0):
        self.location = location
        self.mars_graph = read_mars_graph("mars_graph.txt")
        self.prev_state = prev_state
        self.g = g
        self.h = h
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.location == other.location

    def __hash__(self):
        return hash(self.location)

    def __repr__(self):
        return "(%s)" % (self.location)

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def is_goal(self):
        return self.location == '1,1'


def a_star(start_state, heuristic_fn, goal_test, use_closed_list=True) :
    search_queue = PriorityQueue() # Stores nodes ordered by their f values
    closed_list = {}
    search_queue.put(start_state) 
    state_count = 0
    
    if use_closed_list:
        closed_list[start_state] = True # Add the start state to the closed list so we don't revisit
        
    while not search_queue.empty():
        current_state = search_queue.get() # Get the node with the lowest f value
        
        if goal_test(current_state):
            print("Goal found!")
            print("Total states: ", state_count)
            return current_state
        else:
            # Get all neighboring edges of the current state
            edges = current_state.mars_graph.get_edges(current_state.location) 
            successors = [] # Store the neighbors of the current state
            
            for edge in edges:
                # Create a new map state for each neighbor
                neighbor_state = map_state(location=edge.dest,
                                           mars_graph=current_state.mars_graph, 
                                           prev_state=current_state, 
                                           g=current_state.g + 1) # Since the edges are unweighted, we increment the cost by a constant 1
                
                neighbor_state.h = heuristic_fn(neighbor_state) # Calculate the heuristic value, which will be SLD
                neighbor_state.f = neighbor_state.g + neighbor_state.h # Calculate the total cost
                
                successors.append(neighbor_state)
                
            state_count += len(successors) # Increment the amount of states found
            
            # Filter out the states that have already been visited if we are using a closed list
            if use_closed_list:
                successors = [item for item in successors if item not in closed_list]
            
            for successor in successors:
                if successor not in closed_list:
                    search_queue.put(successor) # Add the successor to the priority queue
                    if use_closed_list:
                        closed_list[successor] = True # Mark the state as visited if we are using a closed list
    print("Goal not found.")                    
    return None
                    

## default heuristic - we can use this to implement uniform cost search
def h1(state) :
    return 0

## you do this - return the straight-line distance between the state and (1,1)
def sld(state) :
    loc = state.location.split(",")
    return sqrt((int(loc[0]) - 1)**2 + (int(loc[1]) - 1)**2) # SLD between the current location and the goal (1,1)

## you implement this. Open the file filename, read in each line,
## construct a Graph object and assign it to self.mars_graph().
def read_mars_graph(filename):
    mars_graph = Graph()
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            elements = line.strip().split(": ") # Split by colon to get the source and destinations separate
            src = elements[0]
            
            if src not in mars_graph.g:
                mars_graph.add_node(src)
                
            if len(elements) > 1: # If there are adjacent nodes
                destinations = elements[1].split() # Split by space
                
                for dest in destinations:
                    if dest not in mars_graph.g:
                        mars_graph.add_node(dest)
                        
                    edge = Edge(src, dest)
                    mars_graph.add_edge(edge)             
    return mars_graph 

def goal_test(state) :
    return state.location == "1,1"

if __name__ == '__main__':
    start = map_state(location="8,8", h=sld(map_state(location="8,8"))) # h is the SLD between the start and the goal
    
    result = a_star(start, sld, goal_test)
    
    if result:
        print("Path found!")
    else:
        print("No path found.")