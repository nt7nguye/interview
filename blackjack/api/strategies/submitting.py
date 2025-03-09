import random
from typing import List
from core import Action, Strategy, PlayerInformation


class MyStrategy(Strategy):
    """Implement your own strategy here"""

    def get_bet_size(self, info: PlayerInformation, bankroll: float) -> float:
        return 1.0

    def get_action(
        self, info: PlayerInformation, possible_actions: List[Action], bankroll: float
    ) -> Action:
        """
        Determine the next action based on the current game state.
        Takes random actions from the set of valid actions.
        """
        return random.choice(possible_actions)
