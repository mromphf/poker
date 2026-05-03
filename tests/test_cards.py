from src.cards import (Card, deck,
                       A, J, Q, K, H, C, D, S)
import pytest

_FULL_DECK = 52

_ADDITION: dict[tuple[Card, ...], int] = {
    (
        Card(2, D),
        Card(3, C)
    ): 5,
    # Jack = 11
    (
        Card(6, C),
        Card(J, C),
    ): 17,
    (
        Card(6, D),
        Card(J, H),
        Card(2, S),
    ): 19,
    # Aces are low
    (
        Card(A, D),
        Card(A, C),
        Card(A, H),
    ): 3,
    # Queen (12) + King (13)
    (
        Card(Q, D),
        Card(K, D),
    ): 25
}


def test_deck_length():
    assert len(deck()) == _FULL_DECK


def test_deck_shuffled_length():
    assert len(deck(shuffled=True)) == _FULL_DECK


@pytest.mark.parametrize("hand,expected", _ADDITION.items())
def test_card_addition(hand: tuple[Card, ...], expected: int):
    assert sum(hand) == expected
