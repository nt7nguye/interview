# Write a program that plays every possible tic-tac-toe game, and then prints the number of valid, completed games
from copy import deepcopy

empty_board = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]
seen = set()


def convert_to_string(board):
    s = ""
    for row in board:
        for node in row:
            s += node
        s += "\n"
    return s


def check_seen(board):
    """
    Check if we've seen this board.
    Convert to string, place it in set
    """
    s = convert_to_string(board)
    return s in seen


def find_next_board_states(board, current_player):
    # optimize this using some knowledge current state so far
    possible = []
    for i, row in enumerate(board):
        for j, node in enumerate(row):
            if node == "_":
                copied_board = deepcopy(board)
                copied_board[i][j] = current_player
                possible.append(copied_board)
    return possible


def check_completed(board, current_player):
    # check for win
    # row, col, dia
    for i in range(3):
        all_true = True
        for j in range(3):
            if board[i][j] != current_player:
                all_true = False
        if all_true:
            return True

    # Col
    for i in range(3):
        all_true = True
        for j in range(3):
            if board[j][i] != current_player:
                all_true = False
        if all_true:
            return True

    # Diag
    left_to_down_diag = True
    for i, j in [[0, 0], [1, 1], [2, 2]]:
        if board[i][j] != current_player:
            left_to_down_diag = False
    if left_to_down_diag:
        return True

    bottom_to_up_diag = True
    for i, j in [[0, 2], [1, 1], [2, 0]]:
        if board[i][j] != current_player:
            bottom_to_up_diag = False
    if bottom_to_up_diag:
        return True

    # If tie returns True
    if all(node != "_" for row in board for node in row):
        return True

    return False


## Core traversing logic
total_valid = 0
current_player = "X"
curr_nodes = [empty_board]
move_count = 0

while move_count < 9:
    next_nodes = []
    for curr_board in curr_nodes:
        for board in find_next_board_states(curr_board, current_player):
            if not check_seen(board):
                if check_completed(board, current_player):
                    total_valid += 1
                else:
                    next_nodes.append(board)
                seen.add(convert_to_string(board))

    curr_nodes = next_nodes
    current_player = "O" if current_player == "X" else "X"
    move_count += 1

print(total_valid)
