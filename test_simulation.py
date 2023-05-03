import simulation as s

def test_simulation_incomplete_board():
    """Will the sim run without errors with an incomplete board? Minimum result is 1 pair"""
    hand = ['Ac', '3d']
    flop = ['As', '5c', '4d']
