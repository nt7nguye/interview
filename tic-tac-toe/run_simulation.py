import sys
import copy
from board import TicTacToeGame
from computer_strategy import TicTacToeStrategy as ComputerStrategy
from human_strategy import TicTacToeStrategy as HumanStrategy
from typing import Tuple

def main():
    verbose = False
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        verbose = True

    won = 0
    lost = 0
    tied = 0

    human = HumanStrategy()
    computer = ComputerStrategy()
    # Given the computer goes first, test against 9 possible starting positions
    for i in range(3):
        for j in range(3):
            winner = run_game(verbose, (i, j), 0, human, computer)

            if winner == human.piece: 
                won += 1
            elif winner == computer.piece: 
                lost += 1
            else: 
                tied += 1

    # Given the human goes first
    winner = run_game(verbose, (0, 0), 1, human, computer)
    if winner == human.piece:
        won += 1
    elif winner == computer.piece:
        lost += 1
    else:
        tied += 1

    # Print results
    print(f"Won: {won}, Lost: {lost}, Tied: {tied}")


"""Returns: Winner's piece ('X' or 'O') or None for tie"""
def run_game(verbose: bool,
            start_position: Tuple[int, int], # Used if computer's first move
            start_turn: int, # Who starts (0 for computer, 1 for human)
            human: HumanStrategy, 
            computer: ComputerStrategy):
    
    game = TicTacToeGame()
    if start_turn == 0:
        game.board[start_position[0]][start_position[1]] = computer.piece

    if verbose:
        print("Starting board:")
        print(game)
    
    turn = 1
    while not game.is_over():
        # Human move
        if turn % 2 == 1:
            move = human.get_move(copy.deepcopy(game.board))
            try:
                game.apply_move(move, human.piece)
            except Exception:
                if verbose:
                    print("Invalid move, computer wins!")
                return computer.piece
        else:
            move = computer.get_move(copy.deepcopy(game.board))
            game.apply_move(move, computer.piece)
        if verbose:
            print(f"Turn {turn}:")
            print(game)
        turn += 1
    
    if game.get_winner() == human.piece:
        if verbose:
            print("Human wins!")
        return human.piece
    elif game.get_winner() == computer.piece:
        if verbose:
            print("Computer wins!")
        return computer.piece
    else:
        if verbose:
            print("Tie!")
        return None


if __name__ == "__main__":
    main()
