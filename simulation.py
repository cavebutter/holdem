import poker_functions as p
from fractions import Fraction
from collections import Counter




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
    deck = p.generate_deck()
    valid_cards = [card.name for card in deck]
    for card in check:
        if card not in valid_cards:
            valid = False
            return valid
    return valid


def convert_and_update(deck, cards):
    if len(cards) == 0:
        return deck, cards
    else:
        cards = p.make_card(cards)
        for card in cards:
            deck.update_deck(card)
        return deck, cards

#####     SIMULATIONS     #####
def evaluate_hand(hole_cards, flop=[], turn=[], river=[]):
    board = flop + turn + river
    hand = None
    if len(hole_cards + board) < 5:
        return hand
    else:
        for func in p.HAND_REGISTRY:
            func = func(hole_cards, board)
            if not func:
                continue
            else:
                return func

def simulation_one_player(hole, flop=[], turn=[], river=[], sims=100000):
    full_board = 7 # number of cards required to run sim
    passed_cards = len(hole) + len(flop) + len(turn) + len(river)
    passed_flop = [item for item in flop]
    high_cards = 0
    pairs = 0
    two_pairs = 0
    trips = 0
    straights = 0
    flushes = 0
    boats = 0
    quads = 0
    straight_flushes = 0
    invalid = 0
    for i in range(sims):
        deck = p.generate_deck()
        deck, hole = convert_and_update(deck, hole)
        deck, flop = convert_and_update(deck, flop)
        deck, turn = convert_and_update(deck, turn)
        deck, river = convert_and_update(deck, river)
        j = full_board - passed_cards
        for k in range(j):  # Add additional cards to make a full board of 7
            deal, deck = deck.deal_card()
            flop.append(deal)  # Adding to flop because it shouldn't matter
        hand = evaluate_hand(hole, flop, turn, river)
        if hand.type == 'straight_flush':
            straight_flushes += 1
        elif hand.type == '4ok':
            quads += 1
        elif hand.type == 'boat':
            boats += 1
        elif hand.type == 'flush':
            flushes += 1
        elif hand.type == 'straight':
            straights += 1
        elif hand.type == '3ok':
            trips += 1
        elif hand.type == '2pair':
            two_pairs += 1
        elif hand.type == 'pair':
            pairs += 1
        elif hand.type == 'hc':
            high_cards += 1
        else:
            invalid += 1
        i += 1
        flop = [item for item in passed_flop] # Reset flop back to original
    return sims, high_cards, pairs, two_pairs, trips, straights, flushes, boats, quads, straight_flushes

# def simulation_one_player(hand, flop=[], turn=[], river=[], sims=100000):
#     passed_board = flop + turn + river
#     full_board = 7 # number of cards required to run a sim
#     passed_cards = len(hand) + len(passed_board)
#     high_cards = 0
#     pairs = 0
#     two_pairs = 0
#     trips = 0
#     straights = 0
#     flushes = 0
#     boats = 0
#     quads = 0
#     straight_flushes = 0
#     for i in range(sims):
#         deck = p.generate_deck()
#         hole_cards = [p.Card(card) for card in hand]
#         for card in hole_cards:
#             deck.update_deck(card)
#         board = [p.Card(card) for card in passed_board]
#         for board_card in passed_board: #  Add board cards to total hand
#             deck.update_deck(board_card)
#         j = full_board - passed_cards # number of cards required to deal for full board
#         for k in range(j): # Add additional cards to make a full board of 7
#             deal, deck = deck.deal_card()
#             board.append(deal)
#         straight_flush, straight_flush_hand = p.find_straight_flush(hand, board)
#         if straight_flush is True:
#             straight_flushes += 1
#             continue
#         else:
#             quad, quad_hand = p.find_multiple(hand, board, n=4)
#             if quad is True:
#                 quads += 1
#                 continue
#             else:
#                 boat, boat_hand = p.find_full_house(hand, board)
#                 if boat is True:
#                     boats += 1
#                     continue
#                 else:
#                     flush, flush_hand = p.find_flush(hand, board)
#                     if flush is True:
#                         flushes += 1
#                         continue
#                     else:
#                         straight, straight_hand = p.find_straight(hand, board)
#                         if straight is True:
#                             straights += 1
#                             continue
#                         else:
#                             trip, trip_hand = p.find_multiple(hand, board, n=3)
#                             if trip is True:
#                                 trips += 1
#                                 continue
#                             else:
#                                 two_pair, two_pair_hand = p.find_two_pair(hand, board)
#                                 if two_pair is True:
#                                     two_pairs += 1
#                                     continue
#                                 else:
#                                     pair, pair_hand = p.find_multiple(hand, board)
#                                     if pair is True:
#                                         pairs += 1
#                                         continue
#                                     else:
#                                         hc, high_card_hand = p.find_high_card(hand, board)
#                                         high_cards += 1
#         i += 1
#     return sims, high_cards, pairs, two_pairs, trips, straights, flushes, boats, quads, straight_flushes






#####     MATH     #####
def percent(hits, sims):
    percent = round((hits / sims) * 100,0)
    return percent

def ratio(hits, sims):
    """Return a ratio (e.g. 3:5) for two input numbers"""
    percent = round((hits / sims),2)
    fraction = str(Fraction(percent).limit_denominator())
    fraction = fraction.replace('/', ':')
    return fraction


#####     REFERENCE     #####
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


rank_value = p.rank_value