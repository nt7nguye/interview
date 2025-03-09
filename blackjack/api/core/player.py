import random
from game import GameState, Action


class RandomPlayer:
    """A simple player that takes random valid actions"""

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
