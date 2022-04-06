from Wumpus import *

import random

class GreedySafePlayer(Player):
  def __init__(self, size, timeLimit):
    Player.__init__(self, size, timeLimit)
    self._previousPosition = (0,0)
    
  def findMove(self, position, wumpusDead, observations):
    directions = self.possibleDirections(position)
    while self.timeRemaining():
      (wumpusProb, goldProb, pitProb, deathProb) = self._wumpusProbabilities.getProbabilities(wumpusDead)
      self._wumpusProbabilities.addParticles(1000)
      
      (wumpusProb, goldProb, pitProb, deathProb) = self._wumpusProbabilities.getProbabilities(wumpusDead)
      
      # Find directions that don't fall in a pit
      safeDirections = []
      for d in directions:
        newPosition = self.adjacent(position, d)
        if pitProb[newPosition] == 0.:
          if newPosition != self._previousPosition: # Don't go back
            safeDirections.append(d)
            
      if len(safeDirections) > 0:
        # Find the direction that decreases the average Manhattan distance to gold
        smallestAverageDistance = 1e10
        for d in safeDirections:
          newPosition = self.adjacent(position, d)
          distance = 0.
          for (goldPosition, prob) in goldProb.items():
            distance += prob*(abs(newPosition[0]-goldPosition[0]) + abs(newPosition[1]-goldPosition[1]))
            
          if distance < smallestAverageDistance:
            smallestAverageDistance = distance
            bestAction = d
            bestNewPosition = newPosition
        
        # If their might be a wumpus in that direction shoot otherwise move in that directions
        if not wumpusDead and wumpusProb[bestNewPosition] > 0:
          self.setMove('A' + bestAction)
        else:
          self.setMove(bestAction)
        
      else:
        options = []
        for d in directions:
          newPosition = self.adjacent(position, d)
          options.append( (deathProb[newPosition], d) )
        self.setMove(min(options)[1])
      
    self._previousPosition = position
