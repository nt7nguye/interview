from enum import Enum
from typing import List


class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"


class Card:
    def __init__(self, suit: Suit, value: int):
        self.suit = suit
        self.value = value  # 1-13 (Ace is 1)

    @property
    def blackjack_value(self) -> List[int]:
        """Returns possible blackjack values for the card"""
        if self.value == 1:  # Ace
            return [1, 11]
        elif self.value > 10:  # Face cards
            return [10]
        return [self.value]

    def __str__(self):
        value_map = {1: "A", 11: "J", 12: "Q", 13: "K"}
        value_str = value_map.get(self.value, str(self.value))
        return f"{value_str}{self.suit.value}"
