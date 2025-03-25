import importlib
import os
import random
import sys
import copy
import traceback
from tty import setcbreak
from board import Piece, TicTacToeGame


def main():
    players = []

    for file in os.listdir(os.path.join(os.path.dirname(__file__), "submissions")):
        if file.endswith(".py") and not file.startswith("__"):
            player_module = importlib.import_module(f"submissions.{file[:-3]}")
            if "TicTacToeStrategy" in dir(player_module):
                players.append(file[:-3])

    # Elo rating {submission_id: elo}
    # TODO: Maybe not match players that are too different in ratings ?
    player_elo = {player: 1500 for player in players}
    k_factor = 24

    for i in range(1000):
        if i % 100 == 0:
            print(f"Running game {i} of 1000")

        player = random.choice(players)
        other_player = random.choice(players)

        if player == other_player:
            continue

        if abs(player_elo[player] - player_elo[other_player]) > 400:
            continue

        player_class = load_player_class(player)
        other_player_class = load_player_class(other_player)

        # This is ugly but avoid infinite recursion for now
        first_player = player_class(Piece.X, Piece.O)
        second_player = other_player_class(Piece.O, Piece.X)
        first_player.opponent = second_player
        second_player.opponent = first_player

        try:
            result = run_game(first_player, second_player, i, player, other_player)
        except Exception as e:
            print(f"Error: Game {i}, {player} vs {other_player}, {e}")
            print(traceback.format_exc())
            continue

        expected_score_first = 1 / (
            1 + 10 ** ((player_elo[other_player] - player_elo[player]) / 400)
        )
        expected_score_second = 1 - expected_score_first

        player_elo[player] += k_factor * (result - expected_score_first)
        player_elo[other_player] += k_factor * (1 - result - expected_score_second)

    # Print players sorted by Elo rating
    sorted_players = sorted(player_elo.items(), key=lambda x: x[1], reverse=True)
    print("\nFinal Elo Ratings:")
    for player, elo in sorted_players:
        print(f"{player}: {elo:.1f}")


def load_player_class(player_name):
    try:
        player_module = importlib.import_module(f"submissions.{player_name}")

        for attr_name in dir(player_module):
            if attr_name == "TicTacToeStrategy":
                player_class = getattr(player_module, attr_name)
                return player_class
    except ImportError as e:
        print(f"Error: Strategy '{player_name}' not found or could not be imported.")
        print(f"Import error: {e}")
        sys.exit(1)


def run_game(first, second, i, player, other_player):
    game = TicTacToeGame()
    turn = 0

    while not game.is_over():
        # Human move
        if turn % 2 == 0:
            try:
                move = first.get_move(copy.deepcopy(game.board))
                # No move is automatically a loss
                if move is None:
                    return 0
                game.apply_move(move, first.piece)
            except Exception as e:
                print(
                    f"Error in first player get_move: Game {i}, {player} vs {other_player}, {e}"
                )
                print(traceback.format_exc())
                return 0
        else:
            try:
                move = second.get_move(copy.deepcopy(game.board))
                # No move is automatically a win
                if move is None:
                    return 1
                game.apply_move(move, second.piece)
            except Exception as e:
                print(
                    f"Error in second player get_move: Game {i}, {player} vs {other_player}, {e}"
                )
                print(traceback.format_exc())
                return 1
        turn += 1

    if game.get_winner() == first.piece:
        return 1
    elif game.get_winner() == second.piece:
        return 0
    else:
        return 0.5


if __name__ == "__main__":
    current_dir: str = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    main()
