# To run: python3 chess.py

import random
from enum import Enum
import pygame
import sys


# Set up the screen
pygame.init()
screen_width = 400
screen_height = 400
screen = pygame.display
screen.set_caption("Chess!")
surface = screen.set_mode([screen_width, screen_height])
light_brown = (205, 133, 63)
dark_brown = (139, 69, 19)
# Load images (you'll need to replace with your filepaths)
w_king_image = pygame.image.load("images/king_w.png").convert_alpha()  
w_queen_image = pygame.image.load("images/queen_w.png").convert_alpha()  
w_rook_image = pygame.image.load("images/rook_w.png").convert_alpha() 
w_knight_image = pygame.image.load("images/knight_w.png").convert_alpha()  
w_bishop_image = pygame.image.load("images/bishop_w.png").convert_alpha()  
w_pawn_image = pygame.image.load("images/pawn_w.png").convert_alpha()  
b_king_image = pygame.image.load("images/king_b.png").convert_alpha()  
b_queen_image = pygame.image.load("images/queen_b.png").convert_alpha()  
b_rook_image = pygame.image.load("images/rook_b.png").convert_alpha() 
b_knight_image = pygame.image.load("images/knight_b.png").convert_alpha()  
b_bishop_image = pygame.image.load("images/bishop_b.png").convert_alpha()  
b_pawn_image = pygame.image.load("images/pawn_b.png").convert_alpha()  



class Color(Enum):
    BLACK = "b"
    WHITE = "w"
    
    def __str__(self):
        return self.value
class Piece:
    def __init__(self, kind, color, start, current, image, has_moved, value):
        self.kind = kind
        self.color = color
        self.start = start
        self.current = current
        self.image = image
        self.has_moved = has_moved
        self.value = value
class King(Piece):
    def __init__(self, color, start):
        if color == Color.BLACK:
            super().__init__("king", Color.BLACK, start, start, b_king_image, False, 100)
        else:
            super().__init__("king", Color.WHITE, start, start, w_king_image, False, 100)
        
    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.current

        # Check all 8 directions around the king, within board boundaries
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0: 
                    continue  # Skip the current position
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:  
                    # TODO: Check if pieces of same color are here
                    # TODO: Check if moving into check
                    valid_moves.append((x,y))

        #if self.current == self.start:
            # TODO: add castling
        return valid_moves
    
    def is_under_attack(self, board):
        for x in range(8):
            for y in range(8):
                piece = board[x][y]  # Assuming your board has pieces
                if piece and piece.color != self.color: 
                    if (self.current) in piece.get_valid_moves(board):
                        return True
        return False
class Queen(Piece):
    def __init__(self, color, start):
        if color == Color.BLACK:
            super().__init__("quee", Color.BLACK, start, start, b_queen_image, False, 9)
        else:
            super().__init__("quee", Color.WHITE, start, start, w_queen_image, False, 9)

    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.current

        # Horizontal and vertical movement
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            dx, dy = direction
            new_x, new_y = x + dx, y + dy
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                # TODO: Check if pieces of same color are here and break

                # Add move if empty or has enemy piece...
                valid_moves.append((new_x, new_y))

                # TODO: Check if enemy piece is here and break

                new_x += dx
                new_y += dy
                

        # Diagonal movement
        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            dx, dy = direction
            new_x, new_y = x + dx, y + dy
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                # TODO: Check if pieces of same color are here and break

                # Add move if empty or has enemy piece...
                valid_moves.append((new_x, new_y))

                # TODO: Check if enemy piece is here and break
                new_x += dx
                new_y += dy

        return valid_moves
class Rook(Piece):
    def __init__(self, color, start):
        if color == Color.BLACK:
            super().__init__("rook", Color.BLACK, start, start, b_rook_image, False, 5)
        else:
            super().__init__("rook", Color.WHITE, start, start, w_rook_image, False, 5)

    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.current

        # Horizontal and vertical movement
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            dx, dy = direction
            new_x, new_y = x + dx, y + dy
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                # TODO: Check if pieces of same color are here and break

                # Add move if empty or has enemy piece...
                valid_moves.append((new_x, new_y))

                # TODO: Check if enemy piece is here and break

                new_x += dx
                new_y += dy

        return valid_moves
class Knight(Piece):
    def __init__(self, color, start):
        if color == Color.BLACK:
            super().__init__("knig", Color.BLACK, start, start, b_knight_image, False, 3)
        else:
            super().__init__("knig", Color.WHITE, start, start, w_knight_image, False, 3)

    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.current

        # All possible L-shaped moves
        for dx in [2, 1, -1, -2]:
            for dy in [2, 1, -1, -2]:
                if abs(dx) == abs(dy):
                    continue
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    # TODO: Check if pieces of same color are here and break

                    # Add move if empty or has enemy piece...
                    valid_moves.append((new_x, new_y))

        return valid_moves
class Bishop(Piece):
    def __init__(self, color, start):
        if color == Color.BLACK:
            super().__init__("bish", Color.BLACK, start, start, b_bishop_image, False, 3)
        else:
            super().__init__("bish", Color.WHITE, start, start, w_bishop_image, False, 3)
    
    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.current                

        # Diagonal movement
        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            dx, dy = direction
            new_x, new_y = x + dx, y + dy
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                # TODO: Check if pieces of same color are here and break

                # Add move if empty or has enemy piece...
                valid_moves.append((new_x, new_y))

                # TODO: Check if enemy piece is here and break
                new_x += dx
                new_y += dy

        return valid_moves
class Pawn(Piece):
    def __init__(self, color, start):
        if color == Color.BLACK:
            super().__init__("pawn", Color.BLACK, start, start, b_pawn_image, False, 1)
        else:
            super().__init__("pawn", Color.WHITE, start, start, w_pawn_image, False, 1)

    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.current
        direction = 1 if self.color == Color.BLACK else -1  # Forward based on color

        # One step forward
        new_y = y + direction
        if 0 <= new_y < 8:
            # TODO: Check if pieces are here and break

            # Add move if empty or has enemy piece...
            valid_moves.append((x, new_y))

            # Two steps forward on the first move
            if self.start == self.current:
                new_y = y + direction
                if 0 <= new_y < 8:
                    # TODO: Check if pieces are here and break

                    # Add move if empty or has enemy piece...
                    valid_moves.append((x, new_y))

        # Diagonal captures
        for dx in [-1, 1]:
            new_x, new_y = x + dx, y + direction
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                # TODO: Check if pieces of other color   
                valid_moves.append((new_x, new_y))
                # TODO: Check en passant
                #valid_moves.append((new_x, new_y))
        return valid_moves
def draw_board(surface):
    square_size = 50
    for row in range(8):
        for col in range(8):
            color = light_brown if (row + col) % 2 == 0 else dark_brown
            pygame.draw.rect(surface, color, (col * square_size, row * square_size, square_size, square_size))
def draw_pieces(surface, board):
    square_size = 50
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                image = piece.image
                surface.blit(image, (col*square_size, row*square_size))
def setup_initial_board():
    board = []

    # Create rows
    for row in range(8):
        board.append([None] * 8)  # Initialize an empty row

    # Set up pieces (rows 0 and 7)
    for col in range(8):
        for row in [0, 1, 6, 7]:
            if row < 4:
                color = Color.BLACK
            else:
                color = Color.WHITE

            if (row == 1) or (row == 6):
                board[row][col] = Pawn(color, (row, col))
            elif (col == 0) or (col == 7):
                board[row][col] = Rook(color, (row, col))
            elif (col == 1) or (col == 6):
                board[row][col] = Knight(color, (row, col))
            elif (col == 2) or (col == 5):
                board[row][col] = Bishop(color, (row, col))
            elif (col == 3):
                board[row][col] = Queen(color, (row, col))
            elif (col == 4):
                board[row][col] = King(color, (row, col))
            else:
                print(f"Oops! ({row}, {col})")

    return board
def print_board(board):
    for row in board:
        for col in row:
            if col != None:
                print(col.color, end="_")
                print(col.kind, end="\t")
            else: 
                print(" [  ]  ", end="\t")
        print()
def main():
    # Example usage:
    board = setup_initial_board()
    print_board(board)
    draw_board(surface)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_pieces(surface, board)
        screen.update()
    pygame.quit()                                                                                           
    sys.exit() 


main()