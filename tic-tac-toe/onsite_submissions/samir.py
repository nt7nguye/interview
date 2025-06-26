from board import Piece
from typing import List, Tuple
from board import Piece
from computer_strategy import TicTacToeStrategy as Opponent


class TicTacToeStrategy:
    def __init__(
        self,
        piece: Piece = Piece.O,
        opponent_piece: Piece = Piece.X,
        opponent=None,
    ):
        self.piece = piece
        self.opponent_piece = opponent_piece
        pass

    def _check_winning_move(
        self, board: List[List[Piece]], move: Tuple[int, int], piece: Piece
    ) -> bool:
        board[move[0]][move[1]] = piece
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
                board[move[0]][move[1]] = Piece.EMPTY
                return True
        board[move[0]][move[1]] = Piece.EMPTY
        return False

    def _check_this_move_gives_double_threats(
        self, move: Tuple[int, int], board: List[List[Piece]], piece: Piece
    ) -> bool:
        # Check for double threats
        possible_winning_moves = 0
        board[move[0]][move[1]] = piece
        for i in range(3):
            for j in range(3):
                if board[i][j] == Piece.EMPTY:
                    if self._check_winning_move(board, (i, j), piece):
                        possible_winning_moves += 1
        board[move[0]][move[1]] = Piece.EMPTY
        return possible_winning_moves >= 2

    def get_move(self, board: List[List[Piece]]) -> Tuple[int, int]:
        """Implement your strategy here"""

        for i in range(3):
            for j in range(3):
                if board[i][j] == Piece.EMPTY:
                    if self._check_winning_move(board, (i, j), self.piece):
                        return (i, j)

        # If the other player has a winning move, have to block it
        for i in range(3):
            for j in range(3):
                if board[i][j] == Piece.EMPTY:
                    if self._check_winning_move(board, (i, j), self.opponent_piece):
                        return (i, j)

        move_count = 0
        for i in range(3):
            for j in range(3):
                if board[i][j] != Piece.EMPTY:
                    move_count += 1

        if move_count == 0:
            self._went_first = True
            return (2, 2)

        elif move_count == 1:
            self._went_first = False
            if board[1][1] == self.opponent_piece:
                return (2, 2)
            else:
                return (1, 1)

        elif move_count == 2:
            # if center is taken, take opposite corner
            if board[1][1] == self.opponent_piece:
                return (0, 0)
            # Default to take bottom left corner, unless it is under threat
            elif (
                board[2][1] == self.opponent_piece or board[0][1] == self.opponent_piece
            ):
                return (0, 2)
            else:
                return (2, 0)

        elif move_count == 4:
            if board[2][0] == self.piece:
                return (0, 0)
            else:
                return (2, 0)

        for i in range(3):
            for j in range(3):
                if board[i][j] == Piece.EMPTY:
                    if self._check_this_move_gives_double_threats(
                        (i, j), board, self.piece
                    ):
                        return (i, j)

        # Look for double threats
        for i in range(3):
            for j in range(3):
                if board[i][j] == Piece.EMPTY:
                    board[i][j] = self.piece
                    double_threat_count = 0
                    for opponent_i in range(3):
                        for opponent_j in range(3):
                            if board[opponent_i][opponent_j] == Piece.EMPTY:
                                if not self._check_this_move_gives_double_threats(
                                    (opponent_i, opponent_j),
                                    board,
                                    self.opponent_piece,
                                ):
                                    double_threat_count += 1
                    if double_threat_count == 0:
                        return (i, j)
                    board[i][j] = Piece.EMPTY

        for i in range(3):
            for j in range(3):
                if board[i][j] == Piece.EMPTY:
                    return (i, j)


# IF Computer goes 1st and not on Center:
# -> Take Center
# ---> if they take opposite corner (take edge)

# If Computer goes 1st and on Center
# -> Take Corner
# --> All moves (but one) lead to a win threat
# ----> stop wins
# ...... stopping line threats (consider checking for our own wins)


# If going first, always take corner
# --> if they don't take center (create auto win algoirthm)
# --> if they do take center:
# ----> take opposite corner
