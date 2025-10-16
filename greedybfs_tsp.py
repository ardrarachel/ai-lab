import collections

def solve_tsp_greedy_heuristic(graph, heuristics, start_node):
    """
    Finds a TSP tour using a Greedy Best-First Search style heuristic.
    At each step, it travels to the unvisited neighbor with the lowest heuristic value.
    """
    # --- 1. Initialization ---
    # Create a set of all unique cities in the graph.
    all_cities = set(graph.keys())
    for node in graph:
        all_cities.update(graph[node].keys())

    # Check if the starting city is valid.
    if start_node not in all_cities:
        print(f"Error: Starting city '{start_node}' not found in the graph.")
        return None, 0

    # Initialize the tour variables.
    tour = [start_node]
    visited = {start_node}
    total_cost = 0  # This will be the SUM of actual edge costs.
    current_city = start_node

    # --- 2. Build the Tour ---
    # Loop until all cities have been visited.
    while len(tour) < len(all_cities):
        best_next_city = None
        min_heuristic = float('inf')  # Start with an infinitely high heuristic value.

        # --- CORE LOGIC CHANGE ---
        # Find the unvisited neighbor with the lowest heuristic value.
        for neighbor in graph.get(current_city, {}).keys():
            if neighbor not in visited:
                # Compare heuristic values instead of edge costs.
                neighbor_heuristic = heuristics.get(neighbor, float('inf'))
                if neighbor_heuristic < min_heuristic:
                    min_heuristic = neighbor_heuristic
                    best_next_city = neighbor
        
        # If a valid next city was chosen based on the heuristic...
        if best_next_city:
            # ...find the ACTUAL travel cost from the graph.
            travel_cost = graph[current_city][best_next_city]
            
            # Update the tour and state.
            tour.append(best_next_city)
            visited.add(best_next_city)
            total_cost += travel_cost  # Add the real travel cost to the total.
            current_city = best_next_city
        else:
            # This happens if the graph is not fully connected.
            print(f"Error: Stuck at '{current_city}'. Cannot reach any unvisited city.")
            return None, 0

    # --- 3. Complete the Tour ---
    # Return from the last city to the starting city.
    last_city = tour[-1]
    if start_node in graph.get(last_city, {}):
        return_cost = graph[last_city][start_node]
        total_cost += return_cost
        tour.append(start_node)
    else:
        print(f"Error: No return path from '{last_city}' back to '{start_node}'.")
        return None, 0

    return tour, total_cost

# --- Main Program Execution ---
if __name__ == "__main__":
    graph = collections.defaultdict(dict)
    heuristics = {}

    print("--- TSP Solver using Greedy BFS Heuristic ---")
    
    # --- Get Heuristic Values from User ---
    try:
        num_nodes = int(input("Enter the number of cities with heuristics: "))
    except ValueError:
        print("Invalid number. Exiting.")
        exit()
    print("Enter each city and its heuristic value (e.g., 'A 10')")
    for i in range(num_nodes):
        try:
            node, h_val = input(f"City {i+1}: ").strip().split()
            heuristics[node] = int(h_val)
        except ValueError:
            print("Invalid input. Format must be 'CityName HeuristicValue'.")

    # --- Get Graph Connections and Costs from User ---
    try:
        num_edges = int(input("\nEnter the number of connections (edges): "))
    except ValueError:
        print("Invalid number. Exiting.")
        exit()
    print("Enter each connection and its cost (e.g., 'A B 5')")
    for i in range(num_edges):
        try:
            node1, node2, cost_str = input(f"Connection {i+1}: ").strip().split()
            cost = int(cost_str)
            graph[node1][node2] = cost
            graph[node2][node1] = cost
        except ValueError:
            print("Invalid input. Format must be 'City1 City2 Cost'.")

    start_node = input("\nEnter the starting city: ").strip()

    # --- Run the solver and print the result ---
    tour, cost = solve_tsp_greedy_heuristic(graph, heuristics, start_node)

    if tour:
        print("\n✅ Greedy TSP Tour Found (using heuristic for decisions):")
        print(f"   Path: {' -> '.join(tour)}")
        print(f"   Total Actual Cost: {cost}")
    else:
        print("\n❌ Could not find a complete tour.")