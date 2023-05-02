# Holdem Percentage Odds and Ratios Calculator

Command line application (for now).  There are two flows:
* Simple Outs and Odds
* Monte Carlo Simulation with Percentages and Odds for a Given Hand/Board combination

## Outs and Odds
Tell the application the number of outs you have to improve your hand, and the application will return the odds of
improving on the turn, river, and turn+river.
#### Usage
`python holdem.py -o N` where `N` is the number of outs.


## Monte Carlo Simulation
Tell the application your hole cards and board as flop, turn, and river.  The application will run 100,000 
simulations of that hand and return the percentage and odds of improving to any poker hand.
#### Usage
`python holdem.py -c Rs Rs -f Rs Rs Rs -t Rs Rs -r Rs` where `Rs` stands for Rank and suit of a card.  

Card ranks must be 2-9, T, J, K, Q, A.  Ranks are case sensitive.
Suits are c, d, h, s.  Suits are case sensitive.

`-c` is the flag for your hole cards.  These must be separated by a space.

`-f` or `--flop` is the optional flag for flop.  Three cards separated by a space.

`-t` or `--turn` is the optional flag for turn.  One card.

`-r` or `--river` is the optional flag for river.  One card.