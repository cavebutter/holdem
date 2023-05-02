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


def test_update_deck_1():
    """Remove a passed card from Deck"""
    deck = p.generate_deck()
    deck.update_deck('Ks')
    cards = [card.name for card in deck]
    assert len(deck) == 51

def test_valid_card():
    check = hand9 + flop9 + turn9 + river9
    valid = p.validate_card(check)
    assert valid


def test_invalid_card():
    check = hand11 + flop11 + turn11 + river11
    valid = p.validate_card(check)
    assert not valid