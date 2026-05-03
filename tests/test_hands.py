"""
Test Suite for identifying Poker hands.

"""
from src.cards import (Card, A, J, Q, K, H, C, D, S)
from src.hands import (high_card, pair, two_pair, three_of_a_kind, straight, flush,
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
        Card(A, H),
    },
    # Two cards are valid: "Pocket" cards
    {
        Card(A, H),
        Card(K, D),
    },
    # Ace high, no flush, no straight
    {
        Card(A, H),
        Card(K, D),
        Card(Q, C),
        Card(J, S),
        Card(9, H),  # nine breaks the broadway straight
    },
    # King high
    {
        Card(K, H),
        Card(Q, D),
        Card(J, C),
        Card(9, S),  # nine breaks the straight
        Card(2, H),
    },
    # All low ranks, no straight, no flush
    {
        Card(2, H),
        Card(4, D),
        Card(6, C),
        Card(8, S),
        Card(J, H),
    },
    # Near-flush (four of one suit, one different)
    {
        Card(A, H),
        Card(K, H),
        Card(Q, H),
        Card(J, H),
        Card(9, C),  # breaks flush and straight
    },
    # Near-straight (one gap)
    {
        Card(A, H),
        Card(K, D),
        Card(Q, C),
        Card(J, S),
        Card(9, D),  # nine instead of ten breaks straight
    },
    # All different suits, scattered ranks
    {
        Card(3, H),
        Card(6, D),
        Card(8, C),
        Card(J, S),
        Card(A, D),
    },
]

_NON_HIGH_CARDS = [
    {
        Card(A, H),
        Card(A, D),
        Card(K, C),
        Card(Q, S),
        Card(J, H),
    },
    # Two pair
    {
        Card(A, H),
        Card(A, D),
        Card(K, C),
        Card(K, S),
        Card(Q, H),
    },
    # Three of a kind
    {
        Card(A, H),
        Card(A, D),
        Card(A, C),
        Card(K, S),
        Card(Q, H),
    },
    # Straight (off-suit)
    {
        Card(10, H),
        Card(9, D),
        Card(8, C),
        Card(7, S),
        Card(6, H),
    },
    # Flush (non-straight)
    {
        Card(A, H),
        Card(10, H),
        Card(7, H),
        Card(4, H),
        Card(2, H),
    },
    # Full house
    {
        Card(A, H),
        Card(A, D),
        Card(A, C),
        Card(K, H),
        Card(K, D),
    },
    # Four of a kind
    {
        Card(A, H),
        Card(A, D),
        Card(A, C),
        Card(A, S),
        Card(K, H),
    },
    # Straight flush
    {
        Card(K, H),
        Card(Q, H),
        Card(J, H),
        Card(10, H),
        Card(9, H),
    },
    # Royal flush
    {
        Card(A, S),
        Card(K, S),
        Card(Q, S),
        Card(J, S),
        Card(10, S),
    },
]

"""
----------------------------------------------------------------------
----------- PAIR
----------------------------------------------------------------------
"""

_PAIRS = [
    {
        Card(2, H),
        Card(2, S),
        Card(A, C),
        Card(J, C),
        Card(7, D),
    },
    {
        # Pair of Aces with distinct kickers
        Card(A, H),
        Card(A, D),
        Card(K, S),
        Card(Q, C),
        Card(10, H),
    },
    {
        # Pair of Tens with a middle-range kicker
        Card(10, S),
        Card(10, C),
        Card(9, D),
        Card(8, H),
        Card(2, C),
    },
    {
        # Pair of Threes with numerical sequence kickers (non-straight)
        Card(3, D),
        Card(3, C),
        Card(4, H),
        Card(5, S),
        Card(7, D),
    },
    {
        # Pair of Kings with non-flush kickers
        Card(K, C),
        Card(K, D),
        Card(6, S),
        Card(4, C),
        Card(3, H),
    },
    # A pair can be made with two cards
    {
        Card(A, H),
        Card(A, D),
    },
]

_PAIRS_NON = [
    {
        # High Card (No pairs, disparate ranks)
        Card(A, H),
        Card(K, S),
        Card(10, C),
        Card(8, D),
        Card(4, S),
    },
    {
        # All distinct ranks, non-sequential
        Card(Q, D),
        Card(J, C),
        Card(9, H),
        Card(7, S),
        Card(5, C),
    },
    {
        # A Straight (Five sequential ranks, distinct)
        Card(9, H),
        Card(8, S),
        Card(7, D),
        Card(6, C),
        Card(5, H),
    },
    {
        # Low ranks, all distinct
        Card(7, C),
        Card(6, D),
        Card(4, S),
        Card(3, H),
        Card(2, C),
    },
    {
        # Broad range of ranks
        Card(K, H),
        Card(J, D),
        Card(8, S),
        Card(5, C),
        Card(3, S),
    },
    {
        # Two pair
        Card(K, H),
        Card(K, D),
        Card(5, S),
        Card(5, C),
        Card(3, S),
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
        Card(A, H),
        Card(A, S),
        Card(K, C),
        Card(K, D),
        Card(Q, H),
    },
    {
        # Middle pairs: Jacks and Tens
        Card(J, D),
        Card(J, C),
        Card(10, S),
        Card(10, H),
        Card(2, C),
    },
    {
        # Low pairs: Fours and Threes
        Card(4, S),
        Card(4, H),
        Card(3, D),
        Card(3, C),
        Card(8, S),
    },
    {
        # Disjointed pairs: Queens and Sevens
        Card(Q, C),
        Card(Q, S),
        Card(7, H),
        Card(7, D),
        Card(9, C),
    },
    {
        # High/Low split: Aces and Twos
        Card(A, D),
        Card(A, C),
        Card(2, H),
        Card(2, S),
        Card(6, D),
    },
]

_TWO_PAIRS_NON = [
    {
        # Three of a Kind (Not two pair)
        Card(Q, H),
        Card(Q, S),
        Card(Q, D),
        Card(8, C),
        Card(5, H),
    },
    {
        # One Pair
        Card(10, C),
        Card(10, D),
        Card(A, S),
        Card(J, H),
        Card(7, C),
    },
    {
        # High Card (Distinct ranks)
        Card(K, S),
        Card(J, D),
        Card(9, H),
        Card(6, C),
        Card(4, S),
    },
    {
        # Straight (Five sequential ranks)
        Card(8, H),
        Card(7, D),
        Card(6, S),
        Card(5, C),
        Card(4, D),
    },
    {
        # Full House (One pair, one set)
        Card(A, C),
        Card(A, C),
        Card(8, C),
        Card(8, C),
        Card(8, C),
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
        Card(K, H),
        Card(K, S),
        Card(K, D),
        Card(9, C),
        Card(4, H),
    },
    {
        # Three of a Kind: Threes
        Card(3, D),
        Card(3, C),
        Card(A, H),
        Card(3, S),
        Card(J, D),
    },
    {
        # Three of a Kind: Tens
        Card(10, C),
        Card(2, C),
        Card(10, H),
        Card(7, D),
        Card(10, S),
    }
]

_SETS_NON = [
    {
        # Two Pair (Not three of a kind)
        Card(A, H),
        Card(A, S),
        Card(Q, C),
        Card(Q, D),
        Card(8, H),
    },
    {
        # One Pair
        Card(J, S),
        Card(J, H),
        Card(9, C),
        Card(5, D),
        Card(2, S),
    },
    {
        # High Card / All distinct ranks
        Card(K, D),
        Card(10, H),
        Card(8, C),
        Card(6, S),
        Card(3, D),
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
        Card(A, H),
        Card(K, S),
        Card(Q, C),
        Card(J, D),
        Card(10, H),
    },
    {
        # Low Straight (Wheel)
        Card(5, S),
        Card(4, C),
        Card(3, D),
        Card(2, H),
        Card(A, C),
    },
    {
        # Mid-range Straight
        Card(9, D),
        Card(8, C),
        Card(7, S),
        Card(6, H),
        Card(5, D),
    },
    {
        # Mid-range Straight (different suits)
        Card(J, C),
        Card(10, D),
        Card(9, S),
        Card(8, H),
        Card(7, C),
    },
    {
        # Lower Mid-range Straight
        Card(6, S),
        Card(5, H),
        Card(4, D),
        Card(3, C),
        Card(2, S),
    }
]

_NON_STRAIGHTS = [
    {
        # Broken Straight (Gap at the Seven)
        Card(9, H),
        Card(8, S),
        Card(6, C),
        Card(5, D),
        Card(4, H),
    },
    {
        # Wrap-around (King-Ace-Two is not a straight)
        Card(K, D),
        Card(A, C),
        Card(2, S),
        Card(3, H),
        Card(4, D),
    },
    {
        # High Card / All distinct but far apart
        Card(A, S),
        Card(J, D),
        Card(8, H),
        Card(5, C),
        Card(2, S),
    },
    {
        # Pair (Contains duplicate ranks, cannot be a straight)
        Card(10, C),
        Card(10, D),
        Card(9, S),
        Card(8, H),
        Card(7, C),
    },
    {
        # Near Broadway (Missing the Jack)
        Card(A, H),
        Card(K, S),
        Card(Q, C),
        Card(10, D),
        Card(9, H),
    }
]

"""
----------------------------------------------------------------------
----------- FLUSH
----------------------------------------------------------------------
"""

_FLUSHES = [
    {
        Card(A, H),
        Card(K, H),
        Card(7, H),
        Card(J, H),
        Card(2, H),
    },
    {
        Card(5, D),
        Card(9, D),
        Card(3, D),
        Card(2, D),
        Card(A, D),
    },
    {
        Card(5, S),
        Card(6, S),
        Card(3, S),
        Card(8, S),
        Card(A, S),
    },
    {
        Card(J, C),
        Card(2, C),
        Card(6, C),
        Card(3, C),
        Card(A, C),
    },
]

_NON_FLUSHES = [
    {
        Card(A, H),
        Card(K, H),
        Card(7, H),
        Card(J, H),
        Card(2, C),
    },
    {
        Card(5, D),
        Card(2, D),
        Card(3, D),
        Card(2, D),
    },
    {
        Card(5, S),
        Card(6, C),
        Card(3, S),
        Card(8, H),
        Card(A, S),
    },
    {
        Card(J, C),
        Card(2, C),
        Card(6, S),
        Card(3, S),
        Card(A, H),
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
        Card(A, H),
        Card(A, D),
        Card(3, H),
        Card(3, C),
        Card(3, S),
    },
    # Threes full of aces
    {
        Card(3, H),
        Card(3, D),
        Card(3, C),
        Card(A, H),
        Card(A, S),
    },
    # Kings full of twos
    {
        Card(K, H),
        Card(K, D),
        Card(K, C),
        Card(2, H),
        Card(2, S),
    },
    # Twos full of kings (low trips, high pair)
    {
        Card(2, H),
        Card(2, D),
        Card(2, C),
        Card(K, H),
        Card(K, S),
    },
    # Mid-rank full house
    {
        Card(7, H),
        Card(7, D),
        Card(7, C),
        Card(J, H),
        Card(J, S),
    },
    # Adjacent ranks
    {
        Card(10, H),
        Card(10, D),
        Card(10, C),
        Card(9, H),
        Card(9, S),
    },
]

_NON_FULL_HOUSES = [
    # Two pair (most common confusion case)
    {
        Card(A, H),
        Card(A, D),
        Card(3, H),
        Card(3, C),
        Card(5, S),
    },
    # Three of a kind, no pair
    {
        Card(A, H),
        Card(A, D),
        Card(A, C),
        Card(3, H),
        Card(5, S),
    },
    # Four of a kind (trips + pair pattern broken)
    {
        Card(A, H),
        Card(A, D),
        Card(A, C),
        Card(A, S),
        Card(3, H),
    },
    # One pair only
    {
        Card(A, H),
        Card(A, D),
        Card(3, H),
        Card(5, C),
        Card(7, S),
    },
    # High card — all distinct ranks
    {
        Card(A, H),
        Card(K, D),
        Card(Q, C),
        Card(J, S),
        Card(9, H),
    },
    # Flush — same suit, no rank grouping (5 distinct ranks)
    {
        Card(A, H),
        Card(K, H),
        Card(Q, H),
        Card(J, H),
        Card(9, H),
    },
    # Invalid hand - duplicated suit is filtered out
    {
        Card(10, H),
        Card(10, D),
        Card(10, D),  # <-- duplicate
        Card(9, H),
        Card(9, S),
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
        Card(A, H),
        Card(A, D),
        Card(A, S),
        Card(A, C),
        Card(2, S),
    },
    # Aces with high kicker
    {
        Card(A, H),
        Card(A, D),
        Card(A, S),
        Card(A, C),
        Card(K, H),
    },
    # Low quads (twos)
    {
        Card(2, H),
        Card(2, D),
        Card(2, S),
        Card(2, C),
        Card(A, H),
    },
    # Mid-rank quads
    {
        Card(7, H),
        Card(7, D),
        Card(7, S),
        Card(7, C),
        Card(K, H),
    },
    # Kings
    {
        Card(K, H),
        Card(K, D),
        Card(K, S),
        Card(K, C),
        Card(A, H),
    },
]

_NON_FOURS = [
    # Three of a kind (the closest neighbour — one short)
    {
        Card(A, H),
        Card(A, D),
        Card(A, S),
        Card(3, C),
        Card(5, H),
    },
    # Full house (trips + pair — two distinct rank groups, like quads)
    {
        Card(A, H),
        Card(A, D),
        Card(A, S),
        Card(K, C),
        Card(K, H),
    },
    # Two pair
    {
        Card(A, H),
        Card(A, D),
        Card(3, H),
        Card(3, C),
        Card(5, S),
    },
    # One pair
    {
        Card(A, H),
        Card(A, D),
        Card(3, H),
        Card(5, C),
        Card(7, S),
    },
    # High card
    {
        Card(A, H),
        Card(K, D),
        Card(Q, C),
        Card(J, S),
        Card(9, H),
    },
    # Three of a kind from prior negative case
    {
        Card(A, H),
        Card(8, D),
        Card(3, H),
        Card(3, C),
        Card(3, S),
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
        Card(A, H),
        Card(K, H),
        Card(Q, H),
        Card(J, H),
        Card(10, H),
    },
    {
        # Low Straight (Wheel)
        Card(5, S),
        Card(4, S),
        Card(3, S),
        Card(2, S),
        Card(A, S),
    },
    {
        # Mid-range Straight
        Card(9, C),
        Card(8, C),
        Card(7, C),
        Card(6, C),
        Card(5, C),
    },
    {
        # Mid-range Straight (different suits)
        Card(J, D),
        Card(10, D),
        Card(9, D),
        Card(8, D),
        Card(7, D),
    },
    {
        # Lower Mid-range Straight
        Card(6, S),
        Card(5, S),
        Card(4, S),
        Card(3, S),
        Card(2, S),
    }
]

_NON_STRAIGHT_FLUSHES = [
    {
        # Broken Straight (Gap at the Seven)
        Card(9, H),
        Card(8, H),
        Card(6, H),
        Card(5, H),
        Card(4, H),
    },
    {
        # Wrap-around (King-Ace-Two is not a straight)
        Card(K, D),
        Card(A, D),
        Card(2, S),
        Card(3, S),
        Card(4, S),
    },
    {
        # Mid-range Straight
        Card(9, C),
        Card(8, C),
        Card(7, C),
        Card(6, C),
        Card(5, H),
    },
    {
        # High Card / All distinct but far apart
        Card(A, D),
        Card(J, D),
        Card(8, D),
        Card(5, D),
        Card(2, D),
    },
    {
        # Pair (Contains duplicate ranks, cannot be a straight)
        Card(10, C),
        Card(10, C),
        Card(9, C),
        Card(8, C),
        Card(7, C),
    },
    {
        # Near Broadway (Missing the Jack)
        Card(A, D),
        Card(K, D),
        Card(Q, D),
        Card(10, D),
        Card(9, D),
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
        Card(A, H),
        Card(K, H),
        Card(Q, H),
        Card(J, H),
        Card(10, H),
    },
    # Spades
    {
        Card(A, S),
        Card(K, S),
        Card(Q, S),
        Card(J, S),
        Card(10, S),
    },
    # Diamonds
    {
        Card(A, D),
        Card(K, D),
        Card(Q, D),
        Card(J, D),
        Card(10, D),
    },
    # Clubs
    {
        Card(A, C),
        Card(K, C),
        Card(Q, C),
        Card(J, C),
        Card(10, C),
    },
]

_NON_ROYAL_FLUSHES = [
    # Off-suit Broadway (straight, not flush)
    {
        Card(A, H),
        Card(K, H),
        Card(Q, H),
        Card(J, H),
        Card(10, C),
    },
    # Suited but not Broadway — straight flush, not royal
    {
        Card(K, H),
        Card(Q, H),
        Card(J, H),
        Card(10, H),
        Card(9, H),
    },
    # Flush but wrong ranks (no ten, no broadway)
    {
        Card(A, H),
        Card(K, H),
        Card(Q, H),
        Card(J, H),
        Card(9, H),
    },
    # Broadway ranks, suited, but ace is wrong suit (one card off)
    {
        Card(A, C),
        Card(K, H),
        Card(Q, H),
        Card(J, H),
        Card(10, H),
    },
    # Full house — two distinct rank groups, superficially "special"
    {
        Card(A, H),
        Card(A, D),
        Card(A, C),
        Card(K, H),
        Card(K, D),
    },
    # Low straight flush (wheel straight flush — suited A2345)
    {
        Card(A, S),
        Card(2, S),
        Card(3, S),
        Card(4, S),
        Card(5, S),
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
