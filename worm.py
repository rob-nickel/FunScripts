# To run: python3 worm.py

import random
import time

def printGameBoard(game_board, path, fastest):
    for i in range(10):
        for j in range(10):
            if (i*10 + j) in path:
                if game_board[i][j] == 'W':
                    char = 'W'
                else:
                    char = 'O'
                if fastest:
                    print('\033[1;32m' + char + '\033[0m',end='')
                else:
                    print('\033[1;31m' + char + '\033[0m',end='')
            else:
                print(game_board[i][j],end='')
        print()

def isWall(index):
    if index // 10 != 0 and index // 10 != 9 and index % 10 != 0 and index % 10 != 9:
            return False
def edgeIndex():
    while True:
        index = random.choice(range(35))
        if index == 0 or index == 9 or index == 26:
            continue
        elif index < 11:
            return index
        elif index > 24:
            return index + 64
        elif index % 2 == 0:
            return (((index - 10) * 5) + 10)
        else:
            return (((index - 9) * 5) + 9)
def finishIndex():
    while True:
        index = random.choice(range(100))
        if index // 10 != 0 and index // 10 != 9 and index % 10 != 0 and index % 10 != 9:
            return index

def create_path_bfs(game_board, entrance_index):
    queue = []
    queue.append([entrance_index]) # Enqueue

    while not len(queue) == 0:
        path = queue[0] # Dequeue
        queue.pop(0)
        current_index = path[len(path)-1]

        if game_board[current_index // 10][current_index % 10] == 'W':
            return path
        
        for dIndex in [-10, -1, 1, 10]: # Possible moves
            next_index = current_index + dIndex
            next_x, next_y = next_index // 10, next_index % 10
            if next_index not in path and next_x > 0 and next_y > 0 and next_x < 9 and next_y < 9:
                new_path = list(path)
                new_path.append(next_index)
                queue.append(new_path) # Enqueue

def create_path_dfs(game_board, entrance_index):
    stack = []
    stack.append([entrance_index]) # push

    while not len(stack) == 0:
        path = stack[len(stack)-1] # pop
        stack.pop(len(stack)-1)
        current_index = path[len(path)-1]

        if game_board[current_index // 10][current_index % 10] == 'W':
            return path
        
        for dIndex in [-10, -1, 10, 1]: # Possible moves
            next_index = current_index + dIndex
            next_x, next_y = next_index // 10, next_index % 10
            if next_index not in path and next_x > 0 and next_y > 0 and next_x < 9 and next_y < 9:
                new_path = list(path)
                new_path.append(next_index)
                stack.append(new_path) # Enqueue

def generate_valid_game_board():
    # Create a 10x10 array of characters initially filled with 'X' (walls)
    game_board = [['X'] * 10 for _ in range(10)]

    # Choose a random index for the finish line (inside the grid)
    finish_line_index = finishIndex()
    game_board[finish_line_index // 10][finish_line_index % 10] = 'W'

    # Choose a random index for the entrance
    entrance_index = edgeIndex()
    game_board[entrance_index // 10][entrance_index % 10] = 'O'

    print(f"Start: {entrance_index} and Finish: {finish_line_index}")
    return game_board, entrance_index


def main():
    game_board, entrance_index = generate_valid_game_board()

    # Create a DFS path from the entrance to the finish line
    start_time = time.time()
    dfs_path = create_path_dfs(game_board, entrance_index)
    dfs_time = time.time() - start_time

    # Create a BFS path from the entrance to the finish line
    start_time = time.time()
    bfs_path = create_path_bfs(game_board, entrance_index)
    bfs_time = time.time() - start_time

    # Print the game board
    print(f"DFS: {dfs_path}")
    printGameBoard(game_board, dfs_path, (dfs_time < bfs_time))
    print(f"BFS: {bfs_path}")
    printGameBoard(game_board, bfs_path, (dfs_time > bfs_time))

main()