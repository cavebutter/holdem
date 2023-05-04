import simulation as s


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
def test_simulation_incomplete_board():
    """Will the sim run without errors with an incomplete board? Minimum result is 1 pair"""
    hand = ['Ac', '3d']
    flop = ['As', '5c', '4d']
    sims = 5
    sim = s.simulation(hand, flop, sims=sims)
    assert sim[0] == 5


def test_no_impossible_straight():
    """Prior to refactor, this hand and others similar would yield a small % of straights"""
    hand = ['As', 'Kd']
    flop = ['Kh', '6c', '4s']
    sim = s.simulation(hand, flop)
    assert sim[4] == 0


def test_duplicate_card():
    check = hand10 + flop10 + turn10 + river10
    duplicate = s.dedupe(check)
    assert duplicate


def test_not_duplicate():
    check = hand9 + flop9 + turn9 + river9
    duplicate = s.dedupe(check)
    assert not duplicate


def test_valid_card():
    check = hand9 + flop9 + turn9 + river9
    valid = s.validate_card(check)
    assert valid


def test_invalid_card():
    check = hand11 + flop11 + turn11 + river11
    valid = s.validate_card(check)
    assert not valid
