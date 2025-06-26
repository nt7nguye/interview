from typing import List, Tuple
from board import Piece
from board import TicTacToeGame


class TicTacToeStrategy:
    def __init__(
        self,
        piece: Piece = Piece.O,
        opponent_piece: Piece = Piece.X,
        opponent=None,
    ):
        self.piece = piece
        self.opponent_piece = opponent_piece
        self.opponent = opponent
        pass

    def get_move(self, board: List[List[Piece]]) -> Tuple[int, int]:
        """Implement your strategy here"""
        eval = float("-inf")
        bestmove = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == Piece.EMPTY:
                    board[i][j] = self.piece  # fix was here

                    neweval = self.minimax(board, False)
                    # print(neweval)
                    if neweval > eval:
                        eval = neweval
                        bestmove = [i, j]
                        # print(neweval)
                        # print(bestmove)
                    board[i][j] = Piece.EMPTY  # and here
        return bestmove

    def minimax(self, board, maximizing):
        game = TicTacToeGame()
        game.board = board
        if game.is_over():
            if game.get_winner() is None:
                return 0
            if game.get_winner() == self.piece:
                return 1
            else:
                return -1
        # print(board)
        eval = -9
        if maximizing:
            for i in range(3):
                for j in range(3):
                    if board[i][j] == Piece.EMPTY:
                        board[i][j] = self.piece
                        neweval = self.minimax(board, not maximizing)
                        eval = max(eval, neweval)

                        board[i][j] = Piece.EMPTY
        else:
            move = self.opponent.get_move(board)
            board[move[0]][move[1]] = self.opponent_piece
            eval = self.minimax(board, not maximizing)
            board[move[0]][move[1]] = Piece.EMPTY
        return eval
