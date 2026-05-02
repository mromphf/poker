"""
Provides enums for Rank and Suit, combined
to form the Card class.

The deck() function is available to create
a collection of 52 cards, sorted or shuffled.
"""

from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from random import shuffle


class Suit(Enum):
    """
    A classic french deck has four colored suits:

    Hearts, Diamonds, Spades, Clubs

    Hearts and Diamonds are Red, Spades and
    Clubs are Black. There is no standard order for Suits.
    """

    HEARTS = 1
    CLUBS = 2
    DIAMONDS = 3
    SPADES = 4

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()


@total_ordering
class Rank(Enum):
    """
    A classic french deck contains four sets
    of 13 ranks from Ace to King.

    Aces can traditionally be low or high depending
    on the game or use case. This enum models Aces
    as the LOWEST rank: 1

    Jack, Queen, and King are called "Face" cards
    and are ranked 11, 12, and 13 respectively. Ace
    High ranks higher than a King.

    Adding Ranks yields an integer based on the
    sum of their values.
    """

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __hash__(self):
        return hash((self.name, self.value))

    def __int__(self):
        return self.value

    def __add__(self, other):
        return self.value + other.value

    def __radd__(self, other):
        return int(self) + int(other)

    def __sub__(self, other):
        return self.value - other.value


@dataclass
@total_ordering
class Card:
    """
    A Card is a combination of a Rank and a Suit.

    Adding cards together yields the sum of their ranks.

    Sorting cards orders by rank, with Aces considered
    low.
    """

    rank: Rank
    suit: Suit

    def __init__(self, r: Rank, s: Suit):
        self.rank = r
        self.suit = s

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.rank == other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __int__(self):
        return self.rank.value

    def __add__(self, other):
        return self.rank.value + other.rank.value

    def __radd__(self, other):
        return int(self) + int(other)

    def __sub__(self, other):
        return self.rank.value - other.rank.value


def deck(shuffled: bool = False) -> list[Card]:
    """
    Creates a deck of 52 cards.

    13 distinct ranks per 4 suits.

    Can optionally be shuffled.

    :param shuffled: Randomize the order of the cards.
    :return: A list with 52 cards, sorted or shuffled.
    """

    cards = [Card(rank, suit)
             for rank in Rank for suit in Suit]

    if shuffled:
        shuffle(cards)

    return cards
