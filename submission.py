from mars_planner import *
from routefinder import *

if __name__ == '__main__':
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
    
    
    start = map_state(location="8,8", h=sld(map_state(location="8,8"))) # h is the SLD between the start and the goal
    
    print("A* results:")
    a_star_result = a_star(start, sld, goal_test)
    
    print("Uniform cost search results:")
    ucs_result = a_star(start, h1, goal_test)