import sys
import copy
from board import TicTacToeGame
from computer_strategy import TicTacToeStrategy as ComputerStrategy
from human_strategy import TicTacToeStrategy as HumanStrategy


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
            game = TicTacToeGame()
            game.board[i][j] = computer.piece

            if verbose:
                print("Starting board:")
                print(game)

            turn = 1
            while not game.is_over():
                # Human move
                if turn % 2 == 1:
                    move = human.get_move(copy.deepcopy(game.board))
                    game.apply_move(move, human.piece)
                else:
                    move = computer.get_move(copy.deepcopy(game.board))
                    game.apply_move(move, computer.piece)
                if verbose:
                    print(f"Turn {turn}:")
                    print(game)
                turn += 1

            if game.get_winner() == human.piece:
                won += 1
                if verbose:
                    print("Human wins!\n", game)
            elif game.get_winner() == computer.piece:
                lost += 1
                if verbose:
                    print("Computer wins!\n", game)
            else:
                tied += 1
                if verbose:
                    print("Tie!\n", game)

    # Given the human goes first
    game = TicTacToeGame()
    turn = 0
    if verbose:
        print("Starting board:")
        print(game)
    while not game.is_over():
        if turn % 2 == 0:
            move = human.get_move(copy.deepcopy(game.board))
            game.apply_move(move, human.piece)
            if verbose:
                print(f"Turn {turn}:")
                print(game)
        else:
            move = computer.get_move(copy.deepcopy(game.board))
            game.apply_move(move, computer.piece)
            if verbose:
                print(f"Turn {turn}:")
                print(game)
        turn += 1

    if game.get_winner() == computer.piece:
        won += 1
        if verbose:
            print("Computer wins!\n", game)
    elif game.get_winner() == human.piece:
        lost += 1
        if verbose:
            print("Human wins!\n", game)
    else:
        tied += 1
        if verbose:
            print("Tie!\n", game)

    # Print results
    print(f"Won: {won}, Lost: {lost}, Tied: {tied}")


if __name__ == "__main__":
    main()
