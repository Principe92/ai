from Othello import *

import sys
import time

player1name = input('Enter the class name for the first player (e.g. MyPlayer): ')
player2name = input('Enter the class name for the second player (e.g. MyPlayer): ')
timeLimit = float(input('Enter the time limit for each turn: '))

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

size = int(input('Enter the width of the graphics window (0 for text mode): '))
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
  print(state)
  
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
    
  print(f'Discs:   \t{state.count(0)}\t{state.count(1)}')
  print(f'Stable:  \t{state.stable(0)}\t{state.stable(1)}')
  print(f'Mobile:  \t{state.mobility(0)}\t{state.mobility(1)}')
  print(f'Frontier:\t{state.frontier(0)}\t{state.frontier(1)}')
  print(f'Corner:  \t{state.corner(0)}\t{state.corner(1)}')
  print()

print(state)
if state.winner() == 0:
  print('Black wins!')
  print(state.count(0), 'to', state.count(1))
elif state.winner() == 1:
  print('White wins!')
  print(state.count(1), 'to', state.count(0))
else:
  print("It's a draw")
  
print()
print('Moves', ' '.join(state.moveToStr(x) for x in moveSequence))

print()
print('Black player stats:')
player1.stats()
print()
print('White player stats:')
player2.stats()
