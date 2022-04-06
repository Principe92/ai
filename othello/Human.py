import random
from Othello import *

class Human(Player):
  def __init__(self, timeLimit):
    Player.__init__(self, timeLimit)
  
  def findMove(self, state):
    move = None
    while move is None:
      print('Move options: ', end='')
      for m in state.actions():
        print(state.moveToStr(m), end=' ')
      print()
      
      move = input('Enter you move (row first then column, e.g CF): ')
      move = move.upper()
      row = ord(move[0]) - ord('A')
      col = ord(move[1]) - ord('A')
      m = 8*row+col
      
      if m not in state.actions():
        print('Invalid move')
        move = None
      
    print('Move', m)
    self.setMove(m)
