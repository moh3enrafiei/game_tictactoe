import numpy as np
import math
import random

# Function to check if any player has won
def check_win(board, player):
    # Check rows
    for i in range(3):
        if board[i][0] == player and board[i][1] == player and board[i][2] == player:
            return True
    # Check columns
    for j in range(3):
        if board[0][j] == player and board[1][j] == player and board[2][j] == player:
            return True
    # Check diagonals
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        return True
    # No win
    return False

# Function to check if game is a draw
def check_draw(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return False
    return True

# Function to get empty places on the board
def empty_places(board):
    return np.argwhere(board == 0)

# Function to get human player's move
def human_move(board):
    while True:
        row = int(input("Enter row (0, 1, or 2): "))
        col = int(input("Enter column (0, 1, or 2): "))
        if board[row][col] != 0:
            print("Invalid move, try again.")
        else:
            return row, col

# Function to get computer player's move
def computer_move(board, player):
    opponent = 3 - player
    # Check for winning move
    for move in empty_places(board):
        new_board = board.copy()
        new_board[move[0], move[1]] = player
        if check_win(new_board, player):
            return move
    # Check for blocking opponent's winning move
    for move in empty_places(board):
        new_board = board.copy()
        new_board[move[0], move[1]] = opponent
        if check_win(new_board, opponent):
            return move
    # Otherwise, use minimax algorithm to determine move
    move = minimax(board, player, 3, True)[1]
    return move

# Function to evaluate board for minimax algorithm
def minimax(board, player, depth, is_maximizing):
    # Base case: check for terminal state
    if check_win(board, player):
        return 1, None
    elif check_win(board, 3 - player):
        return -1, None
    elif check_draw(board):
        return 0, None
    # Recursive case: evaluate possible moves
    if is_maximizing:
        best_score = -math.inf
        for move in empty_places(board):
            new_board = board.copy()
            new_board[move[0], move[1]] = player
            score, _ = minimax(new_board, player, depth-1, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move
    else:
        best_score = math.inf
        for move in empty_places(board):
            new_board = board.copy()
            new_board[move[0], move[1]] = 3 - player
            score, _ = minimax(new_board, player, depth-1, True)
            if score < best_score:
                best_score = score
                best_move = move
        return best_score, best_move

def get_player_char(player):
    if player == 1:
        return "O"
    else:
        return "X"
        
def get_board_str(board):
    board_str = ""
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board_str += " "
            else:
                board_str += get_player_char(board[i][j])
            if j < 2:
                board_str += "|"
        board_str += "\n"
        if i < 2:
            board_str += "-+-+-\n"
    return board_str
def print_board(board):
    print(get_board_str(board))
def play_game():
    # Initialize game
    board = np.zeros((3, 3), dtype=int)
    players = [1, 2]
    random.shuffle(players)
    print("Starting tic-tac-toe game!")
    print(f"Player {get_player_char(players[0])} goes first.")
    # Main game loop
    while True:
        # Human player's turn
        if players[0] == 1:
            print("Your turn!")
            row, col = human_move(board)
            board[row, col] = 1
        # Computer player's turn
        else:
            print("Computer's turn...")
            row, col = computer_move(board, 2)
            board[row, col] = 2
            print(f"Computer played at row {row}, column {col}.")
        # Check for game over
        if check_win(board, players[0]):
            print(f"Player {get_player_char(players[0])} wins!")
            break
        elif check_draw(board):
            print("Game is a draw.")
            break
        # Switch player turns
        players.reverse()
        # Print current board state
        print_board(board)
play_game()