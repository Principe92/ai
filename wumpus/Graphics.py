from cs1graphics import *

from Wumpus import *

class Graphics:
  def __init__(self, size, screenSize):
    print('Graphics', size, screenSize)
    self._size = size

    # Setup the canvas
    self._largeBlockSize = screenSize/(2.*size+1.5)
    self._smallBlockSize = (screenSize - 2*self._largeBlockSize)/(3*size)
    
    self._canvas = Canvas(screenSize, (size+2.5)*self._largeBlockSize + size*self._smallBlockSize + self._smallBlockSize)
    self._canvas.setTitle('Wumpus')
    self._canvas.setBackgroundColor('white')
    
    # Score
    self._score = Text('Score', .35*self._largeBlockSize, Point(.5*screenSize, (1.5+size)*self._largeBlockSize + (1.5+size)*self._smallBlockSize))
    self._canvas.add(self._score)
    
    # Setup main map
    self._mainOrigin = (self._largeBlockSize, 1.5*self._largeBlockSize)
    t = Text('Map', .5*self._largeBlockSize, Point((.5+.5*size)*self._largeBlockSize, .5*self._largeBlockSize))
    self._canvas.add(t)
    self._mainBlock = {}
    for x in range(size):
      for y in range(size):
        b = TextBox(self._largeBlockSize, self._largeBlockSize, Point(self._mainOrigin[0] + x*self._largeBlockSize, self._mainOrigin[1] + y*self._largeBlockSize))
        b.setFontSize(.175*self._largeBlockSize)
        b.setFillColor('black')
        b.setBorderWidth(.01*self._largeBlockSize)
        self._mainBlock[(y,x)] = b
        self._canvas.add(b)
    
    # Setup death map
    self._deathOrigin = ((1.5+size)*self._largeBlockSize, 1.5*self._largeBlockSize)
    t = Text('Death Prob', .5*self._largeBlockSize, Point((1+1.5*size)*self._largeBlockSize, .5*self._largeBlockSize))
    self._canvas.add(t)
    self._deathBlock = {}
    for x in range(size):
      for y in range(size):
        b = Rectangle(self._largeBlockSize, self._largeBlockSize, Point(self._deathOrigin[0] + x*self._largeBlockSize, self._deathOrigin[1] + y*self._largeBlockSize))
        b.setFillColor('black')
        b.setBorderWidth(0)
        self._deathBlock[(y,x)] = b
        self._canvas.add(b)
    
    # Setup wumpus map
    self._wumpusOrigin = (.5*self._largeBlockSize + .5*self._smallBlockSize, (2+size)*self._largeBlockSize + .5*self._smallBlockSize)
    t = Text('Wumpus', .35*self._largeBlockSize, Point(.5*self._largeBlockSize + .5*size*self._smallBlockSize, (1.5+size)*self._largeBlockSize))
    self._canvas.add(t)
    self._wumpusBlock = {}
    for x in range(size):
      for y in range(size):
        b = Rectangle(self._smallBlockSize, self._smallBlockSize, Point(self._wumpusOrigin[0] + x*self._smallBlockSize, self._wumpusOrigin[1] + y*self._smallBlockSize))
        b.setFillColor('black')
        b.setBorderWidth(0)
        self._wumpusBlock[(y,x)] = b
        self._canvas.add(b)
    
    # Setup pit map
    self._pitOrigin = (self._largeBlockSize + (size+.5)*self._smallBlockSize, (2+size)*self._largeBlockSize + .5*self._smallBlockSize)
    t = Text('Pit', .35*self._largeBlockSize, Point(self._largeBlockSize + 1.5*size*self._smallBlockSize, (1.5+size)*self._largeBlockSize))
    self._canvas.add(t)
    self._pitBlock = {}
    for x in range(size):
      for y in range(size):
        b = Rectangle(self._smallBlockSize, self._smallBlockSize, Point(self._pitOrigin[0] + x*self._smallBlockSize, self._pitOrigin[1] + y*self._smallBlockSize))
        b.setFillColor('black')
        b.setBorderWidth(0)
        self._pitBlock[(y,x)] = b
        self._canvas.add(b)
    
    # Setup gold map
    self._goldOrigin = (1.5*self._largeBlockSize + (2*size+.5)*self._smallBlockSize, (2+size)*self._largeBlockSize + .5*self._smallBlockSize)
    t = Text('Gold', .35*self._largeBlockSize, Point(1.5*self._largeBlockSize + 2.5*size*self._smallBlockSize, (1.5+size)*self._largeBlockSize))
    self._canvas.add(t)
    self._goldBlock = {}
    for x in range(size):
      for y in range(size):
        b = Rectangle(self._smallBlockSize, self._smallBlockSize, Point(self._goldOrigin[0] + x*self._smallBlockSize, self._goldOrigin[1] + y*self._smallBlockSize))
        b.setFillColor('black')
        b.setBorderWidth(0)
        self._goldBlock[(y,x)] = b
        self._canvas.add(b)
        
        
  def draw(self, state, probabilities):
    self._score.setMessage(f'Score: {state._score}')
    for (row, col) in state._visited:
      messages = []
      if ('Smell', (row,col)) in state._observations:
        messages.append('Smell')
      elif ('Wumpus', (row, col)) in state._observations:
        if state._wumpusDead:
          messages.append('Dead W')
        else:
          messages.append('Wumpus')
        
      if ('Gold', (row,col)) in state._observations:
        messages.append('Gold')
        
      if ('Pit', (row,col)) in state._observations:
        messages.append('Pit')
        
      if ('Breeze', (row,col)) in state._observations:
        messages.append('Breeze')
        
      self._mainBlock[(row,col)].setMessage('\n'.join(messages))
      if (row,col) == state._position:
        self._mainBlock[(row,col)].setFillColor('cyan')
      else:
        self._mainBlock[(row,col)].setFillColor('white')
        
    # Draw arrows
    for (m, candidates) in state._observations:
      if m.split(' ')[0] == 'Arrow':
        (y,x) = candidates[0]
        end = candidates[-1][::-1]
        
        l = Path()
        l.addPoint(Point(self._mainOrigin[0]+x*self._largeBlockSize, self._mainOrigin[1] + y*self._largeBlockSize))
        l.addPoint(Point(self._mainOrigin[0]+end[0]*self._largeBlockSize, self._mainOrigin[1] + end[1]*self._largeBlockSize))
        l.setBorderWidth(.05*self._largeBlockSize)
        l.setDepth(-5)
        if m == 'Arrow hit':
          l.setBorderColor('red')
        else:
          l.setBorderColor('green')
        self._canvas.add(l)
      
    # Draw distributions
    (wumpusProb, goldProb, pitProb, deathProb) = probabilities
    for r in range(self._size):
      for c in range(self._size):
        v = wumpusProb[(r,c)]
        self._wumpusBlock[(r,c)].getFillColor().setByValue((int(255*v**.5),0,0))
    for r in range(self._size):
      for c in range(self._size):
        v = goldProb[(r,c)]
        self._goldBlock[(r,c)].getFillColor().setByValue((int(255*v**.5),int(255*v**.5),0))
    for r in range(self._size):
      for c in range(self._size):
        v = pitProb[(r,c)]
        self._pitBlock[(r,c)].getFillColor().setByValue((0,0,int(255*v**.5)))
    for r in range(self._size):
      for c in range(self._size):
        v = deathProb[(r,c)]
        self._deathBlock[(r,c)].getFillColor().setByValue((int(255*v**.5),0,0))
      
    self._canvas.refresh()
