import random
from collections import Counter
from dataclasses import dataclass

card_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
rank_value = dict(zip(ranks, card_values))
suits = ['c', 'd', 'h', 's']






def make_card(input_list):
    """Input_list is either a list of Card objects or string Objects.  If Cards, return the cards.
      If string, convert to Card and return"""
    if isinstance(input_list[0], Card):
        return input_list
    else:
        card_list = [Card(card) for card in input_list]
        return card_list




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
        """Select a random card from the deck.  Return the card and the deck with the card removed"""
        i = random.randint(0, len(self)-1)
        card = self[i]
        self.deck.pop(i)
        return card, self

    def update_deck(self, card):
        """Remove card from deck"""
        deck_names = [card.name for card in self.deck]
        if isinstance(card, Card):
            card_name = card.name
        else:
            card_name = card
        deck_idx = deck_names.index(card_name)
        self.deck.pop(deck_idx)



def find_flush(hand, board):
    """Does any combination of 5 cards in hand or on board amount to 5 of the same suit"""
    hand = make_card(hand)
    board = make_card(board)
    total_hand = hand + board
    total_hand_suits = [card.suit for card in total_hand]
    flush = False
    c = Counter(total_hand_suits)
    for suit in total_hand_suits:
        if c[suit] >= 5:
            flush = True
            return flush
    return flush


def find_multiple(hand, board, n=2):
    """Is there a pair, three of a kind, four of a kind/?"""
    hand = make_card(hand)
    board = make_card(board)
    multiple = False
    total_hand = hand + board
    total_hand = [card for card in total_hand]
    values = [card.value for card in total_hand]
    c = Counter(values)
    for value in values:
        if c[value] == n:
            multiple = True
            return multiple
    return multiple


def find_two_pair(hand, board):
    """Is there two-pair?"""
    hand = make_card(hand)
    board = make_card(board)
    two_pair = False
    total_hand = hand + board
    values = [card.value for card in total_hand]
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
    hand = make_card(hand)
    board = make_card(board)
    boat = False
    total_hand = hand + board
    values = [card.value for card in total_hand]
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
    hand = make_card(hand)
    board = make_card(board)
    straight = False
    reqd_hand_size = 5  # required hand size gives us some flexibility at the cost of more lines.  could be more efficient if we say 'if len(values)<5'
    total_hand = hand + board
    values = [*set(card.value for card in total_hand)]
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
    hand = make_card(hand)
    board = make_card(board)
    flush = find_flush(hand, board)
    if flush:
        total_hand = hand + board
        total_hand = [card for card in total_hand]
        hand_suits = [card.suit for card in total_hand]
        c = Counter(hand_suits)
        flush_suit = c.most_common(1)[0][0]
        flush_hand = [card.value for card in total_hand if card.suit == flush_suit]
        straight_flush = evaluate_straight(flush_hand)
        return straight_flush

