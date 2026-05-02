from src.cards import Card, Rank, Suit
import pytest

_ADDITION: dict[tuple[Card, ...], int] = {
    (
        Card(Rank.TWO, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.CLUBS)
    ): 5,
    # Jack = 11
    (
        Card(Rank.SIX, Suit.CLUBS),
        Card(Rank.JACK, Suit.CLUBS)
    ): 17,
    (
        Card(Rank.SIX, Suit.DIAMONDS),
        Card(Rank.JACK, Suit.SPADES),
        Card(Rank.TWO, Suit.CLUBS)
    ): 19,
    # Aces are low
    (
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.ACE, Suit.CLUBS)
    ): 3,
}


@pytest.mark.parametrize("hand,expected", _ADDITION.items())
def test_card_addition(hand: tuple[Card, ...], expected: int):
    assert sum(hand) == expected
