from Wumpus import *

import random

class RandomSafePlayer(Player):
  def __init__(self, size, timeLimit):
    Player.__init__(self, size, timeLimit)
    
  def findMove(self, position, wumpusDead, observations):
    self._wumpusProbabilities.addObservations(observations)
    
    directions = self.possibleDirections(position)
    while self.timeRemaining():
      self._wumpusProbabilities.addParticles(1000)
      (wumpusProb, goldProb, pitProb, deathProb) = self._wumpusProbabilities.getProbabilities(wumpusDead)
      
      # Find safe actions
      safeActions = []
      for d in directions:
        newPosition = self.adjacent(position, d)
        
        if not wumpusDead and wumpusProb[newPosition] > 0:
          safeActions.append('A' + d)
        if deathProb[newPosition] == 0.:
          safeActions.append(d)
          
      if len(safeActions) > 0:
        self.setMove(random.choice(safeActions))
      else:
        options = []
        for d in directions:
          newPosition = self.adjacent(position, d)
          options.append( (deathProb[newPosition], d) )
        self.setMove(min(options)[1])
    
