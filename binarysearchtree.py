class Node:
    """
    A class to represent a single node in the BST.
    Each node holds its own value and pointers to its left and right children.
    """
    def __init__(self, key):
        self.key = key      # The value stored in the node
        self.left = None    # Pointer to the left child
        self.right = None   # Pointer to the right child

class BinarySearchTree:
    """
    A class to represent the entire Binary Search Tree.
    It manages the root node and all operations like insert, search, and delete.
    """
    def __init__(self):
        self.root = None  # The tree is initially empty

    # --- 1. Insertion ---
    
    def insert(self, key):
        """Public method to insert a new key into the tree."""
        if self.root is None:
            # If the tree is empty, the new key becomes the root.
            self.root = Node(key)
        else:
            # Otherwise, find the correct spot starting from the root.
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, current_node, key):
        """Private helper function to recursively find the insertion point."""
        if key < current_node.key:
            # Go left
            if current_node.left is None:
                current_node.left = Node(key)
            else:
                self._insert_recursive(current_node.left, key)
        elif key > current_node.key:
            # Go right
            if current_node.right is None:
                current_node.right = Node(key)
            else:
                self._insert_recursive(current_node.right, key)
        # If key == current_node.key, we do nothing (no duplicates allowed).

    # --- 2. Searching ---
    
    def search(self, key):
        """Public method to search for a key. Returns True if found, False otherwise."""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, current_node, key):
        """Private helper function to recursively search for a key."""
        # Base Cases:
        # 1. The node doesn't exist (we hit a dead end).
        if current_node is None:
            return False
        # 2. We found the key.
        if current_node.key == key:
            return True
        
        # Recursive Steps:
        if key < current_node.key:
            # Go left
            return self._search_recursive(current_node.left, key)
        else:
            # Go right
            return self._search_recursive(current_node.right, key)

    # --- 3. Deletion ---

    def delete(self, key):
        """Public method to delete a key from the tree."""
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, current_node, key):
        """Private helper function to recursively find and delete a node."""
        if current_node is None:
            # The key was not found.
            return current_node

        # 1. Find the node to delete
        if key < current_node.key:
            current_node.left = self._delete_recursive(current_node.left, key)
        elif key > current_node.key:
            current_node.right = self._delete_recursive(current_node.right, key)
        else:
            # 2. Found the node! Now handle the 3 deletion cases:
            
            # Case 1: Node has no children (leaf node)
            if current_node.left is None and current_node.right is None:
                current_node = None # The node is simply removed.
            
            # Case 2: Node has one child
            elif current_node.left is None:
                current_node = current_node.right # Replace node with its right child.
            elif current_node.right is None:
                current_node = current_node.left # Replace node with its left child.
                
            # Case 3: Node has two children
            else:
                # Find the "in-order successor" (the smallest node in the right subtree)
                successor = self._find_min(current_node.right)
                # Copy the successor's key to this node
                current_node.key = successor.key
                # Recursively delete the successor from its original position
                current_node.right = self._delete_recursive(current_node.right, successor.key)
                
        return current_node

    def _find_min(self, node):
        """Helper to find the node with the minimum key in a subtree."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    # --- 4. Traversal (for Printing) ---
    
    def inorder_traversal(self):
        """
        Public method to perform an in-order traversal.
        This prints the tree's keys in sorted order.
        """
        print("In-order Traversal:", end=" ")
        self._inorder_recursive(self.root)
        print() # For a new line

    def _inorder_recursive(self, current_node):
        """Private helper for in-order traversal (Left -> Root -> Right)."""
        if current_node is not None:
            self._inorder_recursive(current_node.left)
            print(current_node.key, end=" ")
            self._inorder_recursive(current_node.right)

# --- Example Usage ---
if __name__ == "__main__":
    bst = BinarySearchTree()
    
    # Insert nodes
    nodes_to_insert = [50, 30, 70, 20, 40, 60, 80]
    print(f"Inserting: {nodes_to_insert}")
    for node in nodes_to_insert:
        bst.insert(node)
        
    # 

    # Print the sorted tree
    bst.inorder_traversal() # Output: 20 30 40 50 60 70 80

    # Search for nodes
    print(f"Search for 40: {bst.search(40)}") # Output: True
    print(f"Search for 90: {bst.search(90)}") # Output: False

    # Delete a node (Case 1: leaf node)
    print("\nDeleting 20 (leaf node)...")
    bst.delete(20)
    bst.inorder_traversal() # Output: 30 40 50 60 70 80

    # Delete a node (Case 2: one child)
    print("\nDeleting 30 (one child)...")
    bst.delete(30)
    bst.inorder_traversal() # Output: 40 50 60 70 80

    # Delete a node (Case 3: two children)
    print("\nDeleting 50 (two children)...")
    bst.delete(50)
    bst.inorder_traversal() # Output: 40 60 70 80



