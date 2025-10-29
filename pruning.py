import math
import networkx as nx
import matplotlib.pyplot as plt
import collections

class Node:
    """A class to represent a node in the game tree."""
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.children = []
        self.minimax_value = None
        # A flag to track if this node's branch was pruned
        self.is_pruned = False

    def add_child(self, child_node):
        self.children.append(child_node)

def alpha_beta_pruning(node, is_maximizing_player, alpha, beta):
    """
    The core Minimax algorithm with Alpha-Beta Pruning.
    """
    # Base case: If it's a leaf node, return its utility value.
    if not node.children:
        node.minimax_value = node.value
        return node.value,[node.name]

    if is_maximizing_player:
        best_value = -math.inf
        best_path = []
        # Loop through each child to find the best move.
        for i, child in enumerate(node.children):
            value,path= alpha_beta_pruning(child, False, alpha, beta)
            if value > best_value:
                best_value = value
                best_path = [node.name] + path
            # Update alpha (the best score MAX can guarantee).
            alpha = max(alpha, best_value)
            
            # --- Pruning Condition ---
            if beta <= alpha:
                # The MIN player (parent) has found a better option already.
                # Prune the remaining children of this node.
                for remaining_child in node.children[i+1:]:
                    remaining_child.is_pruned = True
                    print(f"Pruned edge: {node.name} -> {remaining_child.name}")
                break # Stop searching this branch.
        
        node.minimax_value = best_value
        return best_value,best_path
    else: # Minimizing player
        best_value = math.inf
        best_path = []
        # Loop through each child to find the best move for MIN.
        for i, child in enumerate(node.children):
            value,path = alpha_beta_pruning(child, True, alpha, beta)
            if value < best_value:
                best_value = value
                best_path = [node.name] + path
            # Update beta (the best score MIN can guarantee).
            beta = min(beta, best_value)

            # --- Pruning Condition ---
            if beta <= alpha:
                # The MAX player (parent) has found a better option already.
                # Prune the remaining children of this node.
                for remaining_child in node.children[i+1:]:
                    remaining_child.is_pruned = True
                    print(f"Pruned edge: {node.name} -> {remaining_child.name}")
                break # Stop searching this branch.
        
        node.minimax_value = best_value
        return best_value,best_path

# --- Interactive Tree Builder (Same as before) ---
def build_tree_interactively():
    root_name = input("Enter the name for the root node: ")
    root = Node(root_name)
    nodes_to_process = collections.deque([root])
    while nodes_to_process:
        current_node = nodes_to_process.popleft()
        is_leaf_str = input(f"\nIs node '{current_node.name}' a leaf node? (y/n): ").lower()
        if is_leaf_str == 'y':
            while True:
                try:
                    value = int(input(f"Enter the value for leaf '{current_node.name}': "))
                    current_node.value = value
                    break
                except ValueError: print("Please enter an integer.")
        else:
            while True:
                try:
                    num_children = int(input(f"How many children does '{current_node.name}' have?: "))
                    break
                except ValueError: print("Please enter an integer.")
            for i in range(num_children):
                child_name = input(f"  Enter name for child {i+1} of '{current_node.name}': ")
                child_node = Node(child_name)
                current_node.add_child(child_node)
                nodes_to_process.append(child_node)
    return root

# --- NetworkX Visualization (Updated to show pruning) ---
def build_graph(node, graph):
    if node is None: return
    for child in node.children:
        graph.add_edge(node.name, child.name)
        build_graph(child, graph)

def display_with_networkx(root):
    G = nx.DiGraph()
    build_graph(root, G)

    all_nodes = []
    def get_all_nodes_recursive(node):
        if node:
            all_nodes.append(node)
            for child in node.children:
                get_all_nodes_recursive(child)
    get_all_nodes_recursive(root)
    
    node_map = {n.name: n for n in all_nodes}
    labels = {n.name: f"{n.name}\n[{n.minimax_value}]" if n.minimax_value is not None else n.name for n in all_nodes}
    
    # --- Style updates for pruning ---
    edge_colors = ['lightgray' if node_map.get(v).is_pruned else 'black' for u, v in G.edges()]
    edge_styles = ['dashed' if node_map.get(v).is_pruned else 'solid' for u, v in G.edges()]
    node_colors = ['lightgray' if node_map.get(n).is_pruned else 'skyblue' for n in G.nodes()]

    try:
        pos = nx.drawing.nx_pydot.graphviz_layout(G, prog='dot')
    except ImportError:
        pos = nx.spring_layout(G)

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, labels=labels, with_labels=True, arrows=False,
            node_size=3000, node_color=node_colors, font_size=10,
            font_weight='bold', width=2.0, edge_color=edge_colors, style=edge_styles)
    plt.title("Minimax Tree with Alpha-Beta Pruning")
    plt.show()

# --- Main Program Execution ---
if __name__ == "__main__":
    print("--- Alpha-Beta Pruning: Interactive Tree Builder ---")
    root = build_tree_interactively()

    if root:
        print("\n--- Running Minimax with Alpha-Beta Pruning ---")
        # Start the algorithm with initial alpha (-inf) and beta (+inf).
        value,path=alpha_beta_pruning(root, True, -math.inf, math.inf)

        print(f"\nOptimal value at the root is: {root.minimax_value}")
        print(f"The best path is: {' -> '.join(path)}")
        print("Displaying the pruned tree...")
        display_with_networkx(root)