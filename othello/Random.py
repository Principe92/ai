import random
from Othello import *

class Random(Player):
  def __init__(self, timeLimit):
    Player.__init__(self, timeLimit)
  
  def findMove(self, state):
    actions = state.actions()
    self.setMove(random.choice(actions))
