import random
from collections import Counter
from dataclasses import dataclass

card_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
rank_value = dict(zip(ranks, card_values))
suits = ['c', 'd', 'h', 's']
outs = {'1':('46:1','45:1',"22:1"),
        '2':('22:1','22:1','11:1'),
        '3':('15:1', '14:1', '7:1'),
        '4':('11:1','10:1','5:1'),
        '5':('8.5:1', '8:1','4:1'),
        '6':('7:1','7:1','3:1'),
        '7':('6:1','6:1','2.5:1'),
        '8':('5:1','5:1','2.5:1'),
        '9':('4:1','4:1','2:1'),
        '10':('3.5:1','3.5:1','1.5:1'),
        '11':('3.3:1','3.2:1','1.5:1'),
        '12':('3:1','3:1','1.2:1'),
        }


def dedupe(board):
    duplicate = False
    c = Counter(board)
    for card in board:
        if c[card] > 1:
            duplicate = True
            return duplicate
    return duplicate


def validate_card(check):
    """Detect invalid cards in a passed collection"""
    valid = True
    deck = generate_deck()
    valid_cards = [card.name for card in deck]
    for card in check:
        if card not in valid_cards:
            valid = False
            return valid
    return valid


#####     POKER     #####
@dataclass
class Card:
    def __init__(self, card_str):
        self.rank = str(card_str[0])
        self.suit = card_str[1]
        self.name = self.rank + self.suit
        self.value = rank_value[self.rank]

    def __str__(self):
        return self.name


    def __getitem__(self, item):
        if item == 'rank':
            return self.rank
        elif item == 'suit':
            return self.suit
        elif item == 'name':
            return self.name
        elif item == 'value':
            return self.value


def generate_deck():
    deck = []
    for rank in ranks:
        for suit in suits:
            card_str = rank + suit
            _card = Card(card_str)
            deck.append(_card)
    deck = Deck(deck)
    return deck


class Deck(list):
    def __init__(self, deck):
        self.deck = deck

    def __getitem__(self, item):
        return self.deck[item]

    def __iter__(self):
        for elem in self.deck:
            yield elem

    def __len__(self):
        return len(self.deck)

    def deal_card(self):
        """Select a random card from the deck"""
        i = random.randint(0, len(self)-1)
        card = self[i]
        self.deck.pop(i)
        return card, self

    def update_deck(self, card):
        """Remove card from deck"""
        if isinstance(card, Card):
            card_name = card.name
        else:
            card_name = card
        for item in self:
            if card_name == item.name:
                self.deck.remove(item)
        return self


def find_flush(hand, board):
    """Does any combination of 5 cards in hand or on board amount to 5 of the same suit"""
    total_hand = hand + board
    total_hand_suits = [Card(card).suit for card in total_hand]
    flush = False
    c = Counter(total_hand_suits)
    for suit in total_hand_suits:
        if c[suit] >= 5:
            flush = True
            return flush
    return flush


def find_multiple(hand, board, n=2):
    """Is there a pair, three of a kind, four of a kind/?"""
    multiple = False
    total_hand = hand + board
    total_hand = [Card(card) for card in total_hand]
    values = [card.value for card in total_hand]
    c = Counter(values)
    for value in values:
        if c[value] == n:
            multiple = True
            return multiple
    return multiple


def find_two_pair(hand, board):
    """Is there two-pair?"""
    two_pair = False
    total_hand = hand + board
    values = [Card(card).value for card in total_hand]
    c = Counter(values)
    for value in values:
        if c[value] > 1:
            c.pop(value)
            for value in values:
                if c[value] > 1:
                    two_pair = True
                    return two_pair
    return two_pair


def find_full_house(hand, board):
    """Is there a full house?"""
    boat = False
    total_hand = hand + board
    values = [Card(card).value for card in total_hand]
    c = Counter(values)
    for value in values:
        if c[value] == 3: # This looks overly indented but should offer early exit if there is no 3OK
            c.pop(value)
            for value in values:
                if c[value] > 1:
                    boat = True
                    return boat
    return boat


def evaluate_straight(values):
    """Evaluates a list of card values to determine whether there are 5 consecutive values"""
    straight = False
    count = 0
    for rank in (14, *range(2, 15)):
        if rank in values:
            count += 1
            if count == 5:
                straight = True
                return straight
        else:
            count = 0
    return straight


def find_straight(hand, board):
    """Find a straight in a given hand/board combination"""
    straight = False
    reqd_hand_size = 5  # required hand size gives us some flexibility at the cost of more lines.  could be more efficient if we say 'if len(values)<5'
    total_hand = hand + board
    values = [*set(Card(card).value for card in total_hand)]
    if 14 in values:
        values.append(1)  # Allows for low straight
    values.sort()
    slices = len(values) - reqd_hand_size
    if slices < 0:
        return straight
    else:
        straight = evaluate_straight(values)
        return straight


def find_straight_flush(hand, board):
    """Find a straight flush in a given hand/board combination"""
    flush = find_flush(hand, board)
    if flush:
        total_hand = hand + board
        total_hand = [Card(card) for card in total_hand]
        hand_suits = [card.suit for card in total_hand]
        c = Counter(hand_suits)
        flush_suit = c.most_common(1)[0][0]
        flush_hand = [card.value for card in total_hand if card.suit == flush_suit]
        straight_flush = evaluate_straight(flush_hand)
        return straight_flush

