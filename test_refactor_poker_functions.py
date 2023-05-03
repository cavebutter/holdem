import poker_functions as p

# valid card string
card_str1 = 'As'

# invalid card string
card_string2 = 'Of'

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
river6 = ['Ac']

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
flop9 = ['Jh', '3c', '6d']
turn9 = ['4h']
river9 = ['5s']

#  Duplicated Card
hand10 = ['3c', 'As']
flop10 = ['3c', 'Jd', '9h']
turn10 = ['4s']
river10 = ['8s']


#  Invalid Card
hand11 = ['3c', 'As']
flop11 = ['9c', 'Jd', '9h']
turn11 = ['4s']
river11 = ['Ss']


#  Wheel
hand12 = ['Ac', 'Td']
flop12 = ['2c', '3h', 'Qs']
turn12 = ['4s']
river12 = ['5d']

def test_card_init():
    card = p.Card(card_str1)
    assert type(card) == p.Card


def test_card_rank():
    card = p.Card(card_str1)
    assert card.rank == 'A'


def test_card_suit():
    card = p.Card(card_str1)
    assert card.suit == 's'


def test_card_value():
    card = p.Card(card_str1)
    assert card.value == 14


def test_card_name():
    card = p.Card(card_str1)
    assert card.name == 'As'


def test_deck_init():
    deck = p.generate_deck()
    assert type(deck) == p.Deck


def test_deck_contents():
    deck = p.generate_deck()
    assert type(deck[5]) == p.Card


def test_deck_size():
    deck = p.generate_deck()
    assert len(deck) == 52


def test_deal_card_1():
    """Ensures that the deal_card generates a Card object"""
    deck = p.generate_deck()
    card, deck = deck.deal_card()
    assert type(card) == p.Card


def test_deal_card_2():
    """Ensures that deal_card removes Card from deck"""
    deck = p.generate_deck()
    card, deck = deck.deal_card()
    assert len(deck) == 51


def test_update_deck_1():
    """Remove a passed card from Deck passed as string"""
    deck = p.generate_deck()
    deck.update_deck('Ks')
    cards = [card.name for card in deck]
    assert len(deck) == 51


def test_update_deck_2():
    """Remove a passed card from Deck passed as Card"""
    card = p.Card('Ks')
    deck = p.generate_deck()
    deck.update_deck(card)
    cards = [card.name for card in deck]
    assert len(deck) == 51


def test_update_deck_3():
    """Ensure specific passed card is removed from deck"""
    passed_card = p.Card('2c')
    deck = p.generate_deck()
    deck.update_deck(passed_card)
    cards = [card.name for card in deck]
    assert passed_card.name not in cards


def test_update_deck_4():
    """Ensure specific passed card string is removed from deck"""
    passed_card = '2c'
    deck = p.generate_deck()
    deck.update_deck(passed_card)
    cards = [card.name for card in deck]
    assert passed_card.name not in cards

def test_valid_card():
    check = hand9 + flop9 + turn9 + river9
    valid = p.validate_card(check)
    assert valid


def test_invalid_card():
    check = hand11 + flop11 + turn11 + river11
    valid = p.validate_card(check)
    assert not valid


def test_duplicate_card():
    check = hand10 + flop10 + turn10 + river10
    duplicate = p.dedupe(check)
    assert duplicate


def test_not_duplicate():
    check = hand9 + flop9 + turn9 + river9
    duplicate = p.dedupe(check)
    assert not duplicate


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


def test_straight_wheel():
    board12 = flop12 + turn12 + river12
    straight = p.find_straight(hand12, board12)
    assert straight


def test_not_straight_flush():
    board = flop1 + turn1 + river1
    straight_flush = p.find_straight_flush(hand1, board)
    assert not straight_flush

def test_not_straight_flush_flush():
    board = flop2 + turn2 + river2
    straight_flush = p.find_straight_flush(hand2, board)
    assert not straight_flush


def test_straight_flush():
    board = flop6 + turn6 + river6
    straight_flush = p.find_straight_flush(hand6, board)
    assert straight_flush
