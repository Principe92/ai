from Othello import *

class MinMax(Player):
  def __init__(self, timeLimit):
    Player.__init__(self, timeLimit)
    
    self._nodeCount = 0
    self._parentCount = 0
    self._childCount = 0
    self._depthCount = 0
    self._count = 0
    
  def findMove(self, state):
    self._count += 1
    actions = state.actions()
    depth = 1
    while self.timeRemaining():
      self._depthCount += 1
      self._parentCount += 1
      self._nodeCount += 1
      print('Search depth', depth)
      if state._turn % 2 == 0:
        best = -10000
        for a in actions:
          if not self.timeRemaining(): return
          result = state.result(a)
          v = self.value(result, depth-1)
          if v is None: return
          if v > best:
            best = v
            bestMove = a
      else:
        best = 10000
        for a in actions:
          if not self.timeRemaining(): return
          result = state.result(a)
          v = self.value(result, depth-1)
          if v is None: return
          if v < best:
            best = v
            bestMove = a
      self.setMove(bestMove)
      print('\tBest value', best, state.moveToStr(bestMove))
            
      depth += 1
      
      if abs(best) == 1000:
        break
            
  def value(self, state, depth):
    self._nodeCount += 1
    self._childCount += 1
    
    actions = state.actions()
    if state.gameOver():
      w = state.winner()
      if w == 0:
        return 1000
      if w == 1:
        return -1000
      return 0
      
    if depth == 0:
      return self.heuristic(state)
    
    self._parentCount += 1

    if state._turn % 2 == 0:
      best = -10000
      for a in actions:
        if not self.timeRemaining(): return None
        result = state.result(a)
        v = self.value(result, depth-1)
        if v is None: return None
        if v > best:
          best = v
    else:
      best = 10000
      for a in actions:
        if not self.timeRemaining(): return None
        result = state.result(a)
        v = self.value(result, depth-1)
        if v is None: return None
        if v < best:
          best = v

    return best

  def heuristic(self, state):
    return state.score()
    
  def stats(self):
    print(f'Average depth: {self._depthCount/self._count}')
    print(f'Branching factor: {self._childCount / self._parentCount}')
