from typing import List, Tuple
from board import Piece


class TicTacToeStrategy:
    def __init__(
        self,
        piece: Piece = Piece.O,
        opponent_piece: Piece = Piece.X,
        opponent=None,
    ):
        self.piece = piece
        self.opponent_piece = opponent_piece

    def get_move(self, board: List[List[Piece]]) -> Tuple[int, int]:
        """Implement your strategy here"""
        rows = len(board)
        cols = len(board[0])

        # CHECK VERTICAL WINNING/LOSING MOVE
        for i in range(rows):
            count_mine = 0
            count_empty = 0
            count_opponent = 0
            empty_pieces = []
            for j in range(cols):
                if board[i][j] == self.piece:
                    count_mine += 1
                elif board[i][j] == self.opponent_piece:
                    count_opponent += 1

                elif board[i][j] == Piece.EMPTY:
                    empty_pieces.append((i, j))
                    count_empty += 1

            if count_mine == 2 and count_empty == 1:
                return empty_pieces[0]

            if count_opponent == 2 and count_empty == 1:
                return empty_pieces[0]

        # CHECK HORIZONTAL WINNNING/LOSING MOVE
        for j in range(cols):
            count_mine = 0
            count_empty = 0
            count_opponent = 0
            empty_pieces = []
            for i in range(rows):
                if board[i][j] == self.piece:
                    count_mine += 1
                elif board[i][j] == self.opponent_piece:
                    count_opponent += 1

                elif board[i][j] == Piece.EMPTY:
                    empty_pieces.append((i, j))
                    count_empty += 1

            if count_mine == 2 and count_empty == 1:
                return empty_pieces[0]

            if count_opponent == 2 and count_empty == 1:
                return empty_pieces[0]

        # CHECK DIAGONAL WINNNING/LOSING MOVE
        count_empty_diag = 0
        count_mine_diag = 0
        count_opponent_diag = 0
        empty_pieces_diag = []

        if board[0][0] == self.piece:
            count_mine_diag += 1
        elif board[0][0] == self.opponent_piece:
            count_opponent_diag += 1
        elif board[0][0] == Piece.EMPTY:
            empty_pieces_diag.append((0, 0))
            count_empty_diag += 1

        if board[1][1] == self.piece:
            count_mine_diag += 1
        elif board[1][1] == self.opponent_piece:
            count_opponent_diag += 1
        elif board[1][1] == Piece.EMPTY:
            empty_pieces_diag.append((1, 1))
            count_empty_diag += 1

        if board[2][2] == self.piece:
            count_mine_diag += 1
        elif board[2][2] == self.opponent_piece:
            count_opponent_diag += 1
        elif board[2][2] == Piece.EMPTY:
            empty_pieces_diag.append((2, 2))
            count_empty_diag += 1

        if count_mine_diag == 2 and count_empty_diag == 1:
            return empty_pieces_diag[0]

        if board[2][0] == self.piece:
            count_mine_diag += 1
        elif board[2][0] == self.opponent_piece:
            count_opponent_diag += 1
        elif board[2][0] == Piece.EMPTY:
            empty_pieces_diag.append((0, 0))
            count_empty_diag += 1
