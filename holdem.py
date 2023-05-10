import sys
import simulation as s
import argparse
from prettytable import PrettyTable

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="Hold 'Em Evaluator",
        description="Odds and Probabilities for Your Hold 'Em Hand",
    )

    parser.add_argument('-c', '--Hole_Cards', nargs=2, metavar="Hole Cards", default=[], help="Your two hole cards")
    parser.add_argument('-f', '--flop', nargs=3, metavar="Flop", default=[], help="The three cards for the flos.  Defaults to blank")
    parser.add_argument('-t', '--turn', nargs=1, metavar="Turn", default=[], help="The card for the turn.  Defaults to blank")
    parser.add_argument('-r', '--river', nargs=1, metavar="River", default=[], help="The card for the river.  Defaults to blank")
    parser.add_argument('-o', '--outs', nargs=1, metavar="Outs", default=0, help="Optional, instead of a hand, pass the "
                                                                                 "number of outs.")

    args = parser.parse_args()

    board = args.flop + args.turn + args.river
    #  Validate arguments
    check = board + args.Hole_Cards
    duplicate = s.dedupe(check)
    if duplicate:
        print("There is a duplicate card.  Please check the board and your hand and try again")
        sys.exit()
    valid = s.validate_card(check)
    if not valid:
            print("At least one of your cards is not valid.  Please try again.")
            sys.exit()
    board_str = ''
    for card in board:
        board_str += card + ' '

    if len(args.Hole_Cards) > 0:
        sim = s.simulation_one_player(args.Hole_Cards, args.flop, args.turn, args.river)
        hc_pct = s.percent(sim[1], sim[0])
        hc_ratio = s.ratio(sim[1], sim[0])
        pair_pct = s.percent(sim[2], sim[0])
        pair_ratio = s.ratio(sim[2], sim[0])
        two_pair_pct = s.percent(sim[3], sim[0])
        two_pair_ratio = s.ratio(sim[3], sim[0])
        three_ok_pct = s.percent(sim[4], sim[0])
        three_ok_ratio = s.ratio(sim[4], sim[0])
        straight_pct = s.percent(sim[5], sim[0])
        straight_ratio =  s.ratio(sim[5], sim[0])
        flush_pct = s.percent(sim[6], sim[0])
        flush_ratio = s.ratio(sim[6], sim[0])
        boat_pct = s.percent(sim[7], sim[0])
        boat_ratio = s.ratio(sim[7], sim[0])
        quads_pct = s.percent(sim[8], sim[0])
        quads_ratio = s.ratio(sim[8], sim[0])
        strt_flush_pct = s.percent(sim[9], sim[0])
        strt_flush_ratio = s.ratio(sim[9], sim[0])

        hole_card_str = args.Hole_Cards[0] + ' ' + args.Hole_Cards[1]

        table = PrettyTable()
        table.field_names = ['Hole Cards', 'Board']
        table.add_row([hole_card_str, board_str])

        odds = PrettyTable()
        odds.add_column('Best Final Hand', ['High Card', 'Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind',
                                            'Straight Flush'])
        odds.add_column('% Prob', [hc_pct, pair_pct, two_pair_pct, three_ok_pct, straight_pct, flush_pct, boat_pct, quads_pct, strt_flush_pct])
        odds.add_column('Odds', [hc_ratio, pair_ratio, two_pair_ratio, three_ok_ratio, straight_ratio, flush_ratio, boat_ratio, quads_ratio, strt_flush_ratio])

        print(table)
        print("We ran your hand and board 100,000 times.  Here's the odds:\n")
        print(odds)

    elif args.outs != []:
        outs = args.outs[0]
        x = PrettyTable()
        x.field_names = ['Outs', 'Turn Odds', 'River Odds', 'Turn+River Odds']
        x.add_row([outs, s.outs[outs][0], s.outs[outs][1],s.outs[outs][2]])

        print(x)
