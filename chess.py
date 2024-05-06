# To run: python3 chess.py

import random
from enum import Enum
import pygame
import sys

# Set up the screen
pygame.init()
screen_width = 600
screen_height = 400
screen = pygame.display
screen.set_caption("Chess!")
surface = screen.set_mode([screen_width, screen_height])
light_brown = (205, 133, 63)
dark_brown = (139, 69, 19)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
history = []
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
def get_king_location(board, color):
    for x in range(8):
        for y in range(8):
            if board[y][x] and board[y][x].kind == "king" and board[y][x].color == color:
                return (y, x)
    return None
def would_king_be_under_attack(board, from_location, to_location, color):
    print(f"Under Attack?? {color} {from_location} {to_location}")
    if from_location is None or to_location is None or color is None:
        return False
    current_piece = board[from_location[0]][from_location[1]]
    moving_king = False
    if current_piece.kind == "king":
        moving_king = True
        king_location = current_piece.current
    else:
        king_location = get_king_location(board, color)

    for x in range(8):
        for y in range(8):
            if (y, x) == from_location or (y, x) == to_location:
                continue
            piece = board[y][x]  # Assuming your board has pieces
            if piece == None:
                continue
            if piece.kind == "king" :
                continue
            if piece.color != color: 
                seen_squares = piece.get_seen_squares(board)
                print(f"seen squares: {seen_squares}")
                if moving_king and seen_squares and (to_location) in seen_squares:
                    print(f"Killed by {piece.kind} at {piece.current}")
                    return True
                if not moving_king:
                    fake_board = [row[:] for row in board]
                    fake_board[to_location[0]][to_location[1]] = fake_board[from_location[0]][from_location[1]]
                    fake_board[from_location[0]][from_location[1]] = None
                    seen_squares = piece.get_seen_squares(fake_board)
                    if seen_squares and king_location in seen_squares:
                        print(f"King killed by {piece.kind} at {piece.current}")
                        return True
    return False
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
    def get_seen_squares(self, board):
        seen_squares = []
        y, x = self.current
        # Check all 8 directions around the king, within board boundaries
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0: 
                    continue  # Skip the current position
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:  
                    # If same color piece...
                    if board[new_y][new_x] != None:
                        if board[new_y][new_x].color == self.color:
                            continue
                    seen_squares.append((new_y, new_x))
       
        return seen_squares
    def get_possible_moves(self, board):
        possible_moves = self.get_seen_squares(board)
        # Check for Castling
        if not self.has_moved:
            y, x = self.current[0], self.current[1]
            for new_x in [0, 7]:
                piece = board[y][new_x]
                if piece and piece.kind == "rook" and piece.color == self.color and not piece.has_moved:
                    if new_x == 0:
                        if board[y][1] == None and board[y][2] == None and board[y][3] == None:
                            possible_moves.append((y, 2))
                    if new_x == 7:
                        if board[y][5] == None and board[y][6] == None:
                            possible_moves.append((y, 6))
        return possible_moves
    def get_valid_moves(self, board):
        # All possible moves unless the new spot would be in check.
        valid_moves = self.get_possible_moves(board)
        moves_to_remove = []
        y, x = self.current
        print(f"{valid_moves} and ({y}, {x})")
        
        if valid_moves:
            for move in valid_moves:
                print(f"Trying move {move}. Valid_moves at this point: {valid_moves} length: {len(valid_moves)} and abs = {abs(move[1] - x)}")
                if would_king_be_under_attack(board, self.current, move, self.color):
                    moves_to_remove.append(move)
                elif abs(move[1] - x) == 2:
                    print("Checking castle location.")
                    if move[1] == 2:
                        if would_king_be_under_attack(board, self.current, (y, 3), self.color):
                            moves_to_remove.append(move)
                    elif move[1] == 6:
                        if would_king_be_under_attack(board, self.current, (y, 5), self.color):
                            moves_to_remove.append(move)
        if moves_to_remove:
            for move in moves_to_remove:
                valid_moves.remove(move)
        return valid_moves
    
    def is_under_attack(self, board):
        location = self.current
        for x in range(8):
            for y in range(8):
                if location != (y, x) and self.current != (y, x):
                    piece = board[y][x]  # Assuming your board has pieces
                    if piece and piece.color != self.color: 
                        if (location) in piece.get_valid_moves(board):
                            return True
        return False
class Queen(Piece):
    def __init__(self, color, start):
        if color == Color.BLACK:
            super().__init__("quee", Color.BLACK, start, start, b_queen_image, False, 9)
        else:
            super().__init__("quee", Color.WHITE, start, start, w_queen_image, False, 9)
    def get_seen_squares(self, board):
        seen_squares = []
        y, x = self.current

        # Horizontal and vertical movement
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            dx, dy = direction
            new_x, new_y = x + dx, y + dy
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                # Add move if empty or has enemy piece...
                if board[new_y][new_x] == None:
                    seen_squares.append((new_y, new_x))
                elif board[new_y][new_x].color != self.color:
                    seen_squares.append((new_y, new_x))
                    break
                elif board[new_y][new_x].color == self.color:
                    break
                new_x += dx
                new_y += dy
                
        # Diagonal movement
        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            dx, dy = direction
            new_x, new_y = x + dx, y + dy
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                # Add move if empty or has enemy piece...
                if board[new_y][new_x] == None:
                    seen_squares.append((new_y, new_x))
                elif board[new_y][new_x].color != self.color:
                    seen_squares.append((new_y, new_x))
                    break
                elif board[new_y][new_x].color == self.color:
                    break
                new_x += dx
                new_y += dy
        return seen_squares
    def get_possible_moves(self, board):
        return self.get_seen_squares(board)
    def get_valid_moves(self, board):
        valid_moves = self.get_possible_moves(board)
        print(f"Quee's moves: {valid_moves}")
        moves_to_remove = []
        if valid_moves:
            for move in valid_moves:
                if would_king_be_under_attack(board, self.current, move, self.color):
                    moves_to_remove.append(move)
        if moves_to_remove:
            for move in moves_to_remove:
                valid_moves.remove(move)
        
        #print(f"Quee's moves: {valid_moves}")
        return valid_moves
class Rook(Piece):
    def __init__(self, color, start):
        if color == Color.BLACK:
            super().__init__("rook", Color.BLACK, start, start, b_rook_image, False, 5)
        else:
            super().__init__("rook", Color.WHITE, start, start, w_rook_image, False, 5)
    def get_seen_squares(self, board):
        seen_squares = []
        y, x = self.current

        # Horizontal and vertical movement
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            dx, dy = direction
            new_x, new_y = x + dx, y + dy
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                # Add move if empty or has enemy piece...
                if board[new_y][new_x] == None:
                    seen_squares.append((new_y, new_x))
                elif board[new_y][new_x].color != self.color:
                    seen_squares.append((new_y, new_x))
                    break
                elif board[new_y][new_x].color == self.color:
                    break
                new_x += dx
                new_y += dy
        return seen_squares
    def get_possible_moves(self, board):
        return self.get_seen_squares(board)
    def get_valid_moves(self, board):
        valid_moves = self.get_possible_moves(board)        
        moves_to_remove = []
        if valid_moves:
            for move in valid_moves:
                if would_king_be_under_attack(board, self.current, move, self.color):
                    moves_to_remove.append(move)
        if moves_to_remove:
            for move in moves_to_remove:
                valid_moves.remove(move)
        #print(f"Rook's moves: {valid_moves}")
        return valid_moves
class Knight(Piece):
    def __init__(self, color, start):
        if color == Color.BLACK:
            super().__init__("knig", Color.BLACK, start, start, b_knight_image, False, 3)
        else:
            super().__init__("knig", Color.WHITE, start, start, w_knight_image, False, 3)
    def get_seen_squares(self, board):
        seen_squares = []
        y, x = self.current

        # All possible L-shaped moves
        for dx in [2, 1, -1, -2]:
            for dy in [2, 1, -1, -2]:
                if abs(dx) == abs(dy):
                    continue
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    # Add move if empty or has enemy piece...
                    if board[new_y][new_x] != None:
                        if board[new_y][new_x].color == self.color:
                            continue
                    seen_squares.append((new_y, new_x))
        return seen_squares
    def get_possible_moves(self, board):
        return self.get_seen_squares(board)
    def get_valid_moves(self, board):
        valid_moves = self.get_possible_moves(board)
        moves_to_remove = []
        if valid_moves:
            for move in valid_moves:
                if would_king_be_under_attack(board, self.current, move, self.color):
                    moves_to_remove.append(move)
        if moves_to_remove:
            for move in moves_to_remove:
                valid_moves.remove(move)
        #print(f"Knig's moves: {valid_moves}")
        return valid_moves
class Bishop(Piece):
    def __init__(self, color, start):
        if color == Color.BLACK:
            super().__init__("bish", Color.BLACK, start, start, b_bishop_image, False, 3)
        else:
            super().__init__("bish", Color.WHITE, start, start, w_bishop_image, False, 3)
    def get_seen_squares(self, board):
        seen_squares = []
        y, x = self.current
        # Diagonal movement
        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            dx, dy = direction
            new_x, new_y = x + dx, y + dy
            while 0 <= new_x < 8 and 0 <= new_y < 8:
                # Add move if empty or has enemy piece...
                if board[new_y][new_x] == None:
                    seen_squares.append((new_y, new_x))
                elif board[new_y][new_x].color != self.color:
                    seen_squares.append((new_y, new_x))
                    break
                elif board[new_y][new_x].color == self.color:
                    break
                new_x += dx
                new_y += dy
        return seen_squares
    def get_possible_moves(self, board):
        return self.get_seen_squares(board)
    def get_valid_moves(self, board):
        valid_moves = self.get_possible_moves(board)
        moves_to_remove = []
        if valid_moves:
            for move in valid_moves:
                if would_king_be_under_attack(board, self.current, move, self.color):
                    moves_to_remove.append(move)
        if moves_to_remove:
            for move in moves_to_remove:
                valid_moves.remove(move)
        # print(f"Bish's moves: {valid_moves}")
        return valid_moves
class Pawn(Piece):
    def __init__(self, color, start):
        if color == Color.BLACK:
            super().__init__("pawn", Color.BLACK, start, start, b_pawn_image, False, 1)
        else:
            super().__init__("pawn", Color.WHITE, start, start, w_pawn_image, False, 1)

    def get_seen_squares(self, board):
        seen_squares = []
        y, x = self.current
        direction = 1 if self.color == Color.BLACK else -1  # Forward based on color
        # Diagonal captures
        for dx in [-1, 1]:
            new_x, new_y = x + dx, y + direction
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                seen_squares.append((new_y, new_x))
        return seen_squares
    def get_possible_moves(self, board):
        seen_squares = self.get_seen_squares(board)
        possible_moves = []
        y, x = self.current
        direction = 1 if self.color == Color.BLACK else -1  # Forward based on color
        print(f"Pawn seen squares: {seen_squares}")
        for move in seen_squares:
            if board[move[0]][move[1]]!= None and board[move[0]][move[1]].color != self.color:
                possible_moves.append(move)
            elif board[move[0]][move[1]]== None and (y == 3 and self.color == Color.WHITE) or (y == 4 and self.color == Color.BLACK):
                # En Passant
                global history
                print(f"History: {len(history)} {history}")
                history_string = history[len(history)-1]
                print(f"Testing En Passant: {history_string[13]} {history_string[23]} {history_string[16]}")
                if "pawn" not in history_string:
                    continue
                original_y = history_string[13]
                new_y = history_string[23]
                if not original_y.isdigit() or not new_y.isdigit():
                    continue
                if abs(int(original_y) - int(new_y)) != 2:
                    continue
                if history_string[16].isdigit() and int(history_string[16]) == move[1]:
                    possible_moves.append(move)

        # One step forward
        new_y = y + direction
        if 0 <= new_y < 8:
            if board[new_y][x] == None:
                # Add move if empty
                possible_moves.append((new_y, x))

                # Two steps forward on the first move
                if self.start == self.current:
                    new_y = new_y + direction
                    if 0 <= new_y < 8 and board[new_y][x] == None:
                        possible_moves.append((new_y, x))

        return possible_moves
    def get_valid_moves(self, board):
        valid_moves = self.get_possible_moves(board)
        moves_to_remove = []
        if valid_moves:
            for move in valid_moves:
                if would_king_be_under_attack(board, self.current, move, self.color):
                    moves_to_remove.append(move)
        if moves_to_remove:
            for move in moves_to_remove:
                valid_moves.remove(move)
        # print(f"Pawn's moves: {valid_moves}")
        return valid_moves
def draw_board(surface):
    square_size = 50
    for row in range(8):
        for col in range(10):
            color = light_brown if (row + col) % 2 == 0 else dark_brown
            pygame.draw.rect(surface, color, (col * square_size, row * square_size, square_size, square_size))
    color = dark_brown
    pygame.draw.rect(surface, color, (square_size * 8, 0, square_size * 4, screen_height))
def draw_history(surface, history):
    font = pygame.font.Font(None, 14)
    start_index = max(0, len(history) - 20)
    # Draw move history on the right column
    for i in range(start_index, len(history)):
        move = f"{i+1}. {history[i]}"
        text_surface = font.render(move, True, white)
        text_rect = text_surface.get_rect(midright=(screen_width - 1, 105 + (i - start_index) * 15))  # Adjust the y position for each move
        surface.blit(text_surface, text_rect)
def draw_buttons(surface, one_player, turn):
    # Font settings
    font = pygame.font.Font(None, 20)
    if turn == Color.WHITE:
        turn_text = "White's Turn"
        turn_button = font.render(turn_text, True, black)
        turn_rect = turn_button.get_rect(center=(screen_width - 100, 10))
        pygame.draw.rect(surface, white, turn_rect)
    else:
        turn_text = "Black's Turn"
        turn_button = font.render(turn_text, True, white)
        turn_rect = turn_button.get_rect(center=(screen_width - 100, 10))
        pygame.draw.rect(surface, black, turn_rect)
    surface.blit(turn_button, turn_rect)

    font = pygame.font.Font(None, 24)
    # New game button
    new_game_text = "New Game"
    new_game_button = font.render(new_game_text, True, white)
    new_game_rect = new_game_button.get_rect(center=(screen_width - 100, 28))
    pygame.draw.rect(surface, (0, 128, 0), new_game_rect)
    surface.blit(new_game_button, new_game_rect)
    # Toggle button
    if one_player:
        toggle_text = "1-Player"
    else:
        toggle_text = "2-Player"
    toggle_button = font.render(toggle_text, True, white)
    toggle_rect = toggle_button.get_rect(center=(screen_width - 100, 50))
    pygame.draw.rect(surface, (0, 128, 0), toggle_rect)
    surface.blit(toggle_button, toggle_rect)
    # Undo button
    undo_text = "Undo Move"
    undo_button = font.render(undo_text, True, white)
    undo_rect = undo_button.get_rect(center=(screen_width - 100, 75))
    pygame.draw.rect(surface, (0, 128, 0), undo_rect)
    surface.blit(undo_button, undo_rect)
def draw_pieces(surface, board):
    square_size = 50
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                image = piece.image
                surface.blit(image, (col*square_size, row*square_size))
def draw_highlighted_moves(surface, highlighted_moves):
    square_size = 50
    if highlighted_moves:
        for move in highlighted_moves:
            y, x = move
            pygame.draw.circle(surface, red, (x * square_size + 25, y * square_size + 25), 5)
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
    black_king = board[0][4]
    white_king = board[7][4]
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
def get_clicked_space(mouse_pos, board):
    (click_x, click_y) = mouse_pos
    if click_x > 400:
        if click_y >= 15 and click_y <= 30:
            return("New Game")
        if click_y >= 40 and click_y <= 65:
            return("Toggle Player")
        if click_y >= 65 and click_y <= 90:
            return("Undo")
        else:
            return(None)
    return (int(click_y / 50),int(click_x / 50))
def toggle_color(color):
    if color == Color.WHITE:
        return Color.BLACK
    return Color.WHITE
def main():
    # Initial setup
    board = setup_initial_board()
    one_player = False
    turn = Color.WHITE
    piece_selected_space = None
    highlighted_moves = []
    global history
    print_board(board)
    draw_board(surface)
    draw_buttons(surface, one_player, turn)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
                mouse_pos = pygame.mouse.get_pos()
                selected_space = get_clicked_space(mouse_pos, board)
                print(selected_space)
                if selected_space == "New Game":
                    board = setup_initial_board()
                    turn = Color.WHITE
                    piece_selected_space = None
                    history = []
                    highlighted_moves = []
                    draw_board(surface)
                    draw_buttons(surface, one_player, turn)
                    continue
                elif selected_space == "Toggle Player":
                    if one_player == False:
                        one_player = True
                    else:
                        one_player = False
                    draw_buttons(surface, one_player, turn)
                elif selected_space == "Undo":
                    # TODO: Undo
                    continue
                elif selected_space == None:
                    #clicked on no buttons in the column
                    continue
                else:
                    print("piece selected")
                    if piece_selected_space != None:
                        # Piece currently highlighted:
                        # - - If selection is a valid move, move piece, flip turn.
                        # - - clear selection, clear highlights
                        print(f"Trying to move {piece_selected_space} to {selected_space}. {highlighted_moves} are allowed.")
                        if highlighted_moves and selected_space in highlighted_moves:
                            history_string = f"{piece_selected_space.color} {piece_selected_space.kind} from {piece_selected_space.current} to {selected_space}"
                            castling = False
                            en_passant = False
                            if piece_selected_space.kind == "king" and (abs(piece_selected_space.current[1] - selected_space[1]) == 2):
                                history_string = f"{history_string} castling"
                                castling = True
                            else: 
                                if piece_selected_space.kind == "pawn" and board[selected_space[0]][selected_space[1]] == None and selected_space[1] != piece_selected_space.current[1]:
                                    en_passant = True
                                    history_string = f"{history_string} killing pawn"
                                elif board[selected_space[0]][selected_space[1]] != None:
                                    history_string = f"{history_string} killing {board[selected_space[0]][selected_space[1]].kind}"
                            print(history_string)
                            turn = toggle_color(turn)
                            board[selected_space[0]][selected_space[1]] = piece_selected_space
                            if castling:
                                if selected_space[1] == 2:
                                    board[selected_space[0]][3] = board[selected_space[0]][0]
                                    board[selected_space[0]][0] = None
                                    board[selected_space[0]][3].has_moved = True
                                elif selected_space[1] == 6:
                                    board[selected_space[0]][5] = board[selected_space[0]][7]
                                    board[selected_space[0]][7] = None
                                    board[selected_space[0]][5].has_moved = True
                            elif en_passant:
                                if piece_selected_space.color == Color.WHITE:
                                    board[(selected_space[0]+1)][selected_space[1]] = None
                                else:
                                    board[(selected_space[0]-1)][selected_space[1]] = None
                            piece_selected_space.has_moved = True
                            board[piece_selected_space.current[0]][piece_selected_space.current[1]] = None
                            piece_selected_space.current = selected_space
                            history.append(history_string)
                            print(f"piece moved! New turn: {turn}")
                        highlighted_moves = []
                        piece_selected_space = None
                        print("piece unselected")
                    else:
                        # no piece currently highlighted:
                        # - - If selection is a piece of the correct color, highlight possible moves, refresh board
                        piece_selected_space = board[selected_space[0]][selected_space[1]]
                        print(piece_selected_space)
                        if piece_selected_space != None:
                            if piece_selected_space.color == turn:
                                highlighted_moves = piece_selected_space.get_valid_moves(board)
                                print(f"possible moves: {highlighted_moves}")
                        if highlighted_moves == []:
                            piece_selected_space = None

                    # - refresh board
                    #continue
        draw_board(surface)
        draw_history(surface, history)
        draw_buttons(surface, one_player, turn)
        draw_pieces(surface, board)
        draw_highlighted_moves(surface, highlighted_moves)
        pygame.display.flip()
        # draw_pieces(surface, board)
        # screen.update()
    pygame.quit()                                                                                           
    sys.exit() 


main()