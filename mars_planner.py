## actions:
## pick up tool
## move_to_sample
## use_tool
## move_to_station
## drop_tool
## drop_sample
## move_to_battery
## charge

## locations: battery, sample, station
## holding_sample can be True or False
## holding_tool can be True or False
## Charged can be True or False

from copy import deepcopy
from search_algorithms import *

class RoverState :
    def __init__(self, loc="station", sample_extracted=False, holding_sample=False, holding_tool=False, dropped_off_sample=False, charged=False, depth=0):
        self.loc = loc
        self.sample_extracted=sample_extracted
        self.holding_sample = holding_sample
        self.holding_tool = holding_tool
        self.charged=charged
        self.dropped_off_sample = dropped_off_sample # Added dropped_off_sample so we can detect if the sample has actually been dropped off
        self.depth = depth
        self.prev = None

    ## Returns true if the two states are identical
    def __eq__(self, other):
       return (self.loc == other.loc and 
               self.sample_extracted == other.sample_extracted and 
               self.holding_sample == other.holding_sample and 
               self.charged == other.charged and 
               self.holding_tool == other.holding_tool and
               self.dropped_off_sample == other.dropped_off_sample) 


    def __repr__(self):
        return (f"Location: {self.loc}\n" +
                f"Sample Extracted?: {self.sample_extracted}\n"+
                f"Holding Sample?: {self.holding_sample}\n" +
                f"Dropped Off Sample?: {self.dropped_off_sample}\n" +
                f"Charged? {self.charged}\n" +
                f"Holding Tool? {self.holding_tool}\n") 

    def __hash__(self):
        return self.__repr__().__hash__()

    def successors(self, list_of_actions):

        ## apply each function in the list of actions to the current state to get
        ## a new state.
        ## add the name of the function also
        succ = [(item(self), item.__name__) for item in list_of_actions]
        ## remove actions that have no effect

        succ = [item for item in succ if not item[0] == self]
        return succ

## our actions will be functions that return a new state.

def move_to_sample(state) :
    r2 = deepcopy(state)
    r2.loc = "sample"
    r2.prev=state
    return r2

def move_to_station(state) :
    r2 = deepcopy(state)
    r2.loc = "station"
    r2.prev = state
    return r2

def move_to_battery(state) :
    r2 = deepcopy(state)
    r2.loc = "battery"
    r2.prev = state
    return r2


def pick_up_tool(state) :
    r2 = deepcopy(state)
    r2.holding_tool = True
    r2.prev = state
    return r2

def drop_tool(state) :
    r2 = deepcopy(state)
    r2.holding_tool = False
    r2.prev = state
    return r2

def use_tool(state) :
    r2 = deepcopy(state)
    if state.holding_tool and state.loc == "sample": # Should only be able to use tool if holding tool and at the sample
        r2.sample_extracted = True
    r2.prev = state
    return r2

def pick_up_sample(state) :
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "sample": # Should only be able to pick up sample if holding tool and at the sample
        r2.holding_sample = True
    r2.prev = state
    return r2

def drop_sample(state) :
    r2 = deepcopy(state)
    if state.holding_sample and state.loc == "station":
        r2.holding_sample = False
        r2.dropped_off_sample = True
    r2.prev = state
    return r2

def charge(state) :
    r2 = deepcopy(state)
    if state.dropped_off_sample and state.loc == "battery":
        r2.charged = True
    r2.prev = state
    return r2

action_list = [charge, drop_sample, pick_up_sample,
               move_to_sample, move_to_battery, move_to_station, pick_up_tool, drop_tool, use_tool]

def battery_goal(state) :
    return state.loc == "battery"

def sample_goal(state) :
    return state.loc == "sample"

def station_goal(state) :
    return state.loc == "station"

def remove_sample_goal(state) :
    return state.sample_extracted and state.holding_sample


# Return true if the sample is dropped off, the rover is at the station, and the rover is charged
def mission_complete(state) :
    return state.dropped_off_sample and state.loc == "battery" and state.charged


if __name__=="__main__" :
    s = RoverState()
    bfs_result = breadth_first_search(s, action_list, mission_complete)
    print("BFS result: ", bfs_result, "\n\n")
    
    dfs_result = depth_first_search(s, action_list, mission_complete)
    print("DFS result: ", dfs_result, "\n\n")
    
    dls_result = depth_first_search(s, action_list, mission_complete, limit=10)
    print("DLS result: ", dls_result, "\nLimit: 10 \n\n")
    
    move_to_sample_result = breadth_first_search(s, action_list, sample_goal) # Trying to get to the sample from the start
    print("Move to sample result: ", move_to_sample_result, "\n\n")
    
    remove_sample_result = breadth_first_search(move_to_sample_result[0], action_list, remove_sample_goal) # Trying to remove the sample while at the sample
    print("Remove sample result: ", remove_sample_result, "\n\n")
    
    return_to_charger_result = breadth_first_search(remove_sample_result[0], action_list, battery_goal) # Trying to return to the charger after removing the sample
    print("Return to charger result: ", return_to_charger_result, "\n\n")
    



