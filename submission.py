from mars_planner import *
from routefinder import *
from ortools.sat.python import cp_model

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
    
    
    start = map_state(location="8,8") 
    
    print("A* results:")
    a_star_result = a_star(start, sld, goal_test)
    
    print("Uniform cost search results:")
    ucs_result = a_star(start, h1, goal_test)
    
    # Instantiate model and solver
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    frequencies = {0: 'f1', 1: 'f2', 2: 'f3'}

    # Note 0-2 are the possible choices (f1, f2, and f3)
    Antenna1 = model.NewIntVar(0, 2, "A1")
    Antenna2 = model.NewIntVar(0, 2, "A2")
    Antenna3 = model.NewIntVar(0, 2, "A3")
    Antenna4 = model.NewIntVar(0, 2, "A4")
    Antenna5 = model.NewIntVar(0, 2, "A5")
    Antenna6 = model.NewIntVar(0, 2, "A6")
    Antenna7 = model.NewIntVar(0, 2, "A7")
    Antenna8 = model.NewIntVar(0, 2, "A8")
    Antenna9 = model.NewIntVar(0, 2, "A9")

    ## add the constraints
    model.Add(Antenna1 != Antenna2)
    model.Add(Antenna1 != Antenna3)
    model.Add(Antenna1 != Antenna4)

    model.Add(Antenna2 != Antenna1)
    model.Add(Antenna2 != Antenna3)
    model.Add(Antenna2 != Antenna5)
    model.Add(Antenna2 != Antenna6)

    model.Add(Antenna3 != Antenna1)
    model.Add(Antenna3 != Antenna2)
    model.Add(Antenna3 != Antenna6)
    model.Add(Antenna3 != Antenna9)

    model.Add(Antenna4 != Antenna1)
    model.Add(Antenna4 != Antenna2)
    model.Add(Antenna4 != Antenna5)

    model.Add(Antenna5 != Antenna2)
    model.Add(Antenna5 != Antenna4)

    model.Add(Antenna6 != Antenna2)
    model.Add(Antenna6 != Antenna7)
    model.Add(Antenna6 != Antenna8)

    model.Add(Antenna7 != Antenna6)
    model.Add(Antenna7 != Antenna8)

    model.Add(Antenna8 != Antenna7)
    model.Add(Antenna8 != Antenna9)

    model.Add(Antenna9 != Antenna3)
    model.Add(Antenna9 != Antenna8)


    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:    
        print("Antenna1: %s" % frequencies[solver.Value(Antenna1)])
        print("Antenna2: %s" % frequencies[solver.Value(Antenna2)])
        print("Antenna3: %s" % frequencies[solver.Value(Antenna3)])
        print("Antenna4: %s" % frequencies[solver.Value(Antenna4)])
        print("Antenna5: %s" % frequencies[solver.Value(Antenna5)])
        print("Antenna6: %s" % frequencies[solver.Value(Antenna6)])
        print("Antenna7: %s" % frequencies[solver.Value(Antenna7)])
        print("Antenna8: %s" % frequencies[solver.Value(Antenna8)])
        print("Antenna9: %s" % frequencies[solver.Value(Antenna9)])



    