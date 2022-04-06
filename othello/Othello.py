import numpy
import time
import random

class Othello:
  masks = [ numpy.uint64(0x7F7F7F7F7F7F7F7F), numpy.uint64(0x007F7F7F7F7F7F7F), numpy.uint64(0xFFFFFFFFFFFFFFFF), 
    numpy.uint64(0x00FEFEFEFEFEFEFE), numpy.uint64(0xFEFEFEFEFEFEFEFE), numpy.uint64(0xFEFEFEFEFEFEFE00),
    numpy.uint64(0xFFFFFFFFFFFFFFFF), numpy.uint64(0x7F7F7F7F7F7F7F00) ]
  leftShifts = [ numpy.uint64(0), numpy.uint64(0), numpy.uint64(0), numpy.uint64(0), numpy.uint64(1),
    numpy.uint64(9), numpy.uint64(8), numpy.uint64(7)]
  rightShifts = [numpy.uint64(1), numpy.uint64(9), numpy.uint64(8), numpy.uint64(7), numpy.uint64(0), numpy.uint64(0), numpy.uint64(0), numpy.uint64(0)]  
  
  corners = numpy.uint64(1) | (numpy.uint64(1) << numpy.uint64(7)) | (numpy.uint64(1) << numpy.uint64(56)) | (numpy.uint64(1) << numpy.uint64(63))
  
  leftRight = numpy.uint64(129) | (numpy.uint64(129) << numpy.uint64(8)) | (numpy.uint64(129) << numpy.uint64(16)) | (numpy.uint64(129) << numpy.uint64(24)) | (numpy.uint64(129) << numpy.uint64(32)) | (numpy.uint64(129) << numpy.uint64(40)) | (numpy.uint64(129) << numpy.uint64(48)) | (numpy.uint64(129) << numpy.uint64(56))
  topBottom = numpy.uint64(255) | (numpy.uint64(255) << numpy.uint64(56))
  
  diagonal = (leftRight | topBottom)    
  
  (numpy.uint64(1) << numpy.uint64(8))  
  
  black0 = (numpy.uint64(1)<<numpy.uint64(27))+(numpy.uint64(1)<<numpy.uint64(36))
  white0 = (numpy.uint64(1)<<numpy.uint64(28))+(numpy.uint64(1)<<numpy.uint64(35))
  
  def __init__(self, board):
    self._players = board
    self._turn = 0
    
  def __hash__(self):
    return hash((self._players[0], self._players[1], self._turn))
    
  def __eq__(self, other):
    return (self._players[0], self._players[1], self._turn) == (other._players[0], other._players[1], other._turn)
    
  def reset(self):
    self._players = numpy.array([Othello.black0, Othello.white0], dtype=numpy.uint64)
    self._turn = 0
    
  def getTurn(self):
    return self._turn
     
  def actions(self):
    disks = self._players[self._turn]
    oppDisks = self._players[1-self._turn]
    empty = ~(disks | oppDisks)
    moves = numpy.uint64(0)
    
    for direction in range(8):
      x = self._shift(disks, direction) & oppDisks
      
      x |= self._shift(x, direction) & oppDisks
      x |= self._shift(x, direction) & oppDisks
      x |= self._shift(x, direction) & oppDisks
      x |= self._shift(x, direction) & oppDisks
      x |= self._shift(x, direction) & oppDisks
      
      moves |= self._shift(x, direction) & empty      
    
    actions = []
    
    for loc in range(64):
      m = numpy.uint64(1) << numpy.uint64(loc)
      if m & moves == m:
        actions.append(loc)
        
    if len(actions) == 0:
      actions.append(-1)  # Null move
        
    random.shuffle(actions)
    return actions    
    
  def result(self, action):
    if action != -1:
      disks = self._players[self._turn]
      oppDisks = self._players[1-self._turn]
      captured = numpy.uint64(0)
      
      newDisk = numpy.uint64(1) << numpy.uint64(action)
      disks |= newDisk
      
      for direction in range(8):
        x = self._shift(newDisk, direction) & oppDisks
        
        x |= self._shift(x, direction) & oppDisks
        x |= self._shift(x, direction) & oppDisks
        x |= self._shift(x, direction) & oppDisks
        x |= self._shift(x, direction) & oppDisks
        x |= self._shift(x, direction) & oppDisks
        
        boundingDisk = self._shift(x, direction) & disks
        if boundingDisk:
          captured |= x
          
      if self._turn == 0:
        newGame = Othello(numpy.array([disks ^ captured, oppDisks ^ captured], dtype=numpy.uint64))
        newGame._turn = 1
      else:
        newGame = Othello(numpy.array([oppDisks ^ captured, disks ^ captured], dtype=numpy.uint64))
        newGame._turn = 0
        
      return newGame
      
    else:
      newGame = Othello(numpy.copy(self._players))
      newGame._turn = 1 - self._turn
      return newGame
    
  def gameOver(self):
    if ~(self._players[0] | self._players[1]) == numpy.uint64(0):
      return True
    if len(self.actions()) == 1 and self.actions()[0] == -1:
      r = self.result(-1)
      if len(r.actions()) == 1 and r.actions()[0] == -1:
        return True # Neither player can move
    return False
    
  def winner(self):
    if self.score() > 0:
      return 0
    elif self.score() < 0:
      return 1
    else:
      return -1
    
  def score(self):
    b = numpy.uint64(self._players[0])
    w = numpy.uint64(self._players[1])
    
    s = 0
    while b:
      b &= b - numpy.uint64(1)
      s += 1
    while w:
      w &= w - numpy.uint64(1)
      s -= 1
      
    return s
    
  def count(self, player):
    return bin(self._players[player]).count('1')
    
  def stable(self, player):
    board = self._players[player]
    stable = board & Othello.corners
    newStable = numpy.uint64(0)
    
    while stable != newStable:
      stable = newStable
      newStable = board
      
      # LR shifts
      newStable &= Othello.leftRight | ((stable & numpy.uint64(0x7F7F7F7F7F7F7F7F)) << numpy.uint64(1)) | ((stable & numpy.uint64(0xFEFEFEFEFEFEFEFE)) >> numpy.uint64(1))
      
      # UD shifts
      newStable &= Othello.topBottom | (stable  << numpy.uint64(8)) | (stable >> numpy.uint64(8))
      
      # Diagonal
      newStable &= Othello.diagonal | ((stable & numpy.uint64(0xFEFEFEFEFEFEFE00)) >> numpy.uint64(9)) | ((stable & numpy.uint64(0x007F7F7F7F7F7F7F)) << numpy.uint64(9))
      newStable &= Othello.diagonal | ((stable & numpy.uint64(0x7F7F7F7F7F7F7F00)) >> numpy.uint64(7)) | ((stable & numpy.uint64(0x00FEFEFEFEFEFEFE)) << numpy.uint64(7))
    
    count = 0
    while stable:
      stable &= stable - numpy.uint64(1)
      count += 1
    return count
    
  def frontier(self, player):
    empty = ~(self._players[0] | self._players[1])
    
    adjacent = (empty & numpy.uint64(0x7F7F7F7F7F7F7F7F)) << numpy.uint64(1)
    adjacent |= (empty & numpy.uint64(0xFEFEFEFEFEFEFEFE)) >> numpy.uint64(1)
    adjacent |= empty >> numpy.uint64(8)
    adjacent |= empty << numpy.uint64(8)
    adjacent |= (empty & numpy.uint64(0x007F7F7F7F7F7F7F)) << numpy.uint64(9) 
    adjacent |= (empty & numpy.uint64(0xFEFEFEFEFEFEFE00)) >> numpy.uint64(9)
    adjacent |= (empty & numpy.uint64(0x00FEFEFEFEFEFEFE)) << numpy.uint64(7) 
    adjacent |= (empty & numpy.uint64(0x7F7F7F7F7F7F7F00)) >> numpy.uint64(7)
    
    frontier = adjacent & self._players[player]
    
    count = 0
    while frontier:
      frontier &= frontier - numpy.uint64(1)
      count += 1
    return count
    
  def mobility(self, player):
    if player == self._turn:
      a = self.actions()
    else:
      null = Othello(numpy.copy(self._players))
      null._turn = 1 - self._turn
      a = null.actions()
    
    if len(a) == 1 and a[0] == -1:
      return 0
    return len(a)
    
  def corner(self, player):
    c = self._players[player] & Othello.corners
    
    count = 0
    while c:
      c &= c - numpy.uint64(1)
      count += 1
    return count    
    
  def __str__(self):
    t = ['black', 'white'][self._turn]
    s = f'Turn: {t}\n\n'
    s += '  '
    for i in range(8):
      s += chr(ord('A')+i)
    s += '\n'
    s += ' +' + '-'*8 + '+\n'
    for row in range(8):
      s += chr(ord('A') + row)
      s += '|'
      for col in range(8):
        p = self.getPosition(row,col)
        if p == 0:
          s += 'B'
        elif p == 1:
          s += 'W'
        else:
          s += ' '
      s += '|' + chr(ord('A') + row) + '\n'
    s += ' +' + '-'*8 + '+\n'
    s += '  '
    for i in range(8):
      s += chr(ord('A')+i)
    s += '\n'
    return s
    
  def moveToStr(self, move):
    if move == -1:
      return '--'
    else:
      row = move // 8
      col = move % 8
      return chr(ord('A')+row) + chr(ord('A')+col)
      

  def getPosition(self, row, col):
    pos = numpy.uint64(8*row+col)
    if (numpy.uint64(1) << pos) & self._players[0]:
      return 0
    elif (numpy.uint64(1) << pos) & self._players[1]:
      return 1
    return -1
    
  def _shift(self, disks, direction):
    if direction < 4:
      return (disks >> Othello.rightShifts[direction]) & Othello.masks[direction]
    else:
      return (disks << Othello.leftShifts[direction]) & Othello.masks[direction]
    
    
class Player:
  def __init__(self, timeLimit):
    self._timeLimit = timeLimit
    self._startTime = 0
    self._move = None
    
  def timeRemaining(self):
    if time.time() < self._startTime + self._timeLimit:
      return True
    return False

  def setMove(self, move):
    if self.timeRemaining():
      self._move = move
    
  def getMove(self):
    return self._move
    
  def stats(self):
    pass

  
