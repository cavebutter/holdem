import poker_functions as p
import pytest

# 2 Pair
hand1 = ['As', '4c']
flop1 = ['4d', 'Qh', 'Ts']
turn1 = ['7h']
river1 = ['Ad']

# Flush, 1 Pair
hand2 = ['As', 'Ks']
flop2 = ['4d', 'Kh', 'Ts']
turn2 = ['7s']
river2 = ['3s']

# Straight, no pair, no flush
hand3 = ['4s', '5d']
flop3 = ['6c', '7s', '8h']
turn3 = ['Jc']
river3 = ['As']

# 3 of a kind
hand4 = ['As', 'Ac']
flop4 = ['4d', 'Qh', 'Ts']
turn4 = ['7h']
river4 = ['Ad']

# Full House
hand5 = ['As', 'Ac']
flop5 = ['4d', 'Qh', 'Ts']
turn5 = ['4c']
river5 = ['Ad']

# Straight flush
hand6 = ['4s', '5s']
flop6 = ['6s', '7s', '8s']
turn6 = ['Jc']
river6 = ['As']

# Straight, non-sequential
hand7 = ['2c', '9s']
flop7 = ['Jh', '6c', '3d']
turn7 = ['4h']
river7 = ['5s']

# Straight, 5 card
hand8 = ['2c', '2s']
flop8 = ['6h', '3c', '3d']
turn8 = ['4h']
river8 = ['5s']

# Straight, 6 card
hand9 = ['2c', '7s']
flop9 = ['Jh', '3c', '3d']
turn9 = ['4h']
river9 = ['5s']

def test_count_deck():
    """Test deck generates exactly 52 cards"""
    deck = p.generate_deck()
    assert len(deck) == 52

def test_parse_card_str():
    mycard = p.parse_card(river1[0])
    assert type(mycard) == p.Card

def test_parse_card_Card():
    mycard = p.Card('J', 'd')
    parsed = p.parse_card(mycard)
    assert type(mycard) == p.Card

def test_convert_total_hand_str():
    string = p.convert_total_hand(flop3)
    assert type(string[0]) == p.Card

def test_convert_total_hand_Card():
    cards = [p.Card('4', 'd'), p.Card('K', 's')]
    test = p.convert_total_hand(cards)
    assert  type(test[0]) == p.Card

def test_deal():
    deck = p.generate_deck()
    card, updated_deck = p.deal_card(deck)
    assert type(card) == p.Card and len(updated_deck) == 51

def test_update_deck_count():
    deck = p.generate_deck()
    p.update_deck(deck, flop1[0])
    assert len(deck) == 51

def test_no_flush():
    board = flop1 + turn1 + river1
    flush = p.find_flush(hand1, board)
    assert not flush

def test_flush():
    board2 = flop2 + turn2 + river2
    flush = p.find_flush(hand2, board2)
    assert flush

def test_one_pair():
    board2 = flop2 + turn2 + river2
    pair = p.find_multiple(hand2, board2)
    assert pair

def test_not_one_pair():
    board3 = flop3 + turn3 + river3
    pair = p.find_multiple(hand3, board3)
    assert not pair

def test_not_two_pair():
    board3 = flop3 + turn3 + river3
    two_pair = p.find_two_pair(hand3, board3)
    assert not two_pair

def test_two_pair():
    board1 = flop1 + turn1 + river1
    two_pair = p.find_two_pair(hand1, board1)
    assert two_pair

def test_not_3ok():
    board1 = flop1 + turn1 + river1
    three_o_kind = p.find_multiple(hand1, board1, 3)
    assert not three_o_kind

def test_3ok():
    board4 = flop4 + turn4 + river4
    three_o_kind = p.find_multiple(hand4, board4, 3)
    assert three_o_kind

def test_no_boat():
    board = flop1 + turn1 + river1
    boat = p.find_full_house(hand1, board)
    assert not boat

def test_boat():
    board5 = flop5 + turn5 + river5
    boat = p.find_full_house(hand5, board5)
    assert boat

def test_straight_sequential():
    board3 = flop3 + turn3 + river3
    straight = p.find_straight(hand3, board3)
    assert straight

def test_straight_non_sequential():
    board7 = flop7 + turn7 + river7
    straight = p.find_straight(hand7, board7)
    assert straight

def test_straight_5_card():
    board8 = flop8 + turn8 + river8
    straight = p.find_straight(hand8, board8)
    assert straight

def test_straight_6_card():
    board9 = flop9 + turn9 + river9
    straight = p.find_straight(hand9, board9)
    assert straight

def test_not_straight():
    board4 = flop4 + turn4 + river4
    straight = p.find_straight(hand4, board4)
    assert not straight


def test_not_straight_flush():
    board = flop1 + turn1 + river1
    straight_flush = p.find_straight_flush(hand1, board)
    assert not straight_flush

def test_not_straight_flush_flush():
    board = flop2 + turn2 + river2
    straight_flush = p.find_straight_flush(hand2, board)
    assert not straight_flush

def test_straight_flush():
    board6 = flop6 + turn6 + river6
    straight_flush = p.find_straight_flush(hand6, board6)
    assert straight_flush