from typing import List, Tuple
from board import Piece
from computer_strategy import TicTacToeStrategy as Opponent

class TicTacToeStrategy:
    def __init__(self, piece: Piece = Piece.O, opponent_piece: Piece = Piece.X):
        self.piece = piece
        self.opponent_piece = opponent_piece
        pass

    def check_winner(self, board: List[List[Piece]]) -> Piece:
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
            if combination[0] == combination[1] == combination[2]:
                if combination[0] != Piece.EMPTY: return combination[0]
        
        return Piece.EMPTY

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
        comp = Opponent()
        possible_randoms = []
        """Implement your strategy here"""
        try:
            for i in range(3):
                for j in range(3):
                    if board[i][j] == Piece.EMPTY:
                        board[i][j] = Piece.O
                        a,b = comp.get_move(board=board)
                        board[a][b] = Piece.X

                        # if this gives me a winning move, undo simulation, make this move
                        winner = self.check_winner(board=board)
                        board[i][j] = Piece.EMPTY
                        board[a][b] = Piece.EMPTY
                        if winner == Piece.O:
                            return (i,j)
                        elif winner == Piece.X:
                            continue
                        else:
                            possible_randoms.append((i,j))
            
            # pick random
            if len(possible_randoms) > 0: return possible_randoms[0]
            for i in range(3):
                for j in range(3):
                    if board[i][j] == Piece.EMPTY:
                        return (i,j)
        except:
            # assume value error 
            return ValueError("fix this!")
    
    # SImulate one move
    # Check what opponent would do, then see if i can win/lose