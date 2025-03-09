import random
from blackjack.api.core.player import Player
from core.game import GameState, Action


class RandomPlayer(Player):
    """A simple player that takes random valid actions"""

    def get_bet_size(self, state: GameState) -> float:
        return random.uniform(1, 100)

    def get_action(self, state: GameState) -> Action:
        """
        Determine the next action based on the current game state.
        Takes random actions from the set of valid actions.
        """
        valid_actions = [Action.HIT, Action.STAND]

        if state.can_double:
            valid_actions.append(Action.DOUBLE)
        if state.can_split:
            valid_actions.append(Action.SPLIT)

        return random.choice(valid_actions)
