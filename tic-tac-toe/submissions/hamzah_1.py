from typing import List, Tuple
from board import Piece

class TicTacToeStrategy:
    def __init__(self, piece: Piece = Piece.O, opponent_piece: Piece = Piece.X):
        self.piece = piece
        self.opponent_piece = opponent_piece

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

    def get_move(self, board: List[List[Piece]]) -> Tuple[int, int]:
        """Implement your strategy here"""

        board_dict = {(x,y):4 for x in range(3) for y in range(3)} # cell:scenario (0,1,2,3)

        # check if opponent has winning moves to block
        for i in range(3):
            for j in range(3):
                if board[i][j] == Piece.EMPTY:
                    if self._check_winning_move(board, (i, j), self.opponent_piece):
                        return (i, j)

        # take center if open, regardless of 
        if board[1][1] == Piece.EMPTY:
            return (1,1)
        
        def cell_bfs(cell_x, cell_y) -> None:
            """
            given a cell, traverse around it and return first empty cell
            otherwise, return (-1,-1)
            """

            directions = [(-1, 0), (1, 0), (0,1), (0,-1), (-1,-1), (1,1)]

            for dx, dy in directions:
                adj_x, adj_y = cell_x + dx, cell_y + dy

                if (adj_x < 0 or adj_x > 2 
                    or adj_y < 0 or adj_y > 2):

                    return False
                
                if (board[adj_x][adj_y] == self.piece):
                    board_dict[(cell_x, cell_y)] = 1
            
                if (board[adj_x][adj_y] == Piece.X):
                    board_dict[(cell_x, cell_y)] = 2
                
                else:
                    board_dict[(cell_x, cell_y)] = 3

        # fill adj list
        for i in range(3):
            for j in range(3):
                if board[i][j] == Piece.EMPTY:
                    cell_bfs(i, j)


        # loop through board dict, return lowest non-zero zero value
        min_cell = (0,0)
        for cell in board_dict:
            if board_dict[cell] < board_dict[min_cell]:
                min_cell = cell


        return min_cell

