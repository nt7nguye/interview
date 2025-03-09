import random
from typing import List
from core.card import Card, Suit


class Deck:
    def __init__(self, num_decks: int = 1):
        self.cards: List[Card] = []
        for _ in range(num_decks):
            for suit in Suit:
                for value in range(1, 14):
                    self.cards.append(Card(suit, value))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if not self.cards:
            raise ValueError("Deck is empty")
        return self.cards.pop()
