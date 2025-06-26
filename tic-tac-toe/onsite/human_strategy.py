from typing import List, Tuple
from board import Piece


class TicTacToeStrategy:
    def __init__(self, piece: Piece = Piece.O, opponent_piece: Piece = Piece.X):
        self.piece = piece
        self.opponent_piece = opponent_piece
        pass

    def get_move(self, board: List[List[Piece]]) -> Tuple[int, int]:
        """Implement your strategy here"""
        for i in range(3):
            for j in range(3):
                if board[i][j] == Piece.EMPTY:
                    return (i, j)
        raise ValueError("No move found")
