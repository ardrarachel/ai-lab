import collections
import random
import networkx as nx
import matplotlib.pyplot as plt

# --- 1. Hill Climbing Core Functions ---

def calculate_conflicts(graph, assignment):
    """
    Calculates the total number of conflicts in the current color assignment.
    A conflict is an edge where both nodes have the same color.
    """
    conflicts = 0
    # We check each edge only once to avoid double counting
    checked_edges = set()
    
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            # Create a sorted tuple to uniquely identify an edge
            edge = tuple(sorted((node, neighbor)))
            
            if edge not in checked_edges:
                # If the connected nodes have the same color, it's a conflict.
                if assignment[node] == assignment[neighbor]:
                    conflicts += 1
                checked_edges.add(edge)
                
    return conflicts

def hill_climbing(graph, colors, max_iterations=1000):
    """
    Attempts to solve the map coloring CSP using hill climbing.
    """
    # 1. Start: Create a complete, random assignment
    current_assignment = {}
    for node in graph:
        current_assignment[node] = random.choice(colors)
        
    for i in range(max_iterations):
        current_cost = calculate_conflicts(graph, current_assignment)
        
        # Goal Check: If cost is 0, we found a perfect solution.
        if current_cost == 0:
            print(f"Success! Found a solution in {i} iterations.")
            return current_assignment
        
        # 3. Find Best Neighbor
        best_neighbor_assignment = None
        best_neighbor_cost = current_cost
        
        # Check every possible single-node change
        for node in graph:
            original_color = current_assignment[node]
            for new_color in colors:
                if new_color == original_color:
                    continue
                    
                # Create the "neighbor" assignment
                neighbor_assignment = current_assignment.copy()
                neighbor_assignment[node] = new_color
                
                # Calculate the cost of this new state
                neighbor_cost = calculate_conflicts(graph, neighbor_assignment)
                
                # If this is the best move we've found so far, save it
                if neighbor_cost < best_neighbor_cost:
                    best_neighbor_cost = neighbor_cost
                    best_neighbor_assignment = neighbor_assignment
        
        # 4. Move or Get Stuck
        if best_neighbor_assignment is None:
            # No move improved the score. We are at a local minimum.
            print(f"Stuck at a local minimum after {i} iterations.")
            print(f"Final state has {current_cost} conflicts.")
            return current_assignment
        
        # 5. Move: Adopt the best neighbor's assignment as our new current state
        current_assignment = best_neighbor_assignment
        
    print(f"Reached max iterations ({max_iterations}).")
    print(f"Final state has {calculate_conflicts(graph, current_assignment)} conflicts.")
    return current_assignment

# --- 2. Visualization ---

def display_colored_graph(graph, assignment):
    """
    Displays the final colored graph using NetworkX.
    """
    if not assignment:
        print("No solution to display.")
        return

    # Map our 'r', 'g', 'b' domain to actual color names
    color_map = {'r': 'red', 'g': 'green', 'b': 'blue'}
    
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
            
    # Get the list of colors for drawing, mapped from our assignment
    node_colors = [color_map.get(assignment.get(node), 'gray') for node in G.nodes()]

    print("\nDisplaying the colored graph...")
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, 
            node_size=2000, font_size=12, font_color='white',
            width=2.0, edge_color='gray')
            
    plt.title("Map Coloring - Hill Climbing Solution")
    plt.show()

# --- 3. Main Program ---
if __name__ == "__main__":
    graph = collections.defaultdict(list)
    colors_to_use = ['r', 'g', 'b'] # Our 'rgb' domain

    print("--- Graph Input (for Hill Climbing) ---")
    try:
        num_edges = int(input("Enter the number of edges: "))
    except ValueError:
        print("Invalid number. Exiting.")
        exit()

    print("Enter each edge on a new line (e.g., 'WA NT')")
    nodes_set = set()
    for i in range(num_edges):
        try:
            node1, node2 = input(f"Edge {i+1}: ").strip().split()
            graph[node1].append(node2)
            graph[node2].append(node1)
            nodes_set.add(node1)
            nodes_set.add(node2)
        except ValueError:
            print("Invalid input. Please enter two nodes separated by a space.")
    
    # Ensure all nodes are in the graph dictionary
    for node in nodes_set:
        if node not in graph:
            graph[node] = []

    print(f"\nAttempting to color the map with {len(colors_to_use)} colors: {', '.join(colors_to_use)}")
    
    solution = hill_climbing(graph, colors_to_use)

    if solution:
        print("\n✅ Final Coloring:")
        for node, color in sorted(solution.items()):
            print(f"  - {node}: {color}")
        display_colored_graph(graph, solution)
    else:
        print("\n❌ No solution found.")