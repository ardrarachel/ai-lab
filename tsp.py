import collections

def solve_tsp_nearest_neighbor(graph, start_node):
    """
    Finds a TSP tour using the greedy "Nearest Neighbor" method.
    At each step, it travels to the closest unvisited city.
    """
    # --- 1. Initialization ---
    # Create a set of all unique cities to know how many we need to visit.
    all_cities = set(graph.keys())
    for node in graph:
        # .update() adds all items from the neighbor dictionary's keys to the set.
        all_cities.update(graph[node].keys())

    # Basic error check to ensure the starting city exists in the graph.
    if start_node not in all_cities:
        print(f"Error: Starting city '{start_node}' not found in the graph.")
        return None, 0

    # Initialize the tour variables.
    tour = [start_node]           # The list of cities in the order they are visited.
    visited = {start_node}        # A set for fast checking of visited cities.
    total_cost = 0                # The running total cost of the tour.
    current_city = start_node     # The city we are currently at.

    # --- 2. Build the Tour ---
    # Loop until our tour includes every city.
    while len(tour) < len(all_cities):
        nearest_neighbor = None
        min_cost = float('inf')  # Start with an infinitely high cost.

        # Find the cheapest path from the current city to an unvisited one.
        # .get(current_city, {}) safely gets neighbors, returns empty dict if none.
        for neighbor, cost in graph.get(current_city, {}).items():
            # If the neighbor hasn't been visited and is the cheapest so far...
            if neighbor not in visited and cost < min_cost:
                # ...update it as our best choice for the next step.
                min_cost = cost
                nearest_neighbor = neighbor
        
        # If we found a valid next city, travel there.
        if nearest_neighbor:
            tour.append(nearest_neighbor)
            visited.add(nearest_neighbor)
            total_cost += min_cost
            current_city = nearest_neighbor
        else:
            # If we get here, the graph is not fully connected and we are stuck.
            print(f"Error: Stuck at '{current_city}'. Cannot reach any unvisited city.")
            return None, 0

    # --- 3. Complete the Tour ---
    # After visiting all cities, return to the starting city.
    last_city = tour[-1]
    # Check if there is a direct path from the last city back to the start.
    if start_node in graph.get(last_city, {}):
        return_cost = graph[last_city][start_node]
        total_cost += return_cost
        tour.append(start_node)
    else:
        print(f"Error: No return path from '{last_city}' back to '{start_node}'.")
        return None, 0

    # Return the completed tour and its total cost.
    return tour, total_cost

# --- Main Program Execution ---
if __name__ == "__main__":
    # Use a defaultdict of dictionaries to easily store the graph.
    # e.g., graph['A']['B'] = 10
    graph = collections.defaultdict(dict)

    print("--- TSP Solver using Nearest Neighbor ---")
    try:
        # Get the number of connections the user wants to define.
        num_edges = int(input("Enter the number of connections (edges): "))
    except ValueError:
        print("Invalid number. Exiting.")
        exit()

    print("Enter each connection and its cost (e.g., 'A B 5')")
    # Loop to get the details for each connection.
    for i in range(num_edges):
        try:
            # Read the input and split it into three parts.
            node1, node2, cost_str = input(f"Connection {i+1}: ").strip().split()
            # Convert the cost from a string to an integer.
            cost = int(cost_str)
            # Add the connection to the graph.
            graph[node1][node2] = cost
            # This makes the graph undirected (A->B is the same as B->A).
            graph[node2][node1] = cost
        except ValueError:
            print("Invalid input. Format must be 'City1 City2 Cost'.")

    # Get the starting point for the tour from the user.
    start_node = input("\nEnter the starting city: ").strip()

    # --- Run the solver and print the result ---
    tour, cost = solve_tsp_nearest_neighbor(graph, start_node)

    # If the function returned a valid tour, print the details.
    if tour:
        print("\n✅ Greedy TSP Tour Found:")
        # ' -> '.join(tour) creates a nice string like "A -> B -> C"
        print(f"   Path: {' -> '.join(tour)}")
        print(f"   Total Cost: {cost}")
    else:
        # Otherwise, inform the user that a tour could not be completed.
        print("\n❌ Could not find a complete tour.")