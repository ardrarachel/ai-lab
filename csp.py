import collections
import networkx as nx
import matplotlib.pyplot as plt

# --- 1. Helper Functions for CSP ---

def select_unassigned_variable(variables, assignment):
    """Selects the first unassigned variable from the list."""
    for var in variables:
        if var not in assignment:
            return var
    return None

def is_consistent(variable, color, graph, assignment):
    """Checks if a color assignment is consistent with the constraints."""
    for neighbor in graph.get(variable, []):
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True

# --- 2. The Backtracking Algorithm ---

def backtracking_csp(graph, colors):
    """
    The main backtracking function to solve the map coloring CSP.
    Returns the color assignment dictionary if a solution is found, otherwise None.
    """
    # Keep track of the nodes and the current color assignments
    nodes = list(graph.keys())
    assignment = {}

    def backtrack():
        # If all nodes are assigned a color, we have a solution
        if len(assignment) == len(nodes):
            return assignment

        # Select the next node to color
        var = select_unassigned_variable(nodes, assignment)
        
        # Try each color in the domain
        for color in colors:
            # Check if the color is consistent with the neighbors
            if is_consistent(var, color, graph, assignment):
                # Assign the color
                assignment[var] = color
                
                # Recursively call backtrack
                result = backtrack()
                if result:
                    return result
                
                # If the recursive call failed, backtrack (un-assign the color)
                del assignment[var]
        
        # If no color works, return failure
        return None

    return backtrack()

# --- 3. NetworkX Visualization ---

def display_colored_graph(graph, color_assignment):
    """Creates and displays the colored graph using NetworkX."""
    if not color_assignment:
        print("No solution to display.")
        return

    G = nx.Graph()
    # Add all edges from our adjacency list representation
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
            
    # Get the list of colors in the same order as the nodes in the graph
    node_colors = [color_assignment.get(node, 'gray') for node in G.nodes()]

    print("\nDisplaying the colored graph...")
    plt.figure(figsize=(8, 6))
    
    # Use a layout that spreads nodes out well
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, 
            node_size=2000, font_size=12, font_color='white',
            width=2.0, edge_color='gray')
            
    plt.title("Map Coloring Solution")
    plt.show()

# --- 4. Main Program Execution ---
if __name__ == "__main__":
    graph = collections.defaultdict(list)

    print("--- Graph Input for Map Coloring ---")
    try:
        num_edges = int(input("Enter the number of edges: "))
    except ValueError:
        print("Invalid number. Exiting.")
        exit()

    print("Enter each edge on a new line (e.g., 'WA NT' for Western Australia-Northern Territory)")
    nodes_set = set()
    for i in range(num_edges):
        try:
            node1, node2 = input(f"Edge {i+1}: ").strip().split()
            graph[node1].append(node2)
            graph[node2].append(node1)
            # Keep track of all unique nodes
            nodes_set.add(node1)
            nodes_set.add(node2)
        except ValueError:
            print("Invalid input. Please enter two nodes separated by a space.")
    
    # Ensure all nodes are in the graph dictionary, even if they have no edges
    for node in nodes_set:
        if node not in graph:
            graph[node] = []

    # --- Solve and Display ---
    colors_to_use = ['Red', 'Green', 'Blue']
    print(f"\nAttempting to color the map with {len(colors_to_use)} colors: {', '.join(colors_to_use)}")
    
    solution = backtracking_csp(graph, colors_to_use)

    if solution:
        print("\n✅ Solution found!")
        for node, color in sorted(solution.items()):
            print(f"  - {node}: {color}")
        display_colored_graph(graph, solution)
    else:
        print("\n❌ No solution found with the given colors.")