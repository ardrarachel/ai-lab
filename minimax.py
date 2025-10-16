import math
import networkx as nx
import matplotlib.pyplot as plt
import collections

# --- 1. The Node Class: Our Tree's Building Block ---

class Node:
    """
    A class to represent a single node in the game tree.
    This helps organize the data for each position in the game.
    """
    def __init__(self, name, value=None):
        # The name of the node (e.g., 'A', 'B', 'D').
        self.name = name
        # The utility value if this node is a leaf (a final game state).
        # This will be None for internal nodes.
        self.value = value
        # A list to hold all of this node's children.
        self.children = []
        # This will store the final calculated value after Minimax runs.
        self.minimax_value = None

    def add_child(self, child_node):
        """Adds a child node to this node's list of children."""
        self.children.append(child_node)

# --- 2. The Minimax Algorithm ---

def minimax(node, is_maximizing_player):
    """
    The core recursive Minimax algorithm. It explores the tree downwards,
    then propagates the optimal scores back upwards.
    """
    # --- Base Case ---
    # If the node has no children, it's a leaf node. Its value is its predefined utility.
    if not node.children:
        node.minimax_value = node.value
        return node.value

    # --- Recursive Step ---
    if is_maximizing_player:
        # MAX Player's Turn: Find the child with the HIGHEST possible score.
        best_value = -math.inf  # Start with the lowest possible value.
        for child in node.children:
            # Recursively call minimax for the child. The player is now the Minimizer.
            value = minimax(child, False)
            # Update best_value if we find a better (higher) score.
            best_value = max(best_value, value)
        # Store the calculated best value in the node itself.
        node.minimax_value = best_value
        return best_value
    else: # Minimizing player
        # MIN Player's Turn: Find the child with the LOWEST possible score.
        best_value = math.inf  # Start with the highest possible value.
        for child in node.children:
            # Recursively call minimax for the child. The player is now the Maximizer.
            value = minimax(child, True)
            # Update best_value if we find a better (lower) score.
            best_value = min(best_value, value)
        # Store the calculated best value in the node itself.
        node.minimax_value = best_value
        return best_value

# --- 3. The Interactive Tree Builder ---

def build_tree_interactively():
    """
    Builds the game tree by asking the user for input, level by level.
    This method is simpler for the user than formatting a string.
    """
    root_name = input("Enter the name for the root node: ")
    root = Node(root_name)

    # A queue (First-In, First-Out) acts as a "to-do" list. It holds nodes
    # whose children we still need to ask the user about.
    nodes_to_process = collections.deque([root])

    # Loop as long as there are nodes in our "to-do" list.
    while nodes_to_process:
        # Get the next node from the front of the queue.
        current_node = nodes_to_process.popleft()

        is_leaf_str = input(f"\nIs node '{current_node.name}' a leaf node? (y/n): ").lower()
        if is_leaf_str == 'y':
            # If it's a leaf, get its final game score (utility value).
            while True:
                try:
                    value = int(input(f"Enter the value for leaf '{current_node.name}': "))
                    current_node.value = value
                    break # Exit the loop once a valid integer is entered.
                except ValueError:
                    print("Invalid input. Please enter an integer.")
        else:
            # If it's not a leaf, ask how many children it has.
            while True:
                try:
                    num_children = int(input(f"How many children does '{current_node.name}' have?: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter an integer.")
            
            # Loop to get the name of each child.
            for i in range(num_children):
                child_name = input(f"  Enter name for child {i+1} of '{current_node.name}': ")
                child_node = Node(child_name)
                current_node.add_child(child_node)
                # IMPORTANT: Add the new child to the back of the queue. This ensures
                # we will ask about its children later in the process.
                nodes_to_process.append(child_node)
    
    return root

# --- 4. Visualization Functions (using NetworkX) ---

def build_graph(node, graph):
    """Recursively populates a networkx graph from our Node tree."""
    if node is None: return
    for child in node.children:
        graph.add_edge(node.name, child.name)
        build_graph(child, graph)

def display_with_networkx(root):
    """Creates and displays the graph with all calculated values."""
    G = nx.DiGraph()
    build_graph(root, G)

    # Helper function to get all node objects for labeling
    all_nodes = []
    def get_all_nodes_recursive(node):
        if node:
            all_nodes.append(node)
            for child in node.children:
                get_all_nodes_recursive(child)
    get_all_nodes_recursive(root)
    
    # Create a map from name to node object to easily access the minimax_value
    node_map = {n.name: n for n in all_nodes}
    # Create labels in the format: "NodeName\n[CalculatedValue]"
    labels = {n.name: f"{n.name}\n[{n.minimax_value}]" for n in all_nodes}
    
    try:
        # Use graphviz for a proper top-down hierarchical tree layout.
        pos = nx.drawing.nx_pydot.graphviz_layout(G, prog='dot')
    except ImportError:
        print("\nPyGraphviz not found. Using a simpler layout.")
        pos = nx.spring_layout(G)

    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, labels=labels, with_labels=True, arrows=False,
            node_size=3000, node_color='skyblue', font_size=11,
            font_weight='bold', width=2.0, edge_color='gray')
    
    plt.title("Minimax Tree with Calculated Values")
    plt.show()

# --- 5. Main Program Execution ---

# This block runs only when the script is executed directly.
if __name__ == "__main__":
    print("--- Minimax Algorithm: Interactive Tree Builder ---")
    
    # Start the process by building the tree with user input.
    root = build_tree_interactively()

    if root:
        print("\n--- Running Minimax Algorithm ---")
        # Start the minimax calculation from the root.
        # We assume the first player (at the root) is the Maximizer (True).
        minimax(root, True)

        print(f"\nOptimal value at the root is: {root.minimax_value}")
        print("Displaying the full tree with calculated values...")
        
        # Display the final, annotated tree.
        display_with_networkx(root)
    else:
        print("No tree was created.")