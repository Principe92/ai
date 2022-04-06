from Wumpus import *

import sys
import time

playerName = input('Enter the class name for agent (e.g. RandomPlayer): ')
puzzleName = input('Enter the class name for the layout generator (e.g. RandomLayout5): ')
timeLimit = float(input('Enter the time limit for each turn: '))


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

size = int(input('Enter the width of the graphics window (0 for text mode): '))
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
