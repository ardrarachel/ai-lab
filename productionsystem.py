import collections

# --- 1. Rule Base ---
# Each rule is a function that represents a "production."
# It takes the current state (Working Memory) and returns a new state
# if the rule's condition is met. Otherwise, it returns None.

def fill_jug1(state, capacities):
    """IF jug1 is not full, THEN fill jug1."""
    jug1, jug2 = state
    cap1, _ = capacities
    if jug1 < cap1:
        return (cap1, jug2)
    return None

def fill_jug2(state, capacities):
    """IF jug2 is not full, THEN fill jug2."""
    jug1, jug2 = state
    _, cap2 = capacities
    if jug2 < cap2:
        return (jug1, cap2)
    return None

def empty_jug1(state, capacities):
    """IF jug1 is not empty, THEN empty jug1."""
    jug1, jug2 = state
    if jug1 > 0:
        return (0, jug2)
    return None

def empty_jug2(state, capacities):
    """IF jug2 is not empty, THEN empty jug2."""
    jug1, jug2 = state
    if jug2 > 0:
        return (0, jug1) # Corrected: (jug1, 0)
    return None

def pour_jug1_to_jug2(state, capacities):
    """
    IF jug1 is not empty AND jug2 is not full, 
    THEN pour from jug1 to jug2.
    """
    jug1, jug2 = state
    cap1, cap2 = capacities
    if jug1 > 0 and jug2 < cap2:
        # Calculate amount to pour: either all of jug1 or just enough to fill jug2
        amount = min(jug1, cap2 - jug2)
        return (jug1 - amount, jug2 + amount)
    return None

def pour_jug2_to_jug1(state, capacities):
    """
    IF jug2 is not empty AND jug1 is not full, 
    THEN pour from jug2 to jug1.
    """
    jug1, jug2 = state
    cap1, cap2 = capacities
    if jug2 > 0 and jug1 < cap1:
        # Calculate amount to pour: either all of jug2 or just enough to fill jug1
        amount = min(jug2, cap1 - jug1)
        return (jug1 + amount, jug2 - amount)
    return None

# --- Main Program ---
if __name__ == "__main__":

    # Define the problem: (4-gal jug, 3-gal jug, 2-gal target)
    jug_capacities = (4, 3)
    target_amount = 2
    
    # --- 1. Rule Base ---
    # The set of all possible productions (rules).
    rule_base = [
        fill_jug1,
        fill_jug2,
        empty_jug1,
        empty_jug2,
        pour_jug1_to_jug2,
        pour_jug2_to_jug1
    ]

    # --- 2. Working Memory ---
    # The initial state (facts) of the world.
    working_memory = (0, 0)
    
    # We need a 'visited' set to prevent infinite loops (e.g., fill -> empty -> fill)
    visited_states = set()
    visited_states.add(working_memory)
    
    # A queue to track the path (states to explore).
    # Each item is a (state, path_to_state) tuple.
    queue = collections.deque([ (working_memory, [working_memory]) ])

    print(f"Solving Water Jug Problem: Capacities {jug_capacities}, Target {target_amount} gal")
    print("--- Inference Engine Started ---")

    solution_path = None

    # --- 3. Inference Engine (Recognize-Act Cycle) ---
    while queue:
        # Get the next state from memory to process.
        current_state, path = queue.popleft()
        
        # --- Goal Check ---
        # Check if the current state meets the goal condition.
        if current_state[0] == target_amount or current_state[1] == target_amount:
            print(f"\nGoal Reached! Found {target_amount} gallons.")
            solution_path = path
            break

        # --- Match Phase ---
        # Iterate through the rule base to find all applicable rules.
        for rule in rule_base:
            # --- Act Phase (Simulated) ---
            # Try to "fire" the rule.
            new_state = rule(current_state, jug_capacities)
            
            # If the rule produced a valid new state that we haven't seen...
            if new_state is not None and new_state not in visited_states:
                # Add the new state to our memory of seen states.
                visited_states.add(new_state)
                
                # Update the Working Memory for the next cycle
                # (by adding the new state to the queue to be processed).
                new_path = path + [new_state]
                queue.append((new_state, new_path))
                
                # --- Conflict Resolution (Implicit) ---
                # This is a BFS, so it doesn't just pick one rule,
                # it explores all applicable rules layer by layer.
                # A simpler production system might 'break' here
                # and restart the loop with the new_state.

    # --- Final Output ---
    if solution_path:
        print("\n--- Solution Path (Jug1, Jug2) ---")
        for i, state in enumerate(solution_path):
            print(f"  Step {i}: {state}")
    else:
        print(f"\nNo solution found to reach {target_amount} gallons.")