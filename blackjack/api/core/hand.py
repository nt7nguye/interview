from typing import List
from card import Card


class Hand:
    def __init__(self, cards: List[Card]):
        self.cards = cards
        self.doubled = False
        self.stood = False

    @property
    def is_bust(self) -> bool:
        return min(self.possible_values) > 21 if self.possible_values else True

    @property
    def possible_values(self) -> List[int]:
        """Calculate all possible hand values accounting for aces"""
        if not self.cards:
            return [0]

        values = [0]
        for card in self.cards:
            card_values = card.blackjack_value
            new_values = []
            for value in values:
                for card_value in card_values:
                    new_values.append(value + card_value)
            values = [v for v in new_values if v <= 21] or [min(new_values)]
        return values

    @property
    def best_value(self) -> int:
        """Returns the highest non-busting value, or lowest busting value"""
        values = self.possible_values
        non_bust = [v for v in values if v <= 21]
        return max(non_bust) if non_bust else min(values)
