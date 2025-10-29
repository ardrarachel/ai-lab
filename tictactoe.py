import math  # Used for infinity (-math.inf, math.inf) in the Minimax algorithm.
import time  # Used to add a small delay to the AI's move.

# --- 1. Game Setup ---
# Define constants for the players' markers for clarity.
human_player = 'O'
ai_player = 'X'

def print_board(board):
    """Prints the Tic-Tac-Toe board to the console."""
    print("\n  0 1 2")  # Print column headers.
    for i, row in enumerate(board):
        # 'i' is the row index (0, 1, or 2).
        # 'row' is the list (e.g., ['X', ' ', 'O']).
        # ' | '.join(row) creates a string like "X |   | O".
        print(f"{i} {' | '.join(row)}")
        if i < 2:  # Print the horizontal separator after rows 0 and 1.
            print("  -----")
    print()  # Add an extra newline for spacing.

def get_empty_cells(board):
    """Returns a list of all empty cells (row, col) on the board."""
    cells = []  # Initialize an empty list to store coordinates.
    for i in range(3):  # Iterate through rows (0, 1, 2).
        for j in range(3):  # Iterate through columns (0, 1, 2).
            if board[i][j] == ' ':  # If the cell is empty...
                cells.append((i, j))  # ...add its (row, col) tuple to the list.
    return cells

def check_winner(board, player):
    """Checks if the specified 'player' has won the game."""
    
    # Check rows:
    for row in board:
        # 'all()' checks if every item in the list meets the condition.
        if all([cell == player for cell in row]):
            return True
            
    # Check columns:
    for col in range(3):
        # Check if all cells in a single column (e.g., [0][0], [1][0], [2][0]) match the player.
        if all([board[row][col] == player for row in range(3)]):
            return True
            
    # Check diagonals:
    # Check main diagonal (top-left to bottom-right).
    if all([board[i][i] == player for i in range(3)]):
        return True
    # Check anti-diagonal (top-right to bottom-left).
    if all([board[i][2 - i] == player for i in range(3)]):
        return True
        
    return False  # If no winning condition is met, return False.

def is_board_full(board):
    """Checks if the board is full (no empty cells left)."""
    # If the list of empty cells is empty, the board is full.
    return len(get_empty_cells(board)) == 0

def evaluate(board):
    """
    The utility function for Minimax. Assigns a score to a terminal board state.
    Returns +1 for AI win, -1 for human win, 0 for a draw.
    """
    if check_winner(board, ai_player):
        return 1  # AI (Maximizer) wins.
    elif check_winner(board, human_player):
        return -1  # Human (Minimizer) wins.
    else:
        return 0  # It's a draw.

# --- 2. Minimax AI Algorithm ---

def minimax(board, depth, alpha, beta, is_maximizing):
    """
    The core recursive function for the Minimax algorithm with alpha-beta pruning.
    'is_maximizing' is True if it's the AI's turn, False if it's the Human's.
    'alpha' is the best score the Maximizer can guarantee.
    'beta' is the best score the Minimizer can guarantee.
    """
    
    # --- Base Case: Game Over ---
    # If the game has a winner or is a draw, return the score from 'evaluate'.
    if check_winner(board, ai_player) or check_winner(board, human_player) or is_board_full(board):
        return evaluate(board)

    # --- Recursive Step: Maximizer's Turn (AI) ---
    if is_maximizing:
        best_value = -math.inf  # Initialize best value to negative infinity.
        
        # Try every possible empty cell.
        for row, col in get_empty_cells(board):
            board[row][col] = ai_player  # "Make" the hypothetical move.
            
            # Recursively call minimax for the *next* turn (which is the Minimizer's).
            value = minimax(board, depth + 1, alpha, beta, False)
            
            board[row][col] = ' '  # "Undo" the move (backtracking).
            best_value = max(best_value, value)  # Find the highest score.
            alpha = max(alpha, best_value)  # Update alpha.
            
            # --- Alpha-Beta Pruning ---
            if beta <= alpha:  # If beta is <= alpha, the Minimizer will never let this path happen.
                break  # Stop searching this branch.
        return best_value  # Return the best score the Maximizer can get.

    # --- Recursive Step: Minimizer's Turn (Human) ---
    else:
        best_value = math.inf  # Initialize best value to positive infinity.
        
        # Try every possible empty cell.
        for row, col in get_empty_cells(board):
            board[row][col] = human_player  # "Make" the hypothetical move.
            
            # Recursively call minimax for the *next* turn (which is the Maximizer's).
            value = minimax(board, depth + 1, alpha, beta, True)
            
            board[row][col] = ' '  # "Undo" the move (backtracking).
            best_value = min(best_value, value)  # Find the lowest score.
            beta = min(beta, best_value)  # Update beta.
            
            # --- Alpha-Beta Pruning ---
            if beta <= alpha:  # If beta is <= alpha, the Maximizer will never choose this path.
                break  # Stop searching this branch.
        return best_value  # Return the best score the Minimizer can force.

def find_best_move(board):
    """
    Finds the optimal move for the AI by evaluating all possible first moves.
    This function calls 'minimax' for each valid starting move.
    """
    best_move = (-1, -1)  # Initialize with an invalid move.
    best_value = -math.inf  # Initialize with the worst possible score for the AI.

    # Loop through all possible moves.
    for row, col in get_empty_cells(board):
        board[row][col] = ai_player  # Try this move.
        
        # Call minimax for the *opponent's* (Minimizer's) turn.
        # This tells us the score of the game *after* this move is made.
        move_value = minimax(board, 0, -math.inf, math.inf, False)
        
        board[row][col] = ' '  # Undo the move.

        # If this move results in a better score than our current best...
        if move_value > best_value:
            best_value = move_value  # ...update the best score.
            best_move = (row, col)  # ...update the best move.
            
    return best_move  # Return the coordinates of the best move.

# --- 3. Main Game Loop ---

# This standard Python check ensures this code only runs when the file is
# executed directly (not when imported as a module).
if __name__ == "__main__":
    
    # Initialize an empty 3x3 board (a list of 3 lists).
    game_board = [[' ' for _ in range(3)] for _ in range(3)]
    
    print("Welcome to Tic-Tac-Toe! You are 'O'.")

    # The main game loop, continues until a 'break' statement.
    while True:
        print_board(game_board)

        # --- Human's Turn ---
        # Check if the game is still playable.
        if not is_board_full(board=game_board) and not check_winner(game_board, ai_player):
            try:
                # Get the human's move, e.g., "1 2".
                move = input("Enter your move (row col): ")
                row, col = map(int, move.split())  # Split "1 2" into integers 1 and 2.
                
                if game_board[row][col] == ' ':  # If the chosen cell is empty...
                    game_board[row][col] = human_player  # ...place the human's 'O'.
                else:
                    print("This cell is already taken! Please try again.")
                    continue  # Skip the rest of the loop and ask for input again.
            except (ValueError, IndexError):
                # Catch invalid inputs like "abc" or "5 5".
                print("Invalid input. Please enter row and column as two numbers (e.g., '1 2').")
                continue  # Ask for input again.
        else:
            break  # Exit the 'while True' loop if the game is over.

        # Check for game over *after* the human's move.
        if check_winner(game_board, human_player) or check_winner(game_board, ai_player) or is_board_full(game_board):
            break

        # --- AI's Turn ---
        print("AI is thinking...")
        time.sleep(0.5)  # Add a small delay for dramatic effect.
        
        # Call the AI to find the best move.
        ai_row, ai_col = find_best_move(game_board)
        game_board[ai_row][ai_col] = ai_player  # Place the AI's 'X' on the board.
        print(f"AI chose: {ai_row} {ai_col}")

    # --- Game Over ---
    print("\n--- GAME OVER ---")
    print_board(game_board)  # Show the final board.
    
    # Evaluate the final board state to see who won.
    final_score = evaluate(game_board)
    if final_score == 1:
        print("AI ('X') wins! 🤖")
    elif final_score == -1:
        print("You ('O') win! 🎉")
    else:
        print("It's a draw! 🤝")