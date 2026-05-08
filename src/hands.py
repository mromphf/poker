"""
Identifying Poker Hands

The 10 standard Poker hands are ranked by probability,
with the least probable hand, the Royal Flush, ranking
highest.

High Card and Pair require at most 2 cards,
which is the number of cards dealt to players
at the beginning of a Texas Hold'Em round.

These are commonly referred to as the "pocket" cards.

The other Poker hands are typically formed from a hand
of 5 cards. Every hand from a straight and higher requires
at least 5 cards to be valid.



1. Royal Flush	    A, K, Q, J, 10, of the same suit.
2. Straight Flush	Five consecutive cards of the same suit.
3. Four of a Kind	Four cards of the same rank.
4. Full House	    Three cards of one rank and two cards of another rank.
5. Flush	        Five cards of the same suit, not in sequence.
6. Straight	        Five consecutive cards of any suits.
7. Three of a Kind	Three cards of the same rank.
8. Two Pair	        Two cards of one rank and two cards of another rank.
9. One Pair	        Two cards of the same rank.
10. High Card	    The highest card in the hand when no other hand is made.

https://en.wikipedia.org/wiki/List_of_poker_hands

https://en.wikipedia.org/wiki/Texas_hold_%27em

-- Mark R.    May 2026

"""

from collections import Counter
from src.cards import Card, Rank

# Top straight is often referred to as "Broadway"
_BROADWAY = frozenset({
    Rank.ACE,
    Rank.TEN,
    Rank.JACK,
    Rank.QUEEN,
    Rank.KING
})

# Straights, Flushes, and Full Houses
_FULL_HAND = 5


def high_card(hand: set[Card]) -> bool:
    """
    HIGH CARD

    The lowest ranking hand. A hand of distinct
    ranks that don't form a straight or a flush.

    A single card is a valid high-card hand.

    :param hand: Set of Cards
    :return: True if cards fulfill no other hand
    """

    distinct = len({
        card.rank for card in hand
    }) == len(hand)

    # All ranks are distinct (no pairs or sets) but do not form a straight
    # A hand of at least 5 cards cannot be suited (no flush)

    return distinct and not straight(hand) and not flush(hand)


def pair(hand: set[Card]) -> bool:
    """
    PAIR

    A single rank is repeated twice:

        [ A A 2 5 7 ] <- Aces

        [ A 3 3 9 J ] <- Threes

        [ 3 Q 7 Q 4 ] <- Queens

    :param hand: Set of Cards
    :return: True if hand forms a pair
    """

    # A SINGLE rank is counted twice

    counts = Counter(
        card.rank for card in hand
    ).values()

    return len([c for c in counts if c == 2]) == 1


def two_pair(hand: set[Card]) -> bool:
    """
    TWO PAIR

    Two distinct ranks are repeated twice.

        [ A A 2 2 7 ] <- Aces & Twos

        [ 4 3 4 7 7 ] <- Fours & Sevens

        [ K Q 7 Q K ] <- Queens & Kings

    :param hand: Set of Cards
    :return: True if hand forms two-pair
    """

    counts = Counter(
        card.rank for card in hand
    ).values()

    return len([c for c in counts if c == 2]) == 2


def three_of_a_kind(hand: set[Card]) -> bool:
    """
    THREE OF A KIND

    A single rank is repeated three times

    aka. a Set

        [ A A A 5 7 ] <- Aces

        [ A 7 7 7 J ] <- Sevens

        [ 3 J 7 J J ] <- Jacks

    :param hand: Set of Cards
    :return: True if hand forms a set (three-of-a-kind)
    """

    # A rank is counted 3 times

    return 3 in Counter(
        card.rank for card in hand
    ).values()


def straight(hand: set[Card]) -> bool:
    """
    STRAIGHT

    The ranks of five cards form a contiguous sequence.

        [ A 2 3 4 5 ] <- Low Straight aka. "The Wheel"

        [ 6 5 4 3 7 ] <- Three through Seven, unordered

        [ 10 J Q K A ] <- Top Straight aka. "Broadway"

    For math nerds,

    A contiguous sequence can be identified like so:

    |{A}| = |A| and (max(A) - min(a) = |A| - 1)

    :param hand: Set of Cards
    :return: True if hand forms a straight.
    """

    ranks = {card.rank for card in hand}

    return (len(ranks) == _FULL_HAND and (
            (max(ranks) - min(ranks) == _FULL_HAND - 1)
            or ranks == _BROADWAY))


def flush(hand: set[Card]) -> bool:
    """
    FLUSH

    At least five cards share the same suit.

    :param hand: Set of Cards
    :return: True if at least 5 cards are suited
    """

    if len(hand) < _FULL_HAND:
        return False

    return len({card.suit for card in hand}) == 1


def full_house(hand: set[Card]) -> bool:
    """
    FULL HOUSE

    A distinct pair of ranks combined with a
    distinct set of ranks.

        [ A A A K K ] <- Aces full of Kings

        [ 7 7 2 2 7 ] <- 7s full of 2s

        [ 8 8 J J J ] <- Jacks full of 8s

    :param hand: Set of Cards
    :return: True if hand forms a full house.
    """

    rank_counts = Counter(
        card.rank for card in hand
    ).values()

    return 2 in rank_counts and 3 in rank_counts


def four_of_a_kind(hand: set[Card]) -> bool:
    """
    FOUR OF A KIND

    A single rank is repeated four times:

        [ A A A A 7 ] <- Aces

        [ A 6 6 6 6 ] <- Sixes

        [ K K 10 K K ] <- Kings

    :param hand: Set of Cards.
    :return: True if hand forms four-of-a-kind.
    """

    return 4 in Counter(
        card.rank for card in hand
    ).values()


def straight_flush(hand: set[Card]) -> bool:
    """
    STRAIGHT FLUSH

    A suited straight.

    :param hand: Set of Cards
    :return: True if ranks form a straight and suits form a flush.
    """

    return straight(hand) and flush(hand)


def royal_flush(hand: set[Card]) -> bool:
    """
    ROYAL FLUSH

    The highest-ranking hand in Poker.
    A suited-straight including TEN, JACK, QUEEN, KING, and ACE.

    :param hand: Set of Cards
    :return: True if [10, J, Q, K, A] share the same suit (in any order)
    """

    return flush(hand) and {card.rank for card in hand} == _BROADWAY
