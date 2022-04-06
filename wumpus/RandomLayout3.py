from Wumpus import *

import random

class RandomLayout3(Layout):
  def getSize(self):
    return 3
    
  def getLayout(self):
    layout = ( (0,0), (0,0), [] )
    while not self.valid(layout):
      size = self.getSize()
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
