from Othello import *

import sys
import time


black = 0
white = 0
wins = []

for i in range(0, 10):
    player1name = 'v5'
    player2name = 'v2'
    timeLimit = 2

    exec(f'from {player1name} import *')
    if player1name != 'Human':
        exec(f'player1 = {player1name}({timeLimit})')
    else:
        exec(f'player1 = {player1name}({1e6})')

    exec(f'from {player2name} import *')
    if player2name != 'Human':
        exec(f'player2 = {player2name}({timeLimit})')
    else:
        exec(f'player2 = {player2name}({1e6})')

    size = 0
    if size > 0:
        from Graphics import *
        g = Graphics(size, player1name, player2name)
    else:
        g = None

    state = Othello(numpy.array([Othello.black0, Othello.white0], dtype=numpy.uint64))
    if g is not None:
        g.draw(state)

    moveSequence = []

    while not state.gameOver():
        # print(state)

        if state.getTurn() % 2 == 0:
            player1._startTime = time.time()
            player1.findMove(state)
            move = player1.getMove()
            print(f'Black moves {state.moveToStr(move)}\n')
        else:
            player2._startTime = time.time()
            player2.findMove(state)
            move = player2.getMove()
            print(f'White moves {state.moveToStr(move)}\n')
        state = state.result(move)
        moveSequence.append(move)

        if g is not None:
            g.draw(state)

        # print(f'Discs:   \t{state.count(0)}\t{state.count(1)}')
        # print(f'Stable:  \t{state.stable(0)}\t{state.stable(1)}')
        # print(f'Mobile:  \t{state.mobility(0)}\t{state.mobility(1)}')
        # print(f'Frontier:\t{state.frontier(0)}\t{state.frontier(1)}')
        # print(f'Corner:  \t{state.corner(0)}\t{state.corner(1)}')
        # print()

    print(state)
    if state.winner() == 0:
        print('Black wins!')
        print(state.count(0), 'to', state.count(1))
        black += 1
        wins.append('B')
    elif state.winner() == 1:
        print('White wins!')
        print(state.count(1), 'to', state.count(0))
        white += 1
        wins.append('W')
    else:
        print("It's a draw")
        wins.append('D')

    print()
    print('Moves', ' '.join(state.moveToStr(x) for x in moveSequence))

    print()
    print('Black player stats:')
    player1.stats()
    print()
    print('White player stats:')
    player2.stats()


print(f'Black:  \t{black}')
print(f'White:  \t{white}')
print(f'Wins:  \t{wins}')
