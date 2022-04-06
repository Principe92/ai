from Wumpus import *

import random

class RandomPlayer(Player):
  def __init__(self, size, timeLimit):
    Player.__init__(self, size, timeLimit)
    
  def findMove(self, position, wumpusDead, observations):
    
    actions = self.possibleDirections(position)
    actions = actions + ['A'+d for d in self.possibleDirections(position)]
    self.setMove(random.choice(actions))
    
    self._wumpusProbabilties.addObservations(observations)
    while self.timeRemaining():
      self._wumpusProbabilities.addParticles(1000)
    
