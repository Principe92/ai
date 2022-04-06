from Othello import *

import time

moveSequence = input('Enter the move sequence: ')
delay = float(input('Enter the time delay (0 to wait for user input): '))
size = int(input('Enter the width of the graphics window (0 for text mode): '))
if size > 0:
  from Graphics import *
  g = Graphics(size, 'Black', 'White')
else:
  g = None

state = Othello(numpy.array([Othello.black0, Othello.white0], dtype=numpy.uint64))
print(state)
if delay > 0:
  time.sleep(delay)
else:
  input('Hit enter to continue')
  
for m in moveSequence.strip().split():
  if m == '--':
    a = 0
  else:
    a = 8*(ord(m[0]) - ord('A')) + (ord(m[1]) - ord('A'))
  state = state.result(a)
  
  if state.getTurn() % 2 == 0:
    print(f'Black moves {m}')
  else:
    print(f'White moves {m}')
    
  print()
  print(state)
  
  if g is not None:
    g.draw(state)
  
  print(f'Discs:   \t{state.count(0)}\t{state.count(1)}')
  print(f'Stable:  \t{state.stable(0)}\t{state.stable(1)}')
  print(f'Mobile:  \t{state.mobility(0)}\t{state.mobility(1)}')
  print(f'Frontier:\t{state.frontier(0)}\t{state.frontier(1)}')
  print(f'Corner:  \t{state.corner(0)}\t{state.corner(1)}')
  print()
  
  if delay > 0:
    time.sleep(delay)
  else:
    input('Hit enter to continue')

if state.winner() == 0:
  print('Black wins!')
elif state.winner() == 1:
  print('white wins!')
else:
  print("It's a draw")
