from enum import Enum
from functools import total_ordering


class Suit(Enum):
    HEARTS = 1
    CLUBS = 2
    DIAMONDS = 3
    SPADES = 4

    def __str__(self):
        return str(self.name)


@total_ordering
class Rank(Enum):
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

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __add__(self, other):
        return self.value + other.value

    def __sub__(self, other):
        return self.value - other.value


@total_ordering
class Card:
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

    def __sub__(self, other):
        return self.rank.value - other.rank.value
