from abc import abstractmethod
from typing import List
from core.game import GameState, Action


class Strategy:
    """Abstract base class for a blackjack player"""

    @abstractmethod
    def get_bet_size(self, state: GameState, bankroll: float) -> float:
        """
        Determine the amount of money to bet before the round starts.
        Note: The bet size is defaulted to at least 1.0

        Args:
            state (GameState): The current game state

        Returns:
            float: The amount of money to bet
        """
        raise NotImplementedError("Your strategy must implement this method")

    @abstractmethod
    def get_action(
        self,
        state: GameState,
        possible_actions: List[Action],
        bankroll: float,
    ) -> Action:
        """
        Determine the next action for a given hand.

        Args:
            state (GameState): The current game state
            possible_actions (List[Action]): The list of possible actions
            bankroll (float): The player's current cash

        Returns:
            Action: The next action to take
        """
        raise NotImplementedError("Your strategy must implement this method")
