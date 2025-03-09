from core import Card, Suit


def test_card_creation():
    card = Card(suit=Suit.HEARTS, value=1)
    assert card.suit == Suit.HEARTS
    assert card.value == 1


def test_card_blackjack_value():
    # Test ace
    ace = Card(suit=Suit.SPADES, value=1)
    assert ace.blackjack_value == [1, 11]

    # Test face cards
    king = Card(suit=Suit.HEARTS, value=13)
    assert king.blackjack_value == [10]
    queen = Card(suit=Suit.DIAMONDS, value=12)
    assert queen.blackjack_value == [10]
    jack = Card(suit=Suit.CLUBS, value=11)
    assert jack.blackjack_value == [10]

    # Test number cards
    two = Card(suit=Suit.HEARTS, value=2)
    assert two.blackjack_value == [2]
    ten = Card(suit=Suit.DIAMONDS, value=10)
    assert ten.blackjack_value == [10]
