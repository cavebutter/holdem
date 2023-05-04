import poker_functions as p
from fractions import Fraction


def simulation(hand, flop=[], turn=[], river=[], sims=100000):
    passed_board = flop + turn + river
    full_board = 7 # number of cards required to run a sim
    passed_cards = len(hand) + len(passed_board)
    pairs = 0
    two_pairs = 0
    trips = 0
    straights = 0
    flushes = 0
    boats = 0
    quads = 0
    straight_flushes = 0
    for i in range(sims):
        deck = p.generate_deck()
        hole_cards = [p.Card(card) for card in hand]
        for card in hole_cards:
            deck.update_deck(card)
        board = [p.Card(card) for card in passed_board]
        for board_card in passed_board: #  Add board cards to total hand
            deck.update_deck(board_card)
        j = full_board - passed_cards # number of cards required to deal for full board
        for k in range(j): # Add additional cards to make a full board of 7
            deal, deck = deck.deal_card()
            board.append(deal)
        straight_flush = p.find_straight_flush(hole_cards, board)
        if straight_flush:
            straight_flushes += 1
            continue
        elif p.find_multiple(hole_cards, board, 4):
            quads += 1
            continue
        elif p.find_full_house(hole_cards, board):
            boats += 1
            continue
        elif p.find_flush(hole_cards, board):
            flushes += 1
            continue
        elif p.find_straight(hole_cards, board):
            straights += 1
            continue
        elif p.find_multiple(hole_cards, board, 3):
            trips += 1
            continue
        elif p.find_two_pair(hole_cards, board):
            two_pairs += 1
            continue
        elif p.find_multiple(hole_cards, board):
            pairs += 1
            continue
        i += 1
    return sims, pairs, two_pairs, trips, straights, flushes, boats, quads, straight_flushes


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



