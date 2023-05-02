import random
from collections import Counter
from fractions import Fraction
from dataclasses import dataclass
from collections import UserList

import poker_functions

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
    """Detect duplicate cards in a passed collection"""
    unique_cards = []
    duplicate = False
    for card in board:
        if card in unique_cards:
            duplicate = True
            return duplicate
        else:
            unique_cards.append(card)
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
    card_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    rank_value = dict(zip(ranks, card_values))
    suits = ['c', 'd', 'h', 's']
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
        if isinstance(card, poker_functions.Card):
            card_name = card.name
        else:
            card_name = card
        for item in self:
            if card_name == item.name:
                self.deck.remove(item)
        return self


# def convert_total_hand(total_hand):
#     """Takes a list of either strings or Card abjects.  If strings, convert to Cards.  If Cards return Cards."""
#     if type(total_hand[0]) == str:  # The check for Card type was not preventing errors when passed Cards, so added another check to parse_card
#         total_hand = [parse_card(card) for card in total_hand]
#         return total_hand
#
#     else:
#         return total_hand
#
# def find_flush(hand, board):
#     """Does any combination of 5 cards in hand or on board amount to 5 of the same suit"""
#     total_hand = hand + board
#     total_hand = convert_total_hand(total_hand)
#     flush = False
#     c_count = 0
#     d_count = 0
#     h_count = 0
#     s_count = 0
#     for card in total_hand:  #  TODO is there a more elegant way to do this?
#         if card.suit == 'c':
#             c_count += 1
#         elif card.suit == 'd':
#             d_count += 1
#         elif card.suit == 'h':
#             h_count += 1
#         elif card.suit == 's':
#             s_count += 1
#     suits = [c_count, d_count, h_count, s_count]
#     for suit in suits:
#         if suit >= 5:
#             flush = True
#             return flush
#     return flush
#
# def find_multiple(hand, board, n=2):
#     """Is there a pair?"""
#     multiple = False
#     total_hand = hand + board
#     total_hand = convert_total_hand(total_hand)
#     values = [card.value for card in total_hand]
#     c = Counter(values)
#     for value in values:
#         if c[value] == n:
#             multiple = True
#             return multiple
#     return multiple
#
# def find_two_pair(hand, board):
#     """Is there two-pair?"""
#     #  TODO This function is not DRY
#     two_pair = False
#     total_hand = hand + board
#     total_hand = convert_total_hand(total_hand)
#     values = [card.value for card in total_hand]
#     c = Counter(values)
#     for value in values:
#         if c[value] > 1:
#             c.pop(value)
#             for value in values:
#                 if c[value] > 1:
#                     two_pair = True
#                     return two_pair
#     return two_pair
#
# def find_full_house(hand, board):
#     """Is there a full house?"""
#     # Find 3 of a kind
#     boat = False
#     total_hand = hand + board
#     total_hand = convert_total_hand(total_hand)
#     values = [card.value for card in total_hand]
#     c = Counter(values)
#     for value in values:
#         if c[value] == 3:
#             c.pop(value)
#             for value in values:
#                 if c[value] > 1:
#                     boat = True
#                     return boat
#     return boat
#
# def evaluate_straight(five_cards):
#     straight = (max(five_cards) - min(five_cards) + 1) == len(five_cards)
#     return straight
#
#
# def find_straight(hand, board):
#     #  OMG THIS IS SO UGLY
#     straight = False
#     reqd_hand_size = 5
#     total_hand = hand + board
#     total_hand = convert_total_hand(total_hand)
#     values = [card.value for card in total_hand]
#     total_hand = set(values)  # remove pairs
#     values = [item for item in total_hand] # ordered list with pairs removed
#     slices = len(values) - reqd_hand_size
#     if slices < 0: # Is there a way to iterate rather than if-elif?  Should I?
#         straight = False
#         return straight
#     elif slices == 0:
#         straight = evaluate_straight(values)
#         return straight
#     elif slices == 1:
#         list1 = values[0:4]
#         list2 = values[1:5]
#         combos = [list1, list2]
#         for combo in combos:
#             straight = evaluate_straight(combo)
#             if straight:
#                 return straight
#     elif slices == 2:
#         list1 = values[0:5]
#         list2 = values[1:6]
#         list3 = values[2:]
#         combos = [list1, list2, list3]
#         for combo in combos:
#             straight = evaluate_straight(combo)
#             if straight:
#                 return straight
#     return straight
#
#
# def find_straight_flush(hand, board):
#     straight_flush = False
#     flush = find_flush(hand, board)
#     if flush:
#         total_hand = hand + board
#         total_hand = convert_total_hand(total_hand)
#         suits = [card.suit for card in total_hand]
#         c = Counter(suits)
#         flush_suit = c.most_common(1)
#         flush_suit = flush_suit[0][0][0]
#         flush_hand = [card for card in total_hand if card.suit == flush_suit]
#         straight = find_straight(flush_hand, board=[])
#         if straight:
#             straight_flush = True
#             return straight_flush
#     return straight_flush
#
#
#
# #####     SIMULATION     #####
# def simulation(hand, flop=[], turn=[], river=[], sims=100000):
#     passed_board = flop + turn + river
#     full_board = 7 # number of cards required to run a sim
#     passed_cards = len(hand) + len(passed_board)
#     pairs = 0
#     two_pairs = 0
#     trips = 0
#     straights = 0
#     flushes = 0
#     boats = 0
#     quads = 0
#     straight_flushes = 0
#     for i in range(sims):
#         deck = generate_deck()
#         hole_cards = []
#         board = []
#         for hole_card in hand: #  Add hole cards to total hand
#             foo = parse_card(hole_card)
#             hole_cards.append(foo)
#             deck = update_deck(deck, hole_card)
#         for board_card in passed_board: #  Add board cards to total hand
#             bar = parse_card(board_card)
#             board.append(bar)
#             deck = update_deck(deck, board_card)
#         j = full_board - passed_cards # number of cards required to deal for full board
#         for k in range(j): # Add additional cards to make a full board of 7
#             deal, deck = deal_card(deck)
#             board.append(deal)
#         straight_flush = find_straight_flush(hand, board)
#         if straight_flush:
#             straight_flushes += 1
#             continue
#         elif find_multiple(hand, board, 4):
#             quads += 1
#             continue
#         elif find_full_house(hand, board):
#             boats += 1
#             continue
#         elif find_flush(hand, board):
#             flushes += 1
#             continue
#         elif find_straight(hand, board):
#             straights += 1
#             continue
#         elif find_multiple(hand, board, 3):
#             trips += 1
#             continue
#         elif find_two_pair(hand, board):
#             two_pairs += 1
#             continue
#         elif find_multiple(hand, board):
#             pairs += 1
#             continue
#         i += 1
#     return sims, pairs, two_pairs, trips, straights, flushes, boats, quads, straight_flushes
#
#
# #####     MATH     #####
# def percent(hits, sims):
#     percent = round((hits / sims) * 100,0)
#     return percent
#
# def ratio(hits, sims):
#     """Return a ratio (e.g. 3:5) for two input numbers"""
#     percent = round((hits / sims),2)
#     fraction = str(Fraction(percent).limit_denominator())
#     fraction = fraction.replace('/', ':')
#     return fraction

