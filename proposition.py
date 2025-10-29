def modus_ponens(implication, premise):
    # Parse implication like: "If it rains, the ground is wet"
    if "if" not in implication.lower() or "," not in implication:
        return "Invalid implication format. Use: 'If P, Q'"

    parts = implication.lower().split(",")
    antecedent = parts[0].replace("if", "").strip()
    consequent = parts[1].strip()

    if premise.lower() == antecedent:
        return f"Therefore, {consequent} (Modus Ponens)"
    else:
        return "Premise does not match antecedent. Cannot apply Modus Ponens."


def modus_tollens(implication, negated_consequent):
    if "if" not in implication.lower() or "," not in implication:
        return "Invalid implication format. Use: 'If P, Q'"

    parts = implication.lower().split(",")
    antecedent = parts[0].replace("if", "").strip()
    consequent = parts[1].strip()

    if negated_consequent.lower().startswith("not "):
        given_consequent = negated_consequent.lower().replace("not ", "").strip()
    else:
        return "Must provide negation of consequent (e.g., 'Not Q')"

    if given_consequent == consequent:
        return f"Therefore, not {antecedent} (Modus Tollens)"
    else:
        return "Consequent does not match. Cannot apply Modus Tollens."


def resolve_clauses(clause1, clause2):
    # Remove literals with same variable, opposite signs
    result = set(clause1)
    for lit in clause2:
        if -lit in result:
            result.discard(-lit)
        else:
            result.add(lit)
    return tuple(sorted(result))


def resolution_solver(clauses):
    from collections import deque

    queue = deque(clauses)

    while len(queue) > 1:
        first = queue.popleft()
        second = queue.popleft()

        new_clause = resolve_clauses(first, second)

        if not new_clause:
            return "Contradiction (empty clause)"

        if len(new_clause) == 1:
            return f"Resolved to: {new_clause[0]}"

        # Insert the new clause at the **start**
        queue.appendleft(new_clause)

    if len(queue) == 1 and len(queue[0]) == 1:
        return f"Resolved to: {queue[0][0]}"
    else:
        return f"Final clause: {queue[0]}"


def parse_input(input_str):
    try:
        clauses = eval(input_str)
        if not isinstance(clauses, list) or not all(isinstance(c, tuple) for c in clauses):
            raise ValueError
        return clauses
    except:
        print("❌ Invalid input. Enter clauses as a list of tuples. Example: [(1, -2), (-1, 3)]")
        return None


# ----------- Test Interactively --------------
if __name__ == "__main__":
    print("Choose logic rule:")
    print("1. Modus Ponens")
    print("2. Modus Tollens")
    print("3. Unit Resolution")
    choice = input("Enter 1/2/3: ")

    if choice == "1":
        implication = input("Enter implication (e.g., 'If it rains, the ground is wet'): ")
        premise = input("Enter known premise (e.g., 'it rains'): ")
        result = modus_ponens(implication, premise)
        print(result)

    elif choice == "2":
        implication = input("Enter implication (e.g., 'If it rains, the ground is wet'): ")
        negated_consequent = input("Enter known negated consequent (e.g., 'Not the ground is wet'): ")
        result = modus_tollens(implication, negated_consequent)
        print(result)

    elif choice == "3":
        print("Enter your clauses as a list of tuples, e.g.: [(1, -2), (-1, 3), (2, 3), (-3,)]")

        user_input = input("Clauses: ")
        clauses = parse_input(user_input)

        if clauses:
            result = resolution_solver(clauses)
            print("🧠 Result:", result)
    else:
        print("Invalid choice.")
