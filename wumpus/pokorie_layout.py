from Wumpus import *

import random


class pokorie_layout(Layout):
    def __init__(self):
        self.size = 10 #random.randint(5, 10)

    def getSize(self):
        return self.size

    def getLayout(self):
        # layout = ((0, 0), (0, 0), [])

        wumpus = (1, self.size-1)
        gold = (self.size-1, self.size-1)
        pits = [(0,2), (0,8), (1,7), (2,0), (2,2), (2,7), (3,3), (4,0), (4,4), (4,6), (5,1), (5,5), (5,8), (6,2), (6,6), (7,3), (8,4), (9,7)]
        layout = (wumpus, gold, pits)

        # while not self.valid(layout):
        #     size = self.getSize()
        #     wumpus = (0, 0)

        #     while wumpus == (0, 0):
        #         wumpus = (random.randint(0, size-1), random.randint(0, size-1))
                
        #     self._wumpus = wumpus
        #     gold = (0, size-1)

        #     # while gold == (0, 0):
        #     #     gold = (random.randint(0, size-1), random.randint(0, size-1))

        #     pits = set()

        #     for x in range(size):
        #         for y in range(size):
        #             if (x, y) != (0, 0) and random.random() < .2 and (x, y) != gold:
        #                 pits.add((x, y))

        #     layout = (wumpus, gold, pits)

        return layout
