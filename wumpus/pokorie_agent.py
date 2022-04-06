from Wumpus import *
from queue import PriorityQueue

import random


class pokorie_agent(Player):
    def __init__(self, size, timeLimit):
        Player.__init__(self, size, timeLimit)
        self._previousPosition = (0, 0)
        self.visited = set([(0,0)])


    
    def targetHeuristic(self, position, probs, target):
        (wumpusProb, goldProb, pitProb, deathProb) = probs
        gold = goldProb[target]
        pit = pitProb[target]
        death = deathProb[target]
        

        d = self.manhattan(position, gold, target)
        h = 1000*gold - d - 1000*pit - 1000*death

        # if target not in self.visited:
            # h += 1000

        return h


    
    def getTarget(self, probs, position):
        (wumpusProb, goldProb, pitProb, deathProb) = probs

        best = -999999999999999999999999999
        target = None

        for (goldPosition, prob) in goldProb.items():
            if target not in self.visited:
                h = self.targetHeuristic(position, probs, goldPosition)
                # print('target: ', goldPosition, ' h: ', h)
                if h > best:
                    best = h
                    target = goldPosition

        # print('final target: ', target)
        return target



    def manhattan(self, position, probs, target):
        #(wumpusProb, goldProb, pitProb, deathProb) = probs

        distance = 0.
        # for (goldPosition, prob) in goldProb.items():
        #     distance += prob * \
        #         (abs(position[0]-goldPosition[0]) +
        #          abs(position[1]-goldPosition[1]))

        distance += (abs(position[0]-target[0])) + (abs(position[1]-target[1]))

        return distance

    def terminal(self, position, probs, target):
        (wumpusProb, goldProb, pitProb, deathProb) = probs

        if self.timeRemaining():
            return position == target

        return True

    def heuristics(self, position, probs, target):
        (wumpusProb, goldProb, pitProb, deathProb) = probs

        mh = self.manhattan(position, probs, target)

        (x, y) = position

        side = 0

        # if x > 0:
        #   adjacent.append( (x-1,y) )
        # if x < self._size-1:
        #   adjacent.append( (x+1,y) )
        # if y > 1:
        #   adjacent.append( (x,y-1) )
        # if y < self._size-1:
        #   adjacent.append( (x,y+1) )

        return mh + 1000*pitProb[position] + 1000*deathProb[position]

    def search(self, position, probs, wumpusDead):
        (wumpusProb, goldProb, pitProb, deathProb) = probs

        frontier = PriorityQueue()
        frontier.put((0, (position, 0)))

        explored = set()
        explored.add(position)

        parent = {}

        best = 0
        bestAction = None

        target = self.getTarget(probs, position)

        while not frontier.empty():

            data = frontier.get()[1]
            currentPosition = data[0]
            depth = data[1]

            directions = self.possibleDirections(currentPosition)

            # print('depth: ', depth)
            # print('directions: ', directions)

            # self._wumpusProbabilities.addParticles(1000)

            # probs = (wumpusProb, goldProb, pitProb,
            #      deathProb) = self._wumpusProbabilities.getProbabilities(wumpusDead)

            # target = self.getTarget(probs)

            # if deathProb[currentPosition] == 1.0:
                # continue

            for d in directions:
                newPosition = self.adjacent(currentPosition, d)

                if newPosition not in explored:
                    parent[newPosition] = (currentPosition, d)

                    if self.terminal(newPosition, probs, target):
                        current = newPosition
                        dir = None

                        while current in parent:
                            dir = parent[current][1]
                            current = parent[current][0]

                        return dir

                    newDepth = depth + 1
                    h = self.heuristics(newPosition, probs, target) + newDepth

                    # if h < best:
                    #     best = h
                    #     bestAction = d

                    # print('h: ', h, ' for: ', newPosition)

                    
                    frontier.put((h, (newPosition, newDepth)))

                    explored.add(newPosition)

        # return bestAction


    def findCost(self, position, direction, probs):
        (wumpusProb, goldProb, pitProb, deathProb) = probs

        db = deathProb[position]
        visited = 0

        if position in self.visited:
            visited = self.visited[position]

        if db == 1:
            cost = db + visited/100
        else:
            cost = db + 10*visited

        #cost = db + visited/100
        return (cost, direction)

    
    def hasShotArrow(self, position, observations):

        for o in observations:
            if o[0] == 'Arrow miss':
                return position in o[1]

        return False

    def updateVisited(self, position, d):

        newPosition = self.adjacent(position, d)

        if newPosition in self.visited:
            self.visited[newPosition] += 1
        else:
            self.visited[newPosition] = 1

    def findMove(self, position, wumpusDead, observations):
        directions = self.possibleDirections(position)

        print('directions: ', directions)

        self.visited.add(position)

        while self.timeRemaining():

            probs = (wumpusProb, goldProb, pitProb,
                    deathProb) = self._wumpusProbabilities.getProbabilities(wumpusDead)

            if self._wumpusProbabilities.numParticles() > 500:
                self._wumpusProbabilities.pruneParticles(500)
            
            self._wumpusProbabilities.addObservations(observations)
            self._wumpusProbabilities.addParticles(500 - self._wumpusProbabilities.numParticles())
            #self._wumpusProbabilities.addParticles(300)

            probs = (wumpusProb, goldProb, pitProb,
                    deathProb) = self._wumpusProbabilities.getProbabilities(wumpusDead)

            bestAction = self.search(position, probs, wumpusDead)
            print('direction: ', bestAction)
            bestNewPosition = self.adjacent(position, bestAction)

            # If their might be a wumpus in that direction shoot otherwise move in that directions
            if not wumpusDead and wumpusProb[bestNewPosition] > 0.3 and not self.hasShotArrow(bestNewPosition, observations):
                self.setMove('A' + bestAction)
            else:
                self.setMove(bestAction)

        # while self.timeRemaining():
        #     probs = (wumpusProb, goldProb, pitProb,
        #              deathProb) = self._wumpusProbabilities.getProbabilities(wumpusDead)

        #     self._wumpusProbabilities.addParticles(1000)

        #     probs = (wumpusProb, goldProb, pitProb,
        #              deathProb) = self._wumpusProbabilities.getProbabilities(wumpusDead)

        #     # Find directions that don't fall in a pit
        #     safeDirections = []
        #     for d in directions:
        #         newPosition = self.adjacent(position, d)
        #         if pitProb[newPosition] < 0.5:
        #             if newPosition not in self.visited:  # Don't go back
        #                 safeDirections.append(d)

        #     print('\nvisited: ', self.visited)
        #     print('directions: ', directions)
        #     print('safe: ', safeDirections)

        #     if len(safeDirections) > 0:
        #         # Find the direction that decreases the average Manhattan distance to gold
        #         smallestAverageDistance = 1e10
        #         for d in safeDirections:
        #             newPosition = self.adjacent(position, d)
        #             distance = 0.
        #             for (goldPosition, prob) in goldProb.items():
        #                 distance += prob * \
        #                     (abs(newPosition[0]-goldPosition[0]) +
        #                      abs(newPosition[1]-goldPosition[1]))

        #             print(d, distance)

        #             if distance < smallestAverageDistance:
        #                 smallestAverageDistance = distance
        #                 bestAction = d
        #                 bestNewPosition = newPosition

        #         # If their might be a wumpus in that direction shoot otherwise move in that directions
        #         if not wumpusDead and wumpusProb[bestNewPosition] > 0.5:
        #             self.setMove('A' + bestAction)
        #         else:
        #             self.setMove(bestAction)
        #             self.updateVisited(position, bestAction)

        #     else:
        #         options = []
        #         for d in directions:
        #             newPosition = self.adjacent(position, d)
        #             options.append(self.findCost(newPosition, d, probs))

        #         move = min(options)[1]
        #         self.setMove(move)
        #         self.updateVisited(position, move)

        self._previousPosition = position
