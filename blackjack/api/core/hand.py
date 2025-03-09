from typing import List
from core.card import Card


class Hand:
    def __init__(self, cards: List[Card], bet_amount: int):
        self.cards = cards
        self.bet_amount = bet_amount

    @property
    def is_bust(self) -> bool:
        return min(self.possible_values) > 21 if self.possible_values else True

    @property
    def is_blackjack(self) -> bool:
        """Blackjacks are a point total of 21 using their first two original cards"""
        return len(self.cards) == 2 and self.best_value == 21

    @property
    def can_split(self) -> bool:
        """A hand can be split if it has two cards of the same value.
        Note that there is
        """
        return len(self.cards) == 2 and self.cards[0].value == self.cards[1].value

    @property
    def can_hit(self) -> bool:
        return min(self.possible_values) < 21

    @property
    def can_double(self) -> bool:
        """A hand can double if it has only two cards"""
        return (
            len(self.cards) == 2
            and self.cards[0].value == self.cards[1].value
            and self.can_hit
        )

    @property
    def possible_values(self) -> List[int]:
        """Calculate all possible hand values"""
        if not self.cards:
            return [0]

        permutations = [0]
        for card in self.cards:
            new_permutations = []
            for value in card.blackjack_value:
                for permutation in permutations:
                    new_permutations.append(permutation + value)
            permutations = new_permutations

        return sorted(list(set(permutations)))

    @property
    def best_value(self) -> int:
        """Returns the highest non-busting value, or lowest busting value"""
        values = self.possible_values
        non_bust = [v for v in values if v <= 21]
        return max(non_bust) if non_bust else min(values)
