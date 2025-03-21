from typing import List, Tuple
from board import Piece
import copy
from computer_strategy import TicTacToeStrategy as Opponent


class TicTacToeStrategy:
    def __init__(
        self,
        piece: Piece = Piece.O,
        opponent_piece: Piece = Piece.X,
        opponent=Opponent,
    ):
        self.piece = piece
        self.opponent_piece = opponent_piece
        self.opponent = opponent
        pass

    def _is_winner(self, board: List[List[Piece]], piece: Piece) -> bool:
        winning_combinations = [
            [board[0][0], board[0][1], board[0][2]],
            [board[1][0], board[1][1], board[1][2]],
            [board[2][0], board[2][1], board[2][2]],
            [board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            [board[0][0], board[1][1], board[2][2]],
            [board[0][2], board[1][1], board[2][0]],
        ]

        for combination in winning_combinations:
            if all(cell == piece for cell in combination):
                return True
        return False

    def _full_board(self, board):
        for i in range(3):
            for j in range(3):
                if board[i][j] == Piece.EMPTY:
                    return False
        return True

    def minimax(self, board, depth, player):
        if self._is_winner(board, self.piece):
            return 10, None

        if self._is_winner(board, self.opponent_piece):
            return -10, None
        if self._full_board(board):
            return 0, None

        empty_cells = self.get_empties(board)

        if player:
            best_score = float("-inf")
            best_move = None

            for i, j in empty_cells:
                board[i][j] = self.piece

                score, _ = self.minimax(board, depth + 1, False)
                board[i][j] = Piece.EMPTY

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

            return best_score, best_move
        else:
            best_score = float("inf")
            board_copy = copy.deepcopy(board)
            computer_strategy = self.opponent(self.opponent_piece, self.piece)
            computer_move = computer_strategy.get_move(board_copy)
            board[computer_move[0]][computer_move[1]] = self.opponent_piece
            score, _ = self.minimax(board, depth + 1, True)
            board[computer_move[0]][computer_move[1]] = Piece.EMPTY

            return score, None

    def get_empties(self, board):
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == Piece.EMPTY:
                    empty_cells.append((i, j))
        return empty_cells

    def get_move(self, board: List[List[Piece]]) -> Tuple[int, int]:
        empty_cells = self.get_empties(board)
        if len(empty_cells) == 1:
            return empty_cells[0]
        board_copy = copy.deepcopy(board)

        _, best_move = self.minimax(board_copy, 0, True)

        if best_move is None:
            for i in range(3):
                for j in range(3):
                    if board[i][j] == Piece.EMPTY:
                        return (i, j)

        return best_move
