import copy
import random
import time
from collections import defaultdict 

class WumpusWorld:
  def __init__(self, size, layout):
    self._size = size
    self._wumpusDead = False
    self._gameOver = False
    
    self._wumpus = layout[0]
    self._gold = layout[1]
    self._pits = set(layout[2])
      
    self._position = (0,0)
    self._score = 0
    
    self._observations = set()
    self._visited = set([(0,0)])

  def score(self):
    return self._score
    
  def gameOver(self):
    return self._gameOver
    
  def getPosition(self):
    return self._position
    
  def actions(self):
    l = ['N','E','S','W','AN','AS','AE','AW']
    random.shufle(l)
    return l
    
  def result(self, action):
    observations = []
    result = copy.deepcopy(self)  
      
    # Returns a pair  (state, list of observations)
    (x,y) = result._position
    if action == 'W':
      if y > 0: result._position = (x,y-1)
      result._score -= 1
    elif action == 'S':
      if x < result._size-1: result._position = (x+1,y)  
      result._score -= 1
    elif action == 'E':
      if y < result._size-1: result._position = (x,y+1)  
      result._score -= 1
    elif action == 'N':
      if x > 0: result._position = (x-1,y) 
      result._score -= 1
      
    elif len(action) > 0 and action[0] == 'A':
      candidates = list()
      self._score -= 100
      if action == 'AW':
        for i in range(y,-1,-1):
          candidates.append((x,i))
      elif action == 'AE':
        for i in range(y,result._size,1):
          candidates.append((x,i))
      elif action == 'AS':
        for i in range(x,result._size,1):
          candidates.append((i,y))
      elif action == 'AN':
        for i in range(x,-1,-1):
          candidates.append((i,y))
    
      if result._wumpus in candidates:
        if not result._wumpusDead:  result._score += 200
        result._wumpusDead = True
        observations.append(('Arrow hit', tuple(candidates)))
      else:
        observations.append(('Arrow miss', tuple(candidates)))
        
    result._visited.add(result._position)
        
    # Update observations
    died = False
    if result._position == result._wumpus:
      observations.append( ('Wumpus', result._position) )
      if not result._wumpusDead:
        result._score -= 1000
        result._position = (0,0)
        died = True
    else:
      observations.append( ('No wumpus', result._position) )
    if result._position == result._gold:
      observations.append( ('Gold', result._position) )
      result._score += 10000
      result._gameOver = True
    else:
      observations.append( ('No gold', result._position) )
    if result._position in self._pits:
      observations.append( ('Pit', result._position) )
      result._score -= 1000
      result._position = (0,0)
      died = True
    else:
      observations.append( ('No pit', result._position) )
      
    if not died:
      smell = False
      breeze = False
      (x,y) = result._position
      for p in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
        if p == result._wumpus:
          smell = True
        if p in result._pits:
          breeze = True          
      if smell:
        observations.append( ('Smell', result._position) )
      else:
        observations.append( ('No smell', result._position) )
      if breeze:
        observations.append( ('Breeze', result._position) )
      else:
        observations.append( ('No breeze', result._position) )
    
    for o in observations:
      result._observations.add(o)
    
    return result, observations
    
  def initialObservations(self):
    observations = list()
    
    observations.append(('No wumpus', (0,0)))
    observations.append(('No gold', (0,0)))
    observations.append(('No pit', (0,0)))
    
    if (0,1) in self._pits or (1,0) in self._pits:
      observations.append(('Breeze', (0,0)))
    else:
      observations.append(('No breeze', (0,0)))
      
    if (0,1) == self._wumpus or (1,0) == self._wumpus:
      observations.append(('Smell', (0,0)))
    else:
      observations.append(('No smell', (0,0)))
      
    return observations
    
  def __str__(self):
    s = '\n'
    s += f'Score {self._score}\n'
    s += f'Player at {self._position}\n'
    
    s += '+' + ('----+' * self._size) + '\n'
    
    for row in range(self._size):
      s += '|'
      for col in range(self._size):
        if (row,col) in self._visited:
          if ('Smell', (row,col)) in self._observations:
            s += 'S'
          elif ('Wumpus', (row, col)) in self._observations:
            if self._wumpusDead:
              s += 'D'
            else:
              s += 'W'
          else:
            s += ' '
            
          if ('Gold', (row,col)) in self._observations:
            s += 'G'
          else:
            s += ' '
            
          if ('Pit', (row,col)) in self._observations:
            s += 'P'
          elif ('Breeze', (row,col)) in self._observations:
            s += 'B'
          else:
            s += ' '
            
        else:
          s += '???'
          
        wumpusHit = False
        wumpusMissed = False
        for (m, p) in self._observations:
          if m == 'Arrow hit' and (row,col) in p:
            wumpusHit = True
          if m == 'Arrow miss' and (row,col) in p:
            wumpusMissed = True
            
        if wumpusHit:
          s += 'H'
        elif wumpusMissed:
          s += 'M'
        else:
          s += ' '
        
        s += '|'
        
      s += '\n'          
      s += '+' + ('----+' * self._size) + '\n'
        
    return s

class Player:
  def __init__(self, size, timeLimit):
    self._size = size
    self._timeLimit = timeLimit
    self._startTime = 0
    self._move = None
    
    self._wumpusProbabilities = WumpusProbabilities(size)
    
  def mapSize(self):
    return self._size
    
  def timeRemaining(self):
    if time.time() < self._startTime + self._timeLimit:
      return True
    return False

  def setMove(self, move):
    if self.timeRemaining():
      self._move = move
    
  def getMove(self, position, wumpusDead, observations):
    self._startTime = time.time()
    self.findMove(position, wumpusDead, observations)
    return self._move
    
  def possibleDirections(self, position):
    possible = []
    if position[0] > 0:
      possible.append('N')
    if position[0] < self._size - 1:
      possible.append('S')
    if position[1] > 0:
      possible.append('W')
    if position[1] < self._size - 1:
      possible.append('E')
      
    random.shuffle(possible)
    return possible 
    
  def adjacent(self, position, direction):
    if direction == 'N':
      return (position[0]-1, position[1])
    if direction == 'S':
      return (position[0]+1, position[1])
    if direction == 'E':
      return (position[0], position[1]+1)
    if direction == 'W':
      return (position[0], position[1]-1)
    
  def getProbabilities(self, wumpusDead=False):
    return self._wumpusProbabilities.getProbabilities(wumpusDead)
    
  def addObservations(self, observations):
    self._wumpusProbabilities.addObservations(observations)
    
  def printProbabilities(self, wumpusDead=False):
    (wumpusProb, goldProb, pitProb, deathProb) = self.getProbabilities(wumpusDead)
    
    print()
    print('Wumpus probabilities:')
    self._printProb(wumpusProb)
    print()
    print('Gold probabilities:')
    self._printProb(goldProb)
    print()
    print('Pit probabilities:')
    self._printProb(pitProb)
    print()
    print('Death probabilities:')
    self._printProb(deathProb)
    print()
    
  def _printProb(self, prob):
    print('+' + ('----+' * self._size))
    for row in range(self._size):
      print('|', end='')
      for col in range(self._size):
        print(f'{int(round(1000*prob[(row,col)])):4}', end='|')
      print()
      print('+' + ('----+' * self._size))

class Layout:
  def valid(self, layout):
    (wumpus, gold, pits) = layout
    
    # Nothing at (0,0)
    if wumpus == (0,0):
      return False
    if gold == (0,0):
      return False
    if (0,0) in pits:
      return False    
      
    # Gold in put
    if gold in pits:
      return False
    
    # Path to gold
    size = self.getSize()
    
    component = set()
    component.add( (0,0) )
    changed = True
    while changed:
      oldSize = len(component)
      
      adjacent = []
      for (x,y) in component:
        if x > 1:
          adjacent.append( (x-1,y) )
        if x < size-1:
          adjacent.append( (x+1,y) )
        if y > 0:
          adjacent.append( (x,y-1) )
        if y < size-1:
          adjacent.append( (x,y+1) )
          
      for a in adjacent:
        if a not in pits and a not in component:
          component.add(a)
          
      changed = len(component) != oldSize
      
    if gold not in component:
      return False
      
    return True  
    
  def randomLayout(self, size):
    layout = ( (0,0), (0,0), [] )
    while not self.valid(layout):
      wumpus = (0,0)
      while wumpus == (0,0):
        wumpus = ( random.randint(0,size-1), random.randint(0,size-1) )
      self._wumpus = wumpus
      gold = (0,0)
      while gold == (0,0):
        gold = ( random.randint(0,size-1), random.randint(0,size-1) )
        
      pits = set() 
      for x in range(size):
        for y in range(size):
          if (x,y) != (0,0) and random.random() < .2 and (x,y) != gold:
            pits.add((x,y))
            
      layout = (wumpus, gold, pits)
      
    return layout

class WumpusProbabilities:
  def __init__(self, size):
    self._size = size
    self._possibleWumpus = set()
    self._possibleGold = set()
    self._noPit = set()
    self._pit = set()
    self._possiblePit = set()
    
    self._breeze = set()
    self._noBreeze = set()
    self._smell = set()
    self._noSmell = set()
    
    self._particles = list()
    
    for row in range(self._size):
      for col in range(self._size):
        if (row,col) != (0,0):
          self._possibleWumpus.add((row,col))
          self._possibleGold.add((row,col))
          
  def addObservations(self, observations):    
    for (m, p) in observations:
      if m == 'Arrow hit':
        self._possibleWumpus = set([x for x in self._possibleWumpus if x  in p])
      elif m == 'Arrow miss':
        for x in p:
          self._possibleWumpus.discard(x)
      elif m == 'Wumpus':
        self._possibleWumpus = set([p])
      elif m == 'No wumpus':
        self._possibleWumpus.discard(p)
      elif m == 'Gold':
        self._possibleGold = set([p])
      elif m == 'No gold':
        self._possibleGold.discard(p)
      elif m == 'Pit':
        self._pit.add(p)
      elif m == 'No pit':
        self._noPit.add(p)
        self._possiblePit.discard(p)
      elif m == 'Breeze':
        self._breeze.add(p)
        for (r,c) in [ (p[0]-1,p[1]), (p[0]+1,p[1]), (p[0],p[1]-1), (p[0],p[1]+1) ]:
          if 0<=r<self._size and 0<=c<self._size:
            self._possiblePit.add((r,c))
      elif m == 'No breeze':
        self._noBreeze.add(p)
        # No pit adjacent
        for (r,c) in [ (p[0]-1,p[1]), (p[0]+1,p[1]), (p[0],p[1]-1), (p[0],p[1]+1) ]:
          if 0<=r<self._size and 0<=c<self._size:
            self._noPit.add((r,c))
      elif m == 'Smell':
        self._smell.add(p)
        # No wumpus further away
        adjacentPositions = [ (p[0]-1,p[1]), (p[0]+1,p[1]), (p[0],p[1]-1), (p[0],p[1]+1) ]
        self._possibleWumpus = set([x for x in self._possibleWumpus if x in adjacentPositions])
      elif m == 'No smell':
        self._noSmell.add(p)
        # No wumpus adjacent
        for (r,c) in [ (p[0]-1,p[1]), (p[0]+1,p[1]), (p[0],p[1]-1), (p[0],p[1]+1) ]:
          if 0<=r<self._size and 0<=c<self._size:
            self._possibleWumpus.discard((r,c))
        
      else:
        print('ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(m, p)
        
    self._particles = [ p for p in self._particles if self.particleValid(p) ]
    
  def clearParticles(self):
    self._particles = list()
    
  def getParticles(self):
    return self._particles
    
  def numParticles(self):
    return len(self._particles)
    
  def getParticles(self):
    return self._particles
    
  def pruneParticles(self, num):
    self._particles = self._particles[:num]
    
  def addParticles(self, num):
    goalSize = len(self._particles) + num
    attempts = 0
    increase = goalSize - len(self._particles)
    while len(self._particles) < goalSize:
      attempts += 1
      if attempts % 100 == 0: print (attempts)
      wumpus = random.choice(list(self._possibleWumpus))
      gold = random.choice(list(self._possibleGold))
        
      pits = set() 
      
      # Deal with possible pits
      assigned = set()
      for p in self._breeze:
        adjacent = []
        for (r,c) in [ (p[0]-1,p[1]), (p[0]+1,p[1]), (p[0],p[1]-1), (p[0],p[1]+1) ]:
          if 0<=r<self._size and 0<=c<self._size:
            if (r,c) not in self._noPit:
              adjacent.append((r,c))
        
        pick = random.choice(adjacent)
        if pick not in assigned:
          pits.add(pick)
          assigned.add(p)
          
      for x in range(self._size):
        for y in range(self._size):
          if (x,y) in self._pit:
            pits.add((x,y))
          elif (x,y) in self._noPit:
            pass
          elif (x,y) not in assigned and random.random() < .2 and (x,y) != gold and (x,y) != (0,0):
            pits.add((x,y))
            
            
      layout = (wumpus, gold, pits)
      
      if self.particleValid(layout):
        self._particles.append(layout)
    
  def particleValid(self, particle):
    (wumpus, gold, pits) = particle
    
    # Make sure wumpus is consistent with observations
    if wumpus not in self._possibleWumpus:
      return False
    for (r,c) in [ (wumpus[0], wumpus[1]-1), (wumpus[0], wumpus[1]+1), (wumpus[0]-1, wumpus[1]), (wumpus[0]+1, wumpus[1]) ]:
      if (r,c) in self._noSmell:
        return False
    for p in self._smell:
      adjacent = False
      for (r,c) in [ (p[0], p[1]-1), (p[0], p[1]+1), (p[0]-1, p[1]), (p[0]+1, p[1]) ]:
        if wumpus == (r,c):
          adjacent = True
      if not adjacent:
        return False
      
    # Make sure gold is consistent
    if gold not in self._possibleGold:
      return False
      
    # Make sure gold is not in a pit
    if gold in pits:
      return False
      
    # Make sure pits are consistent with observations
    for p in pits:
      if p in self._noPit:
        return False
      
      # If breeze isn't felt in adjacent squares it's an issue
      for (r,c) in [ (p[0], p[1]-1), (p[0], p[1]+1), (p[0]-1, p[1]), (p[0]+1, p[1]) ]:
        if (r,c) in self._noBreeze:
          return False
          
    for p in self._pit:
      if p not in pits:
        return False
        
    for p in self._breeze:
      # There had better be an adjacent pit
      adjacent = False
      for (r,c) in [ (p[0], p[1]-1), (p[0], p[1]+1), (p[0]-1, p[1]), (p[0]+1, p[1]) ]:
        if (r,c) in pits:
          adjacent = True
          break
      if not adjacent: return False
      
    # Is there a path to the gold
    component = set()
    component.add( (0,0) )
    changed = True
    while changed:
      oldSize = len(component)
      
      adjacent = []
      for (x,y) in component:
        if x > 1:
          adjacent.append( (x-1,y) )
        if x < self._size-1:
          adjacent.append( (x+1,y) )
        if y > 1:
          adjacent.append( (x,y-1) )
        if y < self._size-1:
          adjacent.append( (x,y+1) )
          
      for a in adjacent:
        if a not in pits and a not in component:
          component.add(a)
          
      changed = len(component) != oldSize
      
    if gold not in component:
      return False
        
    return True
    
  def getProbabilities(self, wumpusDead=False):
    wumpusProb = defaultdict(float)
    goldProb = defaultdict(float)
    pitProb = defaultdict(float)
    deathProb = defaultdict(float)
    
    if len(self._particles) > 0:
      inc = 1.0 / len(self._particles)
      
      for layout in self._particles:
        (wumpus, gold, pits) = layout
        
        wumpusProb[wumpus] += inc
        if not wumpusDead and wumpus not in pits: deathProb[wumpus] += inc
        goldProb[gold] += inc
        
        for p in pits:
          pitProb[p] += inc
          deathProb[p] += inc
        
    return (wumpusProb, goldProb, pitProb, deathProb)
