"""
Test Suite for identifying Poker hands.

"""
from src.cards import Card, Rank, Suit
from src.poker import (high_card, pair, two_pair, three_of_a_kind, straight, flush,
                       full_house, four_of_a_kind, straight_flush, royal_flush)
import pytest

"""
----------------------------------------------------------------------
----------- HIGH CARD
----------------------------------------------------------------------
"""

_HIGH_CARDS = [
    # One card is valid
    {
        Card(Rank.ACE, Suit.HEARTS),
    },
    # Two cards are valid: "Pocket" cards
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.DIAMONDS),
    },
    # Ace high, no flush, no straight
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.JACK, Suit.SPADES),
        Card(Rank.NINE, Suit.HEARTS),  # nine breaks the broadway straight
    },
    # King high
    {
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.DIAMONDS),
        Card(Rank.JACK, Suit.CLUBS),
        Card(Rank.NINE, Suit.SPADES),  # nine breaks the straight
        Card(Rank.TWO, Suit.HEARTS),
    },
    # All low ranks, no straight, no flush
    {
        Card(Rank.TWO, Suit.HEARTS),
        Card(Rank.FOUR, Suit.DIAMONDS),
        Card(Rank.SIX, Suit.CLUBS),
        Card(Rank.EIGHT, Suit.SPADES),
        Card(Rank.JACK, Suit.HEARTS),
    },
    # Near-flush (four of one suit, one different)
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.NINE, Suit.CLUBS),  # breaks flush and straight
    },
    # Near-straight (one gap)
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.JACK, Suit.SPADES),
        Card(Rank.NINE, Suit.DIAMONDS),  # nine instead of ten breaks straight
    },
    # All different suits, scattered ranks
    {
        Card(Rank.THREE, Suit.HEARTS),
        Card(Rank.SIX, Suit.DIAMONDS),
        Card(Rank.EIGHT, Suit.CLUBS),
        Card(Rank.JACK, Suit.SPADES),
        Card(Rank.ACE, Suit.DIAMONDS),
    },
]

_NON_HIGH_CARDS = [
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.QUEEN, Suit.SPADES),
        Card(Rank.JACK, Suit.HEARTS),
    },
    # Two pair
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.QUEEN, Suit.HEARTS),
    },
    # Three of a kind
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.QUEEN, Suit.HEARTS),
    },
    # Straight (off-suit)
    {
        Card(Rank.TEN, Suit.HEARTS),
        Card(Rank.NINE, Suit.DIAMONDS),
        Card(Rank.EIGHT, Suit.CLUBS),
        Card(Rank.SEVEN, Suit.SPADES),
        Card(Rank.SIX, Suit.HEARTS),
    },
    # Flush (non-straight)
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.TEN, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.HEARTS),
        Card(Rank.FOUR, Suit.HEARTS),
        Card(Rank.TWO, Suit.HEARTS),
    },
    # Full house
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.KING, Suit.DIAMONDS),
    },
    # Four of a kind
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.KING, Suit.HEARTS),
    },
    # Straight flush
    {
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.TEN, Suit.HEARTS),
        Card(Rank.NINE, Suit.HEARTS),
    },
    # Royal flush
    {
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.QUEEN, Suit.SPADES),
        Card(Rank.JACK, Suit.SPADES),
        Card(Rank.TEN, Suit.SPADES),
    },
]

"""
----------------------------------------------------------------------
----------- PAIR
----------------------------------------------------------------------
"""

_PAIRS = [
    {
        Card(Rank.TWO, Suit.HEARTS),
        Card(Rank.TWO, Suit.SPADES),
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.JACK, Suit.CLUBS),
        Card(Rank.SEVEN, Suit.DIAMONDS),
    },
    {
        # Pair of Aces with distinct kickers
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.TEN, Suit.HEARTS),
    },
    {
        # Pair of Tens with a middle-range kicker
        Card(Rank.TEN, Suit.SPADES),
        Card(Rank.TEN, Suit.CLUBS),
        Card(Rank.NINE, Suit.DIAMONDS),
        Card(Rank.EIGHT, Suit.HEARTS),
        Card(Rank.TWO, Suit.CLUBS),
    },
    {
        # Pair of Threes with numerical sequence kickers (non-straight)
        Card(Rank.THREE, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.CLUBS),
        Card(Rank.FOUR, Suit.HEARTS),
        Card(Rank.FIVE, Suit.SPADES),
        Card(Rank.SEVEN, Suit.DIAMONDS),
    },
    {
        # Pair of Kings with non-flush kickers
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.SIX, Suit.SPADES),
        Card(Rank.FOUR, Suit.CLUBS),
        Card(Rank.THREE, Suit.HEARTS),
    },
    # A pair can be made with two cards
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
    },
]

_PAIRS_NON = [
    {
        # High Card (No pairs, disparate ranks)
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.TEN, Suit.CLUBS),
        Card(Rank.EIGHT, Suit.DIAMONDS),
        Card(Rank.FOUR, Suit.SPADES),
    },
    {
        # All distinct ranks, non-sequential
        Card(Rank.QUEEN, Suit.DIAMONDS),
        Card(Rank.JACK, Suit.CLUBS),
        Card(Rank.NINE, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.SPADES),
        Card(Rank.FIVE, Suit.CLUBS),
    },
    {
        # A Straight (Five sequential ranks, distinct)
        Card(Rank.NINE, Suit.HEARTS),
        Card(Rank.EIGHT, Suit.SPADES),
        Card(Rank.SEVEN, Suit.DIAMONDS),
        Card(Rank.SIX, Suit.CLUBS),
        Card(Rank.FIVE, Suit.HEARTS),
    },
    {
        # Low ranks, all distinct
        Card(Rank.SEVEN, Suit.CLUBS),
        Card(Rank.SIX, Suit.DIAMONDS),
        Card(Rank.FOUR, Suit.SPADES),
        Card(Rank.THREE, Suit.HEARTS),
        Card(Rank.TWO, Suit.CLUBS),
    },
    {
        # Broad range of ranks
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.JACK, Suit.DIAMONDS),
        Card(Rank.EIGHT, Suit.SPADES),
        Card(Rank.FIVE, Suit.CLUBS),
        Card(Rank.THREE, Suit.SPADES),
    },
    {
        # Two pair
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.FIVE, Suit.SPADES),
        Card(Rank.FIVE, Suit.CLUBS),
        Card(Rank.THREE, Suit.SPADES),
    }
]

"""
----------------------------------------------------------------------
----------- TWO PAIR
----------------------------------------------------------------------
"""

_TWO_PAIRS = [
    {
        # High pairs: Aces and Kings
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.QUEEN, Suit.HEARTS),
    },
    {
        # Middle pairs: Jacks and Tens
        Card(Rank.JACK, Suit.DIAMONDS),
        Card(Rank.JACK, Suit.CLUBS),
        Card(Rank.TEN, Suit.SPADES),
        Card(Rank.TEN, Suit.HEARTS),
        Card(Rank.TWO, Suit.CLUBS),
    },
    {
        # Low pairs: Fours and Threes
        Card(Rank.FOUR, Suit.SPADES),
        Card(Rank.FOUR, Suit.HEARTS),
        Card(Rank.THREE, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.CLUBS),
        Card(Rank.EIGHT, Suit.SPADES),
    },
    {
        # Disjointed pairs: Queens and Sevens
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.QUEEN, Suit.SPADES),
        Card(Rank.SEVEN, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.DIAMONDS),
        Card(Rank.NINE, Suit.CLUBS),
    },
    {
        # High/Low split: Aces and Twos
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.TWO, Suit.HEARTS),
        Card(Rank.TWO, Suit.SPADES),
        Card(Rank.SIX, Suit.DIAMONDS),
    },
]

_TWO_PAIRS_NON = [
    {
        # Three of a Kind (Not two pair)
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.SPADES),
        Card(Rank.QUEEN, Suit.DIAMONDS),
        Card(Rank.EIGHT, Suit.CLUBS),
        Card(Rank.FIVE, Suit.HEARTS),
    },
    {
        # One Pair
        Card(Rank.TEN, Suit.CLUBS),
        Card(Rank.TEN, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.CLUBS),
    },
    {
        # High Card (Distinct ranks)
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.JACK, Suit.DIAMONDS),
        Card(Rank.NINE, Suit.HEARTS),
        Card(Rank.SIX, Suit.CLUBS),
        Card(Rank.FOUR, Suit.SPADES),
    },
    {
        # Straight (Five sequential ranks)
        Card(Rank.EIGHT, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.DIAMONDS),
        Card(Rank.SIX, Suit.SPADES),
        Card(Rank.FIVE, Suit.CLUBS),
        Card(Rank.FOUR, Suit.DIAMONDS),
    },
    {
        # Full House (One pair, one set)
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.EIGHT, Suit.CLUBS),
        Card(Rank.EIGHT, Suit.CLUBS),
        Card(Rank.EIGHT, Suit.CLUBS),
    }
]

"""
----------------------------------------------------------------------
----------- SET (THREE OF A KIND)
----------------------------------------------------------------------
"""

_SETS = [
    {
        # Three of a Kind: Kings
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.NINE, Suit.CLUBS),
        Card(Rank.FOUR, Suit.HEARTS),
    },
    {
        # Three of a Kind: Threes
        Card(Rank.THREE, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.CLUBS),
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.THREE, Suit.SPADES),
        Card(Rank.JACK, Suit.DIAMONDS),
    },
    {
        # Three of a Kind: Tens
        Card(Rank.TEN, Suit.CLUBS),
        Card(Rank.TWO, Suit.CLUBS),
        Card(Rank.TEN, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.DIAMONDS),
        Card(Rank.TEN, Suit.SPADES),
    }
]

_SETS_NON = [
    {
        # Two Pair (Not three of a kind)
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.QUEEN, Suit.DIAMONDS),
        Card(Rank.EIGHT, Suit.HEARTS),
    },
    {
        # One Pair
        Card(Rank.JACK, Suit.SPADES),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.NINE, Suit.CLUBS),
        Card(Rank.FIVE, Suit.DIAMONDS),
        Card(Rank.TWO, Suit.SPADES),
    },
    {
        # High Card / All distinct ranks
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.TEN, Suit.HEARTS),
        Card(Rank.EIGHT, Suit.CLUBS),
        Card(Rank.SIX, Suit.SPADES),
        Card(Rank.THREE, Suit.DIAMONDS),
    }
]

"""
----------------------------------------------------------------------
----------- STRAIGHT
----------------------------------------------------------------------
"""

_STRAIGHTS = [
    {
        # High Straight (Broadway)
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.JACK, Suit.DIAMONDS),
        Card(Rank.TEN, Suit.HEARTS),
    },
    {
        # Low Straight (Wheel)
        Card(Rank.FIVE, Suit.SPADES),
        Card(Rank.FOUR, Suit.CLUBS),
        Card(Rank.THREE, Suit.DIAMONDS),
        Card(Rank.TWO, Suit.HEARTS),
        Card(Rank.ACE, Suit.CLUBS),
    },
    {
        # Mid-range Straight
        Card(Rank.NINE, Suit.DIAMONDS),
        Card(Rank.EIGHT, Suit.CLUBS),
        Card(Rank.SEVEN, Suit.SPADES),
        Card(Rank.SIX, Suit.HEARTS),
        Card(Rank.FIVE, Suit.DIAMONDS),
    },
    {
        # Mid-range Straight (different suits)
        Card(Rank.JACK, Suit.CLUBS),
        Card(Rank.TEN, Suit.DIAMONDS),
        Card(Rank.NINE, Suit.SPADES),
        Card(Rank.EIGHT, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.CLUBS),
    },
    {
        # Lower Mid-range Straight
        Card(Rank.SIX, Suit.SPADES),
        Card(Rank.FIVE, Suit.HEARTS),
        Card(Rank.FOUR, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.CLUBS),
        Card(Rank.TWO, Suit.SPADES),
    }
]

_NON_STRAIGHTS = [
    {
        # Broken Straight (Gap at the Seven)
        Card(Rank.NINE, Suit.HEARTS),
        Card(Rank.EIGHT, Suit.SPADES),
        Card(Rank.SIX, Suit.CLUBS),
        Card(Rank.FIVE, Suit.DIAMONDS),
        Card(Rank.FOUR, Suit.HEARTS),
    },
    {
        # Wrap-around (King-Ace-Two is not a straight)
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.TWO, Suit.SPADES),
        Card(Rank.THREE, Suit.HEARTS),
        Card(Rank.FOUR, Suit.DIAMONDS),
    },
    {
        # High Card / All distinct but far apart
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.JACK, Suit.DIAMONDS),
        Card(Rank.EIGHT, Suit.HEARTS),
        Card(Rank.FIVE, Suit.CLUBS),
        Card(Rank.TWO, Suit.SPADES),
    },
    {
        # Pair (Contains duplicate ranks, cannot be a straight)
        Card(Rank.TEN, Suit.CLUBS),
        Card(Rank.TEN, Suit.DIAMONDS),
        Card(Rank.NINE, Suit.SPADES),
        Card(Rank.EIGHT, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.CLUBS),
    },
    {
        # Near Broadway (Missing the Jack)
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.TEN, Suit.DIAMONDS),
        Card(Rank.NINE, Suit.HEARTS),
    }
]

"""
----------------------------------------------------------------------
----------- FLUSH
----------------------------------------------------------------------
"""

_FLUSHES = [
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.HEARTS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.TWO, Suit.HEARTS),
    },
    {
        Card(Rank.FIVE, Suit.DIAMONDS),
        Card(Rank.NINE, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.DIAMONDS),
        Card(Rank.TWO, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.DIAMONDS),
    },
    {
        Card(Rank.FIVE, Suit.SPADES),
        Card(Rank.SIX, Suit.SPADES),
        Card(Rank.THREE, Suit.SPADES),
        Card(Rank.EIGHT, Suit.SPADES),
        Card(Rank.ACE, Suit.SPADES),
    },
    {
        Card(Rank.JACK, Suit.CLUBS),
        Card(Rank.TWO, Suit.CLUBS),
        Card(Rank.SIX, Suit.CLUBS),
        Card(Rank.THREE, Suit.CLUBS),
        Card(Rank.ACE, Suit.CLUBS),
    },
]

_NON_FLUSHES = [
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.HEARTS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.TWO, Suit.CLUBS),
    },
    {
        Card(Rank.FIVE, Suit.DIAMONDS),
        Card(Rank.TWO, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.DIAMONDS),
        Card(Rank.TWO, Suit.DIAMONDS),
    },
    {
        Card(Rank.FIVE, Suit.SPADES),
        Card(Rank.SIX, Suit.CLUBS),
        Card(Rank.THREE, Suit.SPADES),
        Card(Rank.EIGHT, Suit.HEARTS),
        Card(Rank.ACE, Suit.SPADES),
    },
    {
        Card(Rank.JACK, Suit.CLUBS),
        Card(Rank.TWO, Suit.CLUBS),
        Card(Rank.SIX, Suit.SPADES),
        Card(Rank.THREE, Suit.SPADES),
        Card(Rank.ACE, Suit.HEARTS),
    },
]

"""
----------------------------------------------------------------------
----------- FULL HOUSE
----------------------------------------------------------------------
"""

_FULL_HOUSES = [
    # Aces full of threes
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.HEARTS),
        Card(Rank.THREE, Suit.CLUBS),
        Card(Rank.THREE, Suit.SPADES),
    },
    # Threes full of aces
    {
        Card(Rank.THREE, Suit.HEARTS),
        Card(Rank.THREE, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.CLUBS),
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.SPADES),
    },
    # Kings full of twos
    {
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.TWO, Suit.HEARTS),
        Card(Rank.TWO, Suit.SPADES),
    },
    # Twos full of kings (low trips, high pair)
    {
        Card(Rank.TWO, Suit.HEARTS),
        Card(Rank.TWO, Suit.DIAMONDS),
        Card(Rank.TWO, Suit.CLUBS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.KING, Suit.SPADES),
    },
    # Mid-rank full house
    {
        Card(Rank.SEVEN, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.DIAMONDS),
        Card(Rank.SEVEN, Suit.CLUBS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.JACK, Suit.SPADES),
    },
    # Adjacent ranks
    {
        Card(Rank.TEN, Suit.HEARTS),
        Card(Rank.TEN, Suit.DIAMONDS),
        Card(Rank.TEN, Suit.CLUBS),
        Card(Rank.NINE, Suit.HEARTS),
        Card(Rank.NINE, Suit.SPADES),
    },
]

_NON_FULL_HOUSES = [
    # Two pair (most common confusion case)
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.HEARTS),
        Card(Rank.THREE, Suit.CLUBS),
        Card(Rank.FIVE, Suit.SPADES),
    },
    # Three of a kind, no pair
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.THREE, Suit.HEARTS),
        Card(Rank.FIVE, Suit.SPADES),
    },
    # Four of a kind (trips + pair pattern broken)
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.THREE, Suit.HEARTS),
    },
    # One pair only
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.HEARTS),
        Card(Rank.FIVE, Suit.CLUBS),
        Card(Rank.SEVEN, Suit.SPADES),
    },
    # High card — all distinct ranks
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.JACK, Suit.SPADES),
        Card(Rank.NINE, Suit.HEARTS),
    },
    # Flush — same suit, no rank grouping (5 distinct ranks)
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.NINE, Suit.HEARTS),
    },
    # Invalid hand - duplicated suit is filtered out
    {
        Card(Rank.TEN, Suit.HEARTS),
        Card(Rank.TEN, Suit.DIAMONDS),
        Card(Rank.TEN, Suit.DIAMONDS),  # <-- duplicate
        Card(Rank.NINE, Suit.HEARTS),
        Card(Rank.NINE, Suit.SPADES),
    },
]

"""
----------------------------------------------------------------------
----------- FOUR OF A KIND
----------------------------------------------------------------------
"""

_FOURS = [
    # Aces with low kicker
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.TWO, Suit.SPADES),
    },
    # Aces with high kicker
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.KING, Suit.HEARTS),
    },
    # Low quads (twos)
    {
        Card(Rank.TWO, Suit.HEARTS),
        Card(Rank.TWO, Suit.DIAMONDS),
        Card(Rank.TWO, Suit.SPADES),
        Card(Rank.TWO, Suit.CLUBS),
        Card(Rank.ACE, Suit.HEARTS),
    },
    # Mid-rank quads
    {
        Card(Rank.SEVEN, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.DIAMONDS),
        Card(Rank.SEVEN, Suit.SPADES),
        Card(Rank.SEVEN, Suit.CLUBS),
        Card(Rank.KING, Suit.HEARTS),
    },
    # Kings
    {
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.ACE, Suit.HEARTS),
    },
]

_NON_FOURS = [
    # Three of a kind (the closest neighbour — one short)
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.THREE, Suit.CLUBS),
        Card(Rank.FIVE, Suit.HEARTS),
    },
    # Full house (trips + pair — two distinct rank groups, like quads)
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.KING, Suit.HEARTS),
    },
    # Two pair
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.HEARTS),
        Card(Rank.THREE, Suit.CLUBS),
        Card(Rank.FIVE, Suit.SPADES),
    },
    # One pair
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.HEARTS),
        Card(Rank.FIVE, Suit.CLUBS),
        Card(Rank.SEVEN, Suit.SPADES),
    },
    # High card
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.JACK, Suit.SPADES),
        Card(Rank.NINE, Suit.HEARTS),
    },
    # Three of a kind from prior negative case
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.EIGHT, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.HEARTS),
        Card(Rank.THREE, Suit.CLUBS),
        Card(Rank.THREE, Suit.SPADES),
    },
]

"""
----------------------------------------------------------------------
----------- STRAIGHT FLUSH
----------------------------------------------------------------------
"""

_STRAIGHT_FLUSHES = [
    {
        # High Straight (Broadway)
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.TEN, Suit.HEARTS),
    },
    {
        # Low Straight (Wheel)
        Card(Rank.FIVE, Suit.SPADES),
        Card(Rank.FOUR, Suit.SPADES),
        Card(Rank.THREE, Suit.SPADES),
        Card(Rank.TWO, Suit.SPADES),
        Card(Rank.ACE, Suit.SPADES),
    },
    {
        # Mid-range Straight
        Card(Rank.NINE, Suit.CLUBS),
        Card(Rank.EIGHT, Suit.CLUBS),
        Card(Rank.SEVEN, Suit.CLUBS),
        Card(Rank.SIX, Suit.CLUBS),
        Card(Rank.FIVE, Suit.CLUBS),
    },
    {
        # Mid-range Straight (different suits)
        Card(Rank.JACK, Suit.DIAMONDS),
        Card(Rank.TEN, Suit.DIAMONDS),
        Card(Rank.NINE, Suit.DIAMONDS),
        Card(Rank.EIGHT, Suit.DIAMONDS),
        Card(Rank.SEVEN, Suit.DIAMONDS),
    },
    {
        # Lower Mid-range Straight
        Card(Rank.SIX, Suit.SPADES),
        Card(Rank.FIVE, Suit.SPADES),
        Card(Rank.FOUR, Suit.SPADES),
        Card(Rank.THREE, Suit.SPADES),
        Card(Rank.TWO, Suit.SPADES),
    }
]

_NON_STRAIGHT_FLUSHES = [
    {
        # Broken Straight (Gap at the Seven)
        Card(Rank.NINE, Suit.HEARTS),
        Card(Rank.EIGHT, Suit.HEARTS),
        Card(Rank.SIX, Suit.HEARTS),
        Card(Rank.FIVE, Suit.HEARTS),
        Card(Rank.FOUR, Suit.HEARTS),
    },
    {
        # Wrap-around (King-Ace-Two is not a straight)
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.TWO, Suit.SPADES),
        Card(Rank.THREE, Suit.SPADES),
        Card(Rank.FOUR, Suit.SPADES),
    },
    {
        # Mid-range Straight
        Card(Rank.NINE, Suit.CLUBS),
        Card(Rank.EIGHT, Suit.CLUBS),
        Card(Rank.SEVEN, Suit.CLUBS),
        Card(Rank.SIX, Suit.CLUBS),
        Card(Rank.FIVE, Suit.HEARTS),
    },
    {
        # High Card / All distinct but far apart
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.JACK, Suit.DIAMONDS),
        Card(Rank.EIGHT, Suit.DIAMONDS),
        Card(Rank.FIVE, Suit.DIAMONDS),
        Card(Rank.TWO, Suit.DIAMONDS),
    },
    {
        # Pair (Contains duplicate ranks, cannot be a straight)
        Card(Rank.TEN, Suit.CLUBS),
        Card(Rank.TEN, Suit.CLUBS),
        Card(Rank.NINE, Suit.CLUBS),
        Card(Rank.EIGHT, Suit.CLUBS),
        Card(Rank.SEVEN, Suit.CLUBS),
    },
    {
        # Near Broadway (Missing the Jack)
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.QUEEN, Suit.DIAMONDS),
        Card(Rank.TEN, Suit.DIAMONDS),
        Card(Rank.NINE, Suit.DIAMONDS),
    }
]

"""
----------------------------------------------------------------------
----------- ROYAL FLUSH
----------------------------------------------------------------------
"""

_ROYAL_FLUSHES = [
    # Hearts
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.TEN, Suit.HEARTS),
    },
    # Spades
    {
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.QUEEN, Suit.SPADES),
        Card(Rank.JACK, Suit.SPADES),
        Card(Rank.TEN, Suit.SPADES),
    },
    # Diamonds
    {
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.QUEEN, Suit.DIAMONDS),
        Card(Rank.JACK, Suit.DIAMONDS),
        Card(Rank.TEN, Suit.DIAMONDS),
    },
    # Clubs
    {
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.JACK, Suit.CLUBS),
        Card(Rank.TEN, Suit.CLUBS),
    },
]

_NON_ROYAL_FLUSHES = [
    # Off-suit Broadway (straight, not flush)
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.TEN, Suit.CLUBS),
    },
    # Suited but not Broadway — straight flush, not royal
    {
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.TEN, Suit.HEARTS),
        Card(Rank.NINE, Suit.HEARTS),
    },
    # Flush but wrong ranks (no ten, no broadway)
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.NINE, Suit.HEARTS),
    },
    # Broadway ranks, suited, but ace is wrong suit (one card off)
    {
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.TEN, Suit.HEARTS),
    },
    # Full house — two distinct rank groups, superficially "special"
    {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.KING, Suit.DIAMONDS),
    },
    # Low straight flush (wheel straight flush — suited A2345)
    {
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.TWO, Suit.SPADES),
        Card(Rank.THREE, Suit.SPADES),
        Card(Rank.FOUR, Suit.SPADES),
        Card(Rank.FIVE, Suit.SPADES),
    },
]

"""
----------------------------------------------------------------------
------- POSITIVE CASES
----------------------------------------------------------------------
"""


@pytest.mark.parametrize("hand", _HIGH_CARDS)
def test_high_card(hand):
    assert high_card(hand)


@pytest.mark.parametrize("hand", _PAIRS)
def test_pair(hand):
    assert pair(hand)


@pytest.mark.parametrize("hand", _TWO_PAIRS)
def test_two_pairs(hand):
    assert two_pair(hand)


@pytest.mark.parametrize("hand", _SETS)
def test_set(hand):
    assert three_of_a_kind(hand)


@pytest.mark.parametrize("hand", _STRAIGHTS)
def test_straight(hand):
    assert straight(hand)


@pytest.mark.parametrize("hand", _FLUSHES)
def test_flush(hand):
    assert flush(hand)


@pytest.mark.parametrize("hand", _FULL_HOUSES)
def test_full_house(hand):
    assert full_house(hand)


@pytest.mark.parametrize("hand", _FOURS)
def test_fours(hand):
    assert four_of_a_kind(hand)


@pytest.mark.parametrize("hand", _STRAIGHT_FLUSHES)
def test_high_straight_flush(hand):
    assert straight_flush(hand)


@pytest.mark.parametrize("hand", _ROYAL_FLUSHES)
def test_royal_flushes(hand):
    assert royal_flush(hand)


"""
----------------------------------------------------------------------
------- NEGATIVE CASES
----------------------------------------------------------------------
"""


@pytest.mark.parametrize("hand", _NON_HIGH_CARDS)
def test_non_high_card(hand):
    assert not high_card(hand)


@pytest.mark.parametrize("hand", _PAIRS_NON)
def test_non_pair(hand):
    assert not pair(hand)


@pytest.mark.parametrize("hand", _TWO_PAIRS_NON)
def test_non_two_pair(hand):
    assert not two_pair(hand)


@pytest.mark.parametrize("hand", _SETS_NON)
def test_non_set(hand):
    assert not three_of_a_kind(hand)


@pytest.mark.parametrize("hand", _NON_STRAIGHTS)
def test_non_straights(hand):
    assert not straight(hand)


@pytest.mark.parametrize("hand", _NON_FULL_HOUSES)
def test_non_full_houses(hand):
    assert not full_house(hand)


@pytest.mark.parametrize("hand", _NON_FOURS)
def test_non_fours(hand):
    assert not four_of_a_kind(hand)


@pytest.mark.parametrize("hand", _NON_STRAIGHT_FLUSHES)
def test_non_straight_flushes(hand):
    assert not straight_flush(hand)


@pytest.mark.parametrize("hand", _NON_ROYAL_FLUSHES)
def test_non_royal_flush(hand):
    assert not royal_flush(hand)
