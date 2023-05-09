import random
from collections import Counter
from dataclasses import dataclass

card_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
rank_value = dict(zip(ranks, card_values))
value_rank = dict(zip(card_values, ranks))
suits = ['c', 'd', 'h', 's']
hand_values = {'hc': 1,
               'pair': 2,
               '2pair': 3,
               '3ok': 4,
               'straight': 5,
               'flush': 6,
               'boat': 7,
               '4ok': 8,
               'straight_flush': 9
               }





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


@dataclass()
class Hand:
    def __init__(self, type, high_value, low_value = 0, kicker=None):
        """Type = name of hand (e.g. Pair)
        value = value of the hand (i.e. Straight Flush is the most valuable)
        high_value = value.  either the high card in straight or flush, the set in full house, the top pair in 2pair, etc
        low_value = the lower pair in 2 pair or the pair in a full house
        kicker = value of the kicker in the hand.  Can be null
        """
        if kicker in card_values:
            kicker_rank = value_rank[kicker]
        else:
            kicker_rank = 0
        if low_value in card_values:
            low_rank = value_rank[low_value]
        else:
            low_rank = 0
        self.type = type
        self.hand_value = hand_values[type]
        self.kicker = kicker
        self.kicker_rank = kicker_rank
        self.high_value = high_value
        self.high_rank = value_rank[self.high_value]
        self.low_value = low_value
        self.low_rank = low_rank

    def __str__(self):
        return self.type + '-' + self.high_rank

    def __getitem__(self, item):
        if item == 'type':
            return self.type
        elif item == 'hand_value':
            return self.high_value
        elif item == 'kicker':
            return self.kicker
        elif item == 'kicker_rank':
            return self.kicker_rank
        elif item == 'high_value':
            return self.high_value
        elif item == 'high_rank':
            return self.high_rank
        elif item == 'low_value':
            return self.low_value
        elif item == 'low_rank':
            return self.low_rank



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
    flush_hand = None
    c = Counter(total_hand_suits)
    for suit in total_hand_suits:
        if c[suit] >= 5:
            flush = True
    if flush:
        flush_cards = [card for card in total_hand if card.suit == c.most_common(1)[0][0]]
        high_value = max([card.value for card in flush_cards])
        flush_hand = Hand('flush', high_value)
    return flush, flush_hand


def find_multiple(hand, board, n=2):
    """Is there a pair, three of a kind, four of a kind/?"""
    hand = make_card(hand)
    board = make_card(board)
    multiple = False
    multiple_hand = None
    total_hand = hand + board
    values = [card.value for card in total_hand]
    c = Counter(values)
    for value in set(values):
        if c[value] == 2 and n == 2:
            multiple = True
            hand_type = 'pair'
            high_value = value
            kicker = max([value for value in values if value != high_value])
            multiple_hand = Hand(hand_type, high_value, kicker)
            return multiple, multiple_hand
        elif c[value] == 3 and n == 3:
            multiple = True
            hand_type = '3ok'
            high_value = c[value]
            kicker = max([value for value in values if value != high_value])
            multiple_hand = Hand(hand_type, high_value, kicker)
            return multiple, multiple_hand
        elif c[value] == 4 and n == 4:
            multiple = True
            hand_type = '4ok'
            high_value = c[value]
            kicker = max([value for value in values if value != high_value])
            multiple_hand = Hand(hand_type, high_value, kicker)
            return multiple, multiple_hand
    return multiple, multiple_hand


def find_two_pair(hand, board):
    """Is there two-pair?"""
    hand = make_card(hand)
    board = make_card(board)
    two_pair = False
    two_pair_hand = None
    total_hand = hand + board
    values = [card.value for card in total_hand]
    c = Counter(values)
    for value in values:
        if c[value] > 1:
            pair1 = Hand('pair', value)
            c.pop(value)
            for value in values:
                if c[value] > 1:
                    pair2 = Hand('pair', value)
                    kicker = max([value for value in values if value != pair1.high_value and value != pair2.high_value])
                    two_pair_hand = Hand('2pair', max(pair1.high_value, pair2.high_value), low_value=min(pair1.high_value, pair2.high_value), kicker=kicker)
                    two_pair = True
                    return two_pair, two_pair_hand
    return two_pair, two_pair_hand


def find_full_house(hand, board):
    """Is there a full house?"""
    hand = make_card(hand)
    board = make_card(board)
    boat = False
    boat_hand = None
    total_hand = hand + board
    values = [card.value for card in total_hand]
    c = Counter(values)
    for value in set(values):
        if c[value] == 3: # This looks overly indented but should offer early exit if there is no 3OK
            high_value = value
            c.pop(value)
            for value in set(values):
                if c[value] > 1:
                    low_value = value
                    kicker = max([value for value in values if value != high_value and value != low_value])
                    boat_hand = Hand('boat', high_value, low_value=low_value, kicker=kicker)
                    boat = True
                    return boat, boat_hand
    return boat, boat_hand


def evaluate_straight(values):
    """Evaluates a list of card values to determine whether there are 5 consecutive values"""
    straight = False
    count = 0
    straight_hand_values = []
    for rank in (14, *range(2, 15)):
        if rank in values:
            count += 1
            straight_hand_values.append(rank)
            if count == 5:
                straight = True
                return straight, straight_hand_values
        else:
            count = 0
            straight_hand_values = []
    return straight, straight_hand_values


def find_straight(hand, board):
    """Find a straight in a given hand/board combination"""
    hand = make_card(hand)
    board = make_card(board)
    straight = False
    straight_hand = None
    reqd_hand_size = 5  # required hand size gives us some flexibility at the cost of more lines.  could be more efficient if we say 'if len(values)<5'
    total_hand = hand + board
    values = [*set(card.value for card in total_hand)]
    total_hand_values = [card.value for card in total_hand]
    slices = len(values) - reqd_hand_size
    if slices < 0:
        return straight, straight_hand
    else:
        straight, straight_hand_values = evaluate_straight(values)
        if straight:
            hand_type = 'straight'
            if 14 and 5 in straight_hand_values:
                high_card = 5
            else:
                high_card = max(straight_hand_values)
            straight_hand = Hand(hand_type, high_card)
            return straight, straight_hand
        else:
            return straight, straight_hand


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

