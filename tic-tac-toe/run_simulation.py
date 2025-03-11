import sys
from board import TicTacToeGame, Piece
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
            game.board[i][j] = Piece.X

            if verbose:
                print("Starting board:")
                print(game)

            turn = 1
            while not game.is_over():
                # Human move
                if turn % 2 == 1:
                    move = human.get_move(game.board)
                    game.apply_move(move, Piece.O)
                else:
                    move = computer.get_move(game.board)
                    game.apply_move(move, Piece.X)
                if verbose:
                    print(f"Turn {turn}:")
                    print(game)
                turn += 1

            if game.get_winner() == Piece.O:
                won += 1
                if verbose:
                    print("Human wins!", game)
            elif game.get_winner() == Piece.X:
                lost += 1
                if verbose:
                    print("Computer wins!", game)
            else:
                tied += 1
                if verbose:
                    print("Tie!", game)

    # Given the human goes first
    game = TicTacToeGame()
    turn = 0
    if verbose:
        print("Starting board:")
        print(game)
    while not game.is_over():
        if turn % 2 == 0:
            move = human.get_move(game.board)
            game.apply_move(move, Piece.O)
            if verbose:
                print(f"Turn {turn}:")
                print(game)
        else:
            move = computer.get_move(game.board)
            game.apply_move(move, Piece.X)
            if verbose:
                print(f"Turn {turn}:")
                print(game)
        turn += 1

    if game.get_winner() == Piece.X:
        won += 1
    elif game.get_winner() == Piece.O:
        lost += 1
    else:
        tied += 1

    # Print results
    print(f"Won: {won}, Lost: {lost}, Tied: {tied}")


if __name__ == "__main__":
    main()
