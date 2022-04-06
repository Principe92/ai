from Othello import *

class Greedy(Player):
  def findMove(self, state):
    actions = state.actions()
    
    if state._turn % 2 == 0:
      best = -10000
      for a in actions:
        result = state.result(a)
        v = self.heuristic(result)
        if v > best:
          best = v
          bestMove = a
    else:
      best = 10000
      for a in actions:
        result = state.result(a)
        v = self.heuristic(result)
        if v < best:
          best = v
          bestMove = a
    self.setMove(bestMove)
    print('\tBest value', best, state.moveToStr(bestMove))
            

  def heuristic(self, state):
    return state.score()
