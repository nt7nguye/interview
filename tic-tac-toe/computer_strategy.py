from typing import List, Tuple
from board import Piece


class TicTacToeStrategy:
    def __init__(self):
        pass

    def get_move(self, board: List[List[Piece]]) -> Tuple[int, int]:
        """Implement your strategy here"""
        for i in range(3):
            for j in range(3):
                if board[i][j] == Piece.EMPTY:
                    return (i, j)
        raise ValueError("No move found")
