from abc import abstractmethod
from typing import List
from core.game import GameState, Action


class Player:
    """Abstract base class for a blackjack player"""

    @abstractmethod
    def place_bets(self, state: GameState) -> List[float]:
        """
        At the start of each round, the player must place bets on each hand.

        Args:
            state (GameState): The current game state

        Returns:
            A list of float, each representing the amount of money wagered on a hand.
        """
        raise NotImplementedError("Your strategy must implement this method")

    @abstractmethod
    def get_action(
        self,
        state: GameState,
        hand_index: int,
    ) -> Action:
        """
        Determine the next action for a given hand.

        Args:
            state (GameState): The current game state
            hand_index (int): The index of the hand to take an action on

        Returns:
            Action: The next action to take
        """
        raise NotImplementedError("Your strategy must implement this method")
