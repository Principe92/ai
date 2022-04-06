from cs1graphics import *

class Graphics:
  def __init__(self, width, player1, player2):
    scale = width/10
    
    self._canvas = Canvas(width, 12*scale)
    self._canvas.setTitle('Othello: ' + player1 + ' vs ' + player2)
    self._canvas.setBackgroundColor('tan')
    self._canvas.setAutoRefresh(False)
    
    self._turn = Text('Turn: 0')
    self._turn.setFontSize(.85*scale)
    self._turn.moveTo(.5*width, .55*scale)
    self._canvas.add(self._turn)
    
    self._white = Text('White: 0')
    self._white.setFontSize(.85*scale)
    self._white.moveTo(.25*width, 1.5*scale)
    self._canvas.add(self._white)
    
    self._black = Text('Black: 0')
    self._black.setFontSize(.85*scale)
    self._black.moveTo(.75*width, 1.5*scale)
    self._canvas.add(self._black)

    for i in range(8):
      t = Text(chr(ord('A')+i))
      t.setFontSize(.8*scale)
      t.moveTo((1.5+i)*scale, 2.5*scale)
      t.setDepth(-10)
      self._canvas.add(t)
      t = Text(chr(ord('A')+i))
      t.setFontSize(.8*scale)
      t.moveTo((1.5+i)*scale, 11.6*scale)
      t.setDepth(-10)
      self._canvas.add(t)
      t = Text(chr(ord('A')+i))
      t.setFontSize(.8*scale)
      t.moveTo(.5*scale, (3.5+i)*scale)
      t.setDepth(-10)
      self._canvas.add(t)
      t = Text(chr(ord('A')+i))
      t.setFontSize(.8*scale)
      t.moveTo(9.5*scale, (3.5+i)*scale)
      t.setDepth(-10)
      self._canvas.add(t)
      
    for i in range(8):
      l = Path()
      l.setBorderWidth(.01*scale)
      l.addPoint(Point(1*scale,(3.5+i)*scale))
      l.addPoint(Point(9*scale,(3.5+i)*scale))
      self._canvas.add(l)
      l = Path()
      l.setBorderWidth(.01*scale)
      l.addPoint(Point((1.5+i)*scale,3*scale))
      l.addPoint(Point((1.5+i)*scale,11*scale))
      self._canvas.add(l)
      
    self._pieces = []
    for row in range(8):
      l = []
      for col in range(8):
        c = Circle(.45*scale)
        c.moveTo((1.5+col)*scale, (3.5+row)*scale)
        c.setBorderWidth(0)
        self._canvas.add(c)
        l.append(c)
      self._pieces.append(l)
      
    self._canvas.refresh()

  def draw(self, state):
    if state.gameOver():
      t = 'Game over'
    else:
      t = ['Black', 'White'][state.getTurn()]
    self._turn.setMessage(f'Turn: {t}')
    self._white.setMessage(f'Black: {state.count(0)}')
    self._black.setMessage(f'White: {state.count(1)}')
    
    for r in range(8):
      for c in range(8):
        p = state.getPosition(r,c)
        if p == 0:
          self._pieces[r][c].setFillColor('black')
        elif p == 1:
          self._pieces[r][c].setFillColor('white')
        else:
          self._pieces[r][c].setFillColor('transparent')
    
    self._canvas.refresh()
