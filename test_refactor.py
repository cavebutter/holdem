import poker_functions as p

# valid card string
card_str1 = 'As'

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
    deck = p.Deck
    assert type(deck) == p.Deck