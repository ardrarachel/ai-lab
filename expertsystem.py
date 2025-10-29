def solve_expert_system(facts, rule_base):
    """
    This is the "Inference Engine".
    It loops through the rules, firing any that match the facts.
    It stops when no new facts can be added.
    """
    new_fact_added = True
    while new_fact_added:
        new_fact_added = False
        
        for (conditions, new_fact) in rule_base:
            # Check if all conditions are in our set of facts
            if conditions.issubset(facts) and new_fact not in facts:
                # If they are, add the new fact!
                facts.add(new_fact)
                print(f"Fact Added: {new_fact}")
                new_fact_added = True
                break # Restart the loop
    
    return facts

# --- Main Program Execution ---
if __name__ == "__main__":

    # --- 1. The Rule Base (The "Doctor's" Knowledge) ---
    # Define simple "IF-THEN" rules for diagnosis.
    rules = [
        # General rules
        ({'fever'}, 'is_sick'),
        ({'cough'}, 'is_sick'),
        ({'headache'}, 'is_sick'),
        
        # Specific diagnosis rules
        ({'is_sick', 'fever', 'body_aches'}, 'has_flu'),
        ({'is_sick', 'runny_nose', 'sore_throat'}, 'has_cold'),
        ({'sneezing', 'itchy_eyes'}, 'has_allergies'),
    ]

    # --- 2. The Working Memory (The Patient's Symptoms) ---
    # We build our initial set of facts by asking the user.
    initial_facts = set()
    
    print("--- Simple Medical Diagnosis Expert System ---")
    print("Please answer yes/no (y/n) to the following symptoms:")

    # Define the questions that establish initial facts
    questions = {
        'fever': "Do you have a fever?",
        'body_aches': "Do you have body aches?",
        'cough': "Do you have a cough?",
        'runny_nose': "Do you have a runny nose?",
        'sore_throat': "Do you have a sore throat?",
        'headache': "Do you have a headache?",
        'sneezing': "Are you sneezing a lot?",
        'itchy_eyes': "Do you have itchy eyes?",
    }

    # Ask all questions and populate the initial facts
    for fact_name, question in questions.items():
        answer = input(f"  {question} (y/n): ").lower()
        if answer == 'y':
            initial_facts.add(fact_name)

    print("\n--- Initial Facts (Symptoms) ---")
    print(initial_facts)
    
    print("\n--- Running Inference Engine ---")
    # --- 3. Run the Inference Engine ---
    final_facts = solve_expert_system(initial_facts, rules)
    
    print("\n--- Final Deduced Facts ---")
    print(final_facts)
    
    # Check for a final diagnosis
    if 'has_flu' in final_facts:
        print("\nFinal Diagnosis: You likely have the Flu. 🤒")
    elif 'has_cold' in final_facts:
        print("\nFinal Diagnosis: You likely have a Cold. 🤧")
    elif 'has_allergies' in final_facts:
        print("\nFinal Diagnosis: You likely have Allergies. 🌼")
    elif 'is_sick' in final_facts:
        print("\nFinal Diagnosis: You seem to be sick, but I can't be more specific.")
    else:
        print("\nFinal Diagnosis: You seem healthy! 👍")