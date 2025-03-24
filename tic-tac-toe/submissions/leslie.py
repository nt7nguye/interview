# from typing import List, Tuple
# from collections import deque
# from board import Piece
# from computer_strategy import TicTacToeStrategy as Opponent


# # Really really slow. only ran once so keep this as benchmark
# # Final Elo Ratings:
# # leslie: 1710.7
# # kelvin_minimax: 1635.3
# # tanisha: 1632.6
# # kelvin_tweak: 1482.2
# # samir: 1471.6
# # hamzah_1: 1437.8
# # computer_strategy: 1406.9
# # hamzah_2: 1222.8

# class TicTacToeStrategy:
#     def __init__(
#         self, piece: Piece = Piece.O, opponent_piece: Piece = Piece.X, opponent=Opponent
#     ):
#         self.piece = piece
#         self.opponent_piece = opponent_piece
#         self.opponent = opponent
#         pass

#     """
#         Use BFS-implemented shortest path algorithm to traverse each possible next move, then prioritize the optimal next move baesd on the following rule:
#           1) If there's any way to achieve a win for `self.piece`,
#              pick the move that leads to a win in the fewest total moves.
#           2) Otherwise, pick the move that leads to a draw in the fewest total moves.
#           3) Otherwise, pick a move arbitrarily (loss is unavoidable if the computer
#              plays in a way that blocks all possible lines).
#     """

#     def get_move(self, board: List[List[Piece]]) -> Tuple[int, int]:
#         # Generate all legal moves
#         candidate_moves = []
#         for i in range(3):
#             for j in range(3):
#                 if board[i][j] == Piece.EMPTY:
#                     candidate_moves.append((i, j))

#         if not candidate_moves:
#             raise ValueError("No move found: board is already full or invalid.")

#         # For each candidate move, we check if that move can lead to a human-win or a possible draw. We'll track the best(shortest steps) among them.
#         best_win_move = None
#         best_win_cost = float("inf")

#         best_draw_move = None
#         best_draw_cost = float("inf")

#         for move in candidate_moves:
#             # Copy board, apply this candidate move by O
#             new_board = self._clone_board(board)
#             new_board[move[0]][move[1]] = self.piece

#             # If this move wins immediately, the cost is 1 move in total.
#             if self._get_winner(new_board) == self.piece:
#                 if 1 < best_win_cost:
#                     best_win_cost = 1
#                     best_win_move = move
#                 continue

#             # If the game ended in a draw immediately, the cost is 1 move in total.
#             if self._is_over(new_board):
#                 if self._get_winner(new_board) is None and 1 < best_draw_cost:
#                     best_draw_cost = 1
#                     best_draw_move = move
#                 continue
#             """
#             Otherwise, we do BFS over all possible next moves:
#               1) The minimal number of total moves until O eventually wins
#               2) The minimal number of total moves until a draw is reached
#             """
#             min_win_cost, min_draw_cost = self._bfs_outcome_search(
#                 new_board, next_turn=self.opponent_piece
#             )
#             # If we found a possible win, checking if we need to update the best_win_move for return.
#             if min_win_cost + 1 < best_win_cost:
#                 best_win_cost = min_win_cost + 1
#                 best_win_move = move

#             # Else if we haven't found any possible win, see if draw is possible, and best_draw_move should be updated for return.
#             if min_win_cost + 1 == float("inf") and min_draw_cost + 1 < best_draw_cost:
#                 best_draw_cost = min_draw_cost + 1
#                 best_draw_move = move

#         # return based on the priority rank of "least steps to win > least steps to draw". Otherwise, pick the first empty cell(unavoidable loss case).
#         if best_win_move is not None:
#             return best_win_move
#         elif best_draw_move is not None:
#             return best_draw_move
#         else:
#             # No winning or drawing line is possible, so pick first candidate
#             return candidate_moves[0]

#     def _bfs_outcome_search(
#         self, start_board: List[List[Piece]], next_turn: Piece
#     ) -> Tuple[int, int]:
#         """
#         Explore all possible moves from 'start_board', we track:
#           1) The fewest total moves to an O-win
#           2) The fewest total moves to a draw
#           3) If no O-win or draw will be found, we return (inf, inf)

#         We'll treat each expansion as cost=1 per move by either side.
#         """
#         # If the board is already terminal, check outcome.
#         if self._is_over(start_board):
#             winner = self._get_winner(start_board)
#             if winner == self.piece:
#                 return (0, float("inf"))
#             elif winner is None:
#                 return (float("inf"), 0)
#             else:
#                 return (float("inf"), float("inf"))

#         # BFS queue: each entry is (board_state, next_to_move, moves_so_far)
#         queue = deque()
#         queue.append((self._clone_board(start_board), next_turn, 0))

#         # We'll track the minimal number of moves to check if O will eventually win or draw
#         best_win_cost = float("inf")
#         best_draw_cost = float("inf")

#         while queue:
#             current_board, turn, cost = queue.popleft()

#             if self._is_over(current_board):
#                 winner = self._get_winner(current_board)
#                 if winner == self.piece:
#                     if cost < best_win_cost:
#                         best_win_cost = cost
#                 elif winner is None:
#                     if cost < best_draw_cost:
#                         best_draw_cost = cost
#                 continue

#             # If game is not ended, continue to generate moves
#             # current_piece = turn

#             empty_cells = []
#             for i in range(3):
#                 for j in range(3):
#                     if current_board[i][j] == Piece.EMPTY:
#                         empty_cells.append((i, j))

#             for r, c in empty_cells:
#                 next_board = self._clone_board(current_board)
#                 next_board[r][c] = turn

#                 next_player = self.opponent_piece if turn == self.piece else self.piece
#                 queue.append((next_board, next_player, cost + 1))

#         return (best_win_cost, best_draw_cost)

#     # Helper functions defined
#     def _clone_board(self, board: List[List[Piece]]) -> List[List[Piece]]:
#         return [row[:] for row in board]

#     def _get_winner(self, board: List[List[Piece]]) -> Piece:
#         lines = [
#             [board[0][0], board[0][1], board[0][2]],
#             [board[1][0], board[1][1], board[1][2]],
#             [board[2][0], board[2][1], board[2][2]],
#             [board[0][0], board[1][0], board[2][0]],
#             [board[0][1], board[1][1], board[2][1]],
#             [board[0][2], board[1][2], board[2][2]],
#             [board[0][0], board[1][1], board[2][2]],
#             [board[0][2], board[1][1], board[2][0]],
#         ]

#         for combo in lines:
#             if all(cell == Piece.X for cell in combo):
#                 return Piece.X
#             if all(cell == Piece.O for cell in combo):
#                 return Piece.O

#         return None

#     def _is_over(self, board: List[List[Piece]]) -> bool:
#         if self._get_winner(board) is not None:
#             return True
#         return all(cell != Piece.EMPTY for row in board for cell in row)
