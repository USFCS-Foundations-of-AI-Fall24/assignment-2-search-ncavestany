from queue import PriorityQueue
from Graph import *

class map_state() :
    ## f = total estimated cost
    ## g = cost so far
    ## h = estimated cost to goal
    def __init__(self, location="", mars_graph=None,
                 prev_state=None, g=0,h=0):
        self.location = location
        self.mars_graph = mars_graph
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
    search_queue = PriorityQueue()
    closed_list = {}
    search_queue.put(start_state)
    ## you do the rest.


## default heuristic - we can use this to implement uniform cost search
def h1(state) :
    return 0

## you do this - return the straight-line distance between the state and (1,1)
def sld(state) :
    sqt(a^ + b2)

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
    


if __name__ == '__main__':
    # Load the graph from the MarsMap file
    mars_graph = read_mars_graph("mars_graph.txt")
    
    # Print out the nodes and their corresponding edges
    print("Graph nodes and their edges:")
    
    # Iterate over the adjacency list
    # for node, edges in mars_graph.g.items():
    #     print(f"Node {node}:")
    #     for edge in edges:
    #         print(f"  {edge}")
    
    print(mars_graph.get_edges("1,1"))

