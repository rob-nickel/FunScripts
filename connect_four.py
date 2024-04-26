import os
import random

def board_is_full(board):
    for i in range(len(board[0])):
        if board[0][i] == ' ':
            return False
    return True
def is_winning_piece(board, row, col):
    """Checks if the piece at (row, col) is part of the winning combination."""
    player = board[row][col]
    if player == ' ':
        return False

    # Only need to check in the directions where the piece is a part of a line of 4
    directions = []

    # Check horizontal
    if col >= 3 and board[row][col - 1] == player and board[row][col - 2] == player and board[row][col - 3] == player:
        directions.append('h')
    if col <= len(board[0]) - 4 and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
        directions.append('h')

    # Check vertical
    if row >= 3 and board[row - 1][col] == player and board[row - 2][col] == player and board[row - 3][col] == player:
        directions.append('v')

    # Check diagonals
    if row >= 3 and col >= 3 and board[row - 1][col - 1] == player and board[row - 2][col - 2] == player and board[row - 3][col - 3] == player:
        directions.append('d1')
    if row <= len(board) - 4 and col <= len(board[0]) - 4 and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
        directions.append('d1')
    if row >= 3 and col <= len(board[0]) - 4 and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
        directions.append('d2')
    if row <= len(board) - 4 and col >= 3 and board[row + 1][col - 1] == player and board[row + 2][col - 2] == player and board[row + 3][col - 3] == player:
        directions.append('d2')

    return len(directions) > 0 

def print_board(board):
    """Prints the current state of the Connect 4 board, highlighting the winning pieces."""
    for row in range(len(board)):
        for col in range(len(board[0])):
            piece = board[row][col]
            if piece != ' ' and is_winning_piece(board, row, col):
                print("\033[1;32m" + piece + "\033[0m", end=' ')  # Yellow highlight
            else:
                print(piece, end=' ')
        print()
    print("1 2 3 4 5 6 7")

def get_column_input(player, board):
    """Gets valid column input from the player."""
    while True:
        try:
            column = int(input(f"Player {player}, choose a column (1-7): "))
            if 1 <= column <= 7 and board[0][column - 1] == ' ':
                return column
            else:
                print("Invalid input. Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def check_win(board):
    """Checks if a player has won the game."""
    # Check horizontal wins
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] != ' ' and \
               board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3]:
                return board[row][col]

    # Check vertical wins
    for row in range(len(board) - 3):
        for col in range(len(board[0])):
            if board[row][col] != ' ' and \
               board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col]:
                return board[row][col]

    # Check diagonal wins (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] != ' ' and \
               board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]:
                return board[row][col]

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] != ' ' and \
               board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3]:
                return board[row][col]

    return ' '  # No winner yet

def get_computer_move(board):
    """Determines the computer's move"""
    # 1. Check for immediate computer wins
    for col in range(len(board[0])):
        if can_win(board, 'O', col):
            return col + 1

    # 2. Check for blocks (human player wins)
    for col in range(len(board[0])):
        if can_win(board, 'X', col):  
            return col + 1

    # 3. Play randomly
    valid_columns = [col + 1 for col in range(len(board[0])) if board[0][col] == ' ']
    return random.choice(valid_columns)

def can_win(board, player, col):
    """Checks if placing a piece in 'col' results in a win for 'player'"""
    temp = 0
    # Make a temporary move
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            temp = 1
            break
    if temp != 1:
        return False

    winner = check_win(board)

    # Undo the temporary move
    board[row][col] = ' ' 

    return winner == player


def main():
    # Example usage
    board = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]

    current_player = 'X'

    while True:
        if current_player == 'X':
            column = get_column_input(current_player, board)
        else:
            column = get_computer_move(board)

        # Add piece to column (gravity simulation)
        for i in range(len(board) - 1, -1, -1):
            if board[i][column - 1] == ' ':
                board[i][column - 1] = current_player
                break

        print_board(board)

        winner = check_win(board)
        if winner != ' ':
            print(f"Player {winner} has won!")
            break
        if board_is_full(board):
            print(f"It's a draw!")
            break


        # Switch players
        current_player = 'O' if current_player == 'X' else 'X'


if __name__ == "__main__":
    main()