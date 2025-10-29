import heapq
def printpuzzle(state):
    for i in range(0,9,3):
        print(" ".join(map(str, state[i:i+3])).replace('0', '_'))
    print()
def misplaced(initial,goal):
    misplaced=0
    for i in range(9):
        if(initial[i]!=goal[i] and initial[i]!=0):
            misplaced+=1
    return misplaced
def manhattan(initial,goal):
    dist=0
    for i in range(9):
        if(initial[i]!=0):
            row,col=divmod(i,3)
            goalrow,goalcol=divmod(goal.index(initial[i]),3)
            dist+=abs(row-goalrow)+abs(col-goalcol)
    return dist
def successors(initial):
    successor=[]
    blankind=initial.index(0)
    row,col=divmod(blankind,3)
    moves=[(-1,0),(1,0),(0,-1),(0,1)]
    for dx,dr in moves:
        newr,newcol=dx+row,dr+col
        if(0<=newr<3 and 0<=newcol<3):
            index=newr*3+newcol
            newstate=list(initial)
            newstate[blankind],newstate[index]=newstate[index],newstate[blankind]
            successor.append(tuple(newstate))
    return successor
def astar(initial,goal,heuristic):
    pq=[(0,0,initial,[initial])]
    explored_states = set()
    while pq:
        # Pop the state with the lowest f_cost
        f_cost, g_cost, current_state, path = heapq.heappop(pq)

        if current_state in explored_states:
            continue
        
        explored_states.add(current_state)

        if current_state == goal:
            return path, len(explored_states) # Return path and number of states explored

        # Explore successors
        for successor in successors(current_state):
            if successor not in explored_states:
                new_g_cost = g_cost + 1
                h_cost = heuristic(successor, goal)
                new_f_cost = new_g_cost + h_cost
                heapq.heappush(pq, (new_f_cost, new_g_cost, successor, path + [successor]))
    
    return None, len(explored_states)
if __name__ == "__main__":
    print("--- 8-Puzzle Solver using A* Search ---")
    
    # --- Get User Input for States ---
    print("\nEnter the initial state of the puzzle (use 0 for the blank space).")
    print("Example: 1 2 3 4 5 6 7 8 0")
    try:
        initial_input = input("Initial State: ").strip().split()
        initial_state = tuple(map(int, initial_input))
        if len(initial_state) != 9 or len(set(initial_state)) != 9:
            raise ValueError
    except ValueError:
        print("Invalid input. Please enter 9 unique numbers from 0 to 8.")
        exit()

    print("\nEnter the goal state of the puzzle.")
    try:
        goal_input = input("Goal State: ").strip().split()
        goal_state = tuple(map(int, goal_input))
        if len(goal_state) != 9 or len(set(goal_state)) != 9:
            raise ValueError
    except ValueError:
        print("Invalid input. Please enter 9 unique numbers from 0 to 8.")
        exit()

    # --- Get User Choice for Heuristic ---
    print("\nChoose a heuristic function:")
    print("1. Number of Misplaced Tiles")
    print("2. Manhattan Distance")
    
    try:
        choice = int(input("Enter your choice (1 or 2): "))
        if choice == 1:
            heuristic = misplaced
            heuristic_name = "Misplaced Tiles"
        elif choice == 2:
            heuristic = manhattan
            heuristic_name = "Manhattan Distance"
        else:
            raise ValueError
    except ValueError:
        print("Invalid choice. Please enter 1 or 2.")
        exit()

    # --- Run A* and Print Results ---
    print(f"\nSolving puzzle using A* with {heuristic_name} heuristic...")
    
    solution_path, states_explored = astar(initial_state, goal_state, heuristic)

    if solution_path:
        print("\n✅ Solution Found!")
        print(f"Total moves: {len(solution_path) - 1}")
        print(f"Total states explored: {states_explored}")
        print("\nSolution Path:")
        for i, state in enumerate(solution_path):
            print(f"Step {i}:")
            printpuzzle(state)
    else:
        print("\n❌ No solution found. The puzzle may be unsolvable from the initial state.")