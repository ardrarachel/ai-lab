import collections

def solve_water_jug(cap1, cap2, target):
    """
    Solves the Water Jug Problem using Breadth-First Search.
    
    cap1: Capacity of jug 1
    cap2: Capacity of jug 2
    target: The target amount of water to get in one of the jugs
    """
    
    # The queue will store tuples of: ( (jug1, jug2), path_to_this_state )
    # path_to_this_state is a list of (jug1, jug2) tuples
    queue = collections.deque([ ((0, 0), [(0, 0)]) ])
    
    # The 'visited' set stores states we've already seen to avoid infinite loops.
    visited = set([(0, 0)])

    while queue:
        # Get the next state and the path to reach it from the front of the queue.
        (jug1, jug2), path = queue.popleft()

        # --- Goal Check ---
        # If either jug has the target amount, we found a solution.
        if jug1 == target or jug2 == target:
            return path, len(path) - 1

        # --- Generate All Possible Next States (Actions) ---
        
        # 1. Fill jug 1
        state_fill1 = (cap1, jug2)
        if state_fill1 not in visited:
            visited.add(state_fill1)
            queue.append((state_fill1, path + [state_fill1]))
            
        # 2. Fill jug 2
        state_fill2 = (jug1, cap2)
        if state_fill2 not in visited:
            visited.add(state_fill2)
            queue.append((state_fill2, path + [state_fill2]))

        # 3. Empty jug 1
        state_empty1 = (0, jug2)
        if state_empty1 not in visited:
            visited.add(state_empty1)
            queue.append((state_empty1, path + [state_empty1]))

        # 4. Empty jug 2
        state_empty2 = (jug1, 0)
        if state_empty2 not in visited:
            visited.add(state_empty2)
            queue.append((state_empty2, path + [state_empty2]))

        # 5. Pour from jug 1 to jug 2
        # Calculate amount to pour: either all of jug 1, or just enough to fill jug 2
        pour_amount1 = min(jug1, cap2 - jug2)
        state_pour12 = (jug1 - pour_amount1, jug2 + pour_amount1)
        if state_pour12 not in visited:
            visited.add(state_pour12)
            queue.append((state_pour12, path + [state_pour12]))
            
        # 6. Pour from jug 2 to jug 1
        # Calculate amount to pour: either all of jug 2, or just enough to fill jug 1
        pour_amount2 = min(jug2, cap1 - jug1)
        state_pour21 = (jug1 + pour_amount2, jug2 - pour_amount2)
        if state_pour21 not in visited:
            visited.add(state_pour21)
            queue.append((state_pour21, path + [state_pour21]))

    # If the queue becomes empty and we haven't found the target, no solution exists.
    return None, 0

# --- Main Program Execution ---
if __name__ == "__main__":
    try:
        cap_jug1 = int(input("Enter the capacity of Jug 1: "))
        cap_jug2 = int(input("Enter the capacity of Jug 2: "))
        target_amount = int(input("Enter the target amount: "))
        
        # A simple check for solvability
        if target_amount > max(cap_jug1, cap_jug2):
            print("\n❌ No solution possible: Target is larger than both jugs.")
        else:
            print(f"\nSearching for a way to get {target_amount} gallons...")
            solution_path, steps = solve_water_jug(cap_jug1, cap_jug2, target_amount)
            
            if solution_path:
                print(f"\n✅ Solution found in {steps} steps!")
                print("Path (Jug1, Jug2):")
                for i, state in enumerate(solution_path):
                    print(f"  Step {i}: {state}")
            else:
                print("\n❌ No solution found.")
                
    except ValueError:
        print("Invalid input. Please enter integers only.")