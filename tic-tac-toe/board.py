from enum import Enum
from typing import Tuple


class Piece(str, Enum):
    X = "X"
    O = "O"
    EMPTY = " "


class TicTacToeGame:
    def __init__(self):
        self.board = [[Piece.EMPTY for _ in range(3)] for _ in range(3)]

    def __str__(self):
        board_str = ""
        for row in self.board:
            board_str += "|".join(row) + "\n"
            board_str += "-----\n"
        return board_str

    def is_over(self) -> bool:
        return self.get_winner() is not None or self.is_full()

    def is_full(self) -> bool:
        return all(cell != Piece.EMPTY for row in self.board for cell in row)

    def get_winner(self) -> Piece | None:
        winning_combinations = [
            [self.board[0][0], self.board[0][1], self.board[0][2]],
            [self.board[1][0], self.board[1][1], self.board[1][2]],
            [self.board[2][0], self.board[2][1], self.board[2][2]],
            [self.board[0][0], self.board[1][0], self.board[2][0]],
            [self.board[0][1], self.board[1][1], self.board[2][1]],
            [self.board[0][2], self.board[1][2], self.board[2][2]],
            [self.board[0][0], self.board[1][1], self.board[2][2]],
            [self.board[0][2], self.board[1][1], self.board[2][0]],
        ]

        for combination in winning_combinations:
            if all(cell == Piece.X for cell in combination):
                return Piece.X
            if all(cell == Piece.O for cell in combination):
                return Piece.O
        return None

    def apply_move(self, move: Tuple[int, int], piece: Piece):
        if self.board[move[0]][move[1]] != Piece.EMPTY:
            raise ValueError(f"Cell {move} already occupied\n{str(self)}")
        self.board[move[0]][move[1]] = piece
