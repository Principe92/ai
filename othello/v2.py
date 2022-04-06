from Othello import *


class v2(Player):
    def __init__(self, timeLimit):
        Player.__init__(self, timeLimit)

        self._nodeCount = 0
        self._parentCount = 0
        self._childCount = 0
        self._depthCount = 0
        self._count = 0

    
    def sort(self, move):

        row = move // 8
        col = move % 8

        originalTiles = [(3, 3), (3, 4), (4, 3), (4, 4)]

        best = 0

        for index in range(0, 4):
            tile = originalTiles[index]

            dist = abs(tile[0] - row) + abs(tile[1] - col)

            if (dist <= best or best == 0):
                best = dist

        return best

    def findMove(self, state):

        self._count += 1
        actions = state.actions()
        depth = 1

        # print(actions)

        actions = sorted(actions, key = lambda x : self.sort(x), reverse=False)

        # print(actions)

        while self.timeRemaining():
            self._depthCount += 1
            self._parentCount += 1
            self._nodeCount += 1

            print('Search depth', depth)

            if state._turn % 2 == 0:
                best = -10000

                for a in actions:
                    if not self.timeRemaining():
                        return

                    result = state.result(a)
                    v = self.value(result, depth-1, -10000, 10000)

                    if v is None:
                        return
                    if v > best:
                        best = v
                        bestMove = a
            else:
                best = 10000

                for a in actions:
                    if not self.timeRemaining():
                        return

                    result = state.result(a)
                    v = self.value(result, depth-1, -10000, 10000)

                    if v is None:
                        return
                    if v < best:
                        best = v
                        bestMove = a

            self.setMove(bestMove)
            print('\tBest value', best, state.moveToStr(bestMove))

            depth += 1

            if abs(best) == 1000:
                break

    def value(self, state, depth, alpha, beta):
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
                if not self.timeRemaining():
                    return None

                result = state.result(a)
                v = self.value(result, depth-1, alpha, beta)

                if v is None:
                    return None
                if v > best:
                    best = v

                if v > alpha:
                    alpha = v

                    if alpha >= beta:
                        return best
        else:
            best = 10000
            for a in actions:
                if not self.timeRemaining():
                    return None

                result = state.result(a)
                v = self.value(result, depth-1, alpha, beta)

                if v is None:
                    return None
                if v < best:
                    best = v

                if v < beta:
                    beta = v

                    if alpha >= beta:
                        return best

        return best

    def heuristic(self, state):
        player = -1
        mult = -1

        mobility = abs(state.mobility(0) - state.mobility(1))
        corner = abs(state.corner(0) - state.corner(1))
        frontier = abs(state.frontier(0) - state.frontier(1))
        stable = abs(state.stable(0) - state.stable(1))

        # if state._turn % 2 == 0:
        #     player = 0

        # print("\nMobility 0: {0} | Mobility 1: {1}".format(state.mobility(0), state.mobility(1)))
        # print("\nCorner 0: {0} | Corner 1: {1}".format(state.corner(0), state.corner(1)))
        # print("\nFrontier 0: {0} | Frontier 1: {1}".format(state.frontier(0), state.frontier(1)))
        # print("\nStable 0: {0} | Stable 1: {1}".format(state.stable(0), state.stable(1)))
        # print("\n\n")
        # return .4 * mobility + .3 * corner + .1 * frontier + .2 * stable  # state.score()
        return stable

    def stats(self):
        print(f'Average depth: {self._depthCount/self._count}')
        print(f'Branching factor: {self._childCount / self._parentCount}')
