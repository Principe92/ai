from Wumpus import *

import sys
import time

playerName = 'pokorie_agent'
puzzleName = 'pokorie_layout'
timeLimit = 1


exec(f'from {puzzleName} import *')
exec(f'puzzle = {puzzleName}()')
layout = puzzle.getLayout()

exec(f'from {playerName} import *')
if playerName != 'Human':
    exec(f'player = {playerName}({puzzle.getSize()}, {timeLimit})')
else:
    exec(f'player = {puzzleName}({1e6})')


if not puzzle.valid(layout):
    print('Layout is invalid.  It is either too large or has too many pits.  Or you cannot reach gold.')
    print(layout)
    sys.exit(0)

size = 900
if size > 0:
    print('Importing graphics')
    from Graphics import *
    g = Graphics(puzzle.getSize(), size)
else:
    g = None


state = WumpusWorld(puzzle.getSize(), layout)
observations = state.initialObservations()
player.addObservations(observations)

if g is not None:
    g.draw(state, player.getProbabilities(state._wumpusDead))

turn = 0
while not state.gameOver() and turn < 200:
    turn += 1
    print()
    print('Turn:', turn)
    print(state)
    print('Observations:')
    for o in observations:
        print(f'\t{o}')

    move = player.getMove(state.getPosition(), state._wumpusDead, observations)
    state, observations = state.result(move)

    player.printProbabilities(state._wumpusDead)
    print(f'Player moves {move}\n')

    player.addObservations(observations)

    if g is not None:
        g.draw(state, player.getProbabilities(state._wumpusDead))

print(state)
print('Observations:')
for o in observations:
    print(f'\t{o}')

if turn < 200:
    print(f'You won in {turn} turns')
else:
    print('You lost')
