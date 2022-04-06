from Othello import *


class v5(Player):
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

        edges = {'01': (0, 1),
                 '10': (1, 0),
                 '11': (1, 1),
                 '06': (0, 6),
                 '16': (1, 6),
                 '17': (1, 7),
                 '60': (6, 0),
                 '61': (6, 1),
                 '71': (7, 1),
                 '66': (6, 6),
                 '67': (6, 7),
                 '76': (7, 6)}

        choice = sorted([abs(27 - move), abs(28 - move), abs(35 - move), abs(38 - move)])[0]
        
        penalty = 0
        key = '{0}{1}'.format(row, col)
        if key in edges:
            penalty = 99

        return choice + penalty

    def findMove(self, state):

        self._count += 1
        actions = state.actions()
        depth = 1

        actions = sorted(actions, key=lambda x: self.sort(x), reverse=False)

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

        # actions = sorted(actions, key = lambda x : self.sort(x), reverse=False)

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

        playerIndex = state._turn % 2

        mobility = abs(state.mobility(0) - state.mobility(1))
        corner = abs(state.corner(0) - state.corner(1))
        frontier = abs(state.frontier(0) - state.frontier(1))
        stable = abs(state.stable(0) - state.stable(1))

        # mobility = state.mobility(playerIndex)
        # corner = state.corner(playerIndex)
        # frontier = state.frontier(playerIndex)
        # stable = state.stable(playerIndex)

        core = 0
        edge = 0

        middleTiles = [(3, 3), (3, 4), (4, 3), (4, 4)]
        edges = [(0, 1), (1, 0), (1, 1), (0, 6), (1, 6), (1, 7),
                 (6, 0), (6, 1), (7, 1), (6, 6), (6, 7), (7, 6)]
        corners = [(0, 0), (0, 0), (0, 0), (0, 7), (0, 7), (0, 7),
                   (7, 0), (7, 0), (7, 0), (7, 7), (7, 7), (7, 7)]

        best = 0

        player = state._turn % 2

        # for index in range(0, len(middleTiles)):
        #     tile = middleTiles[index]

        #     piece = state.getPosition(tile[0], tile[1])

        #     if (state._turn % 2 == piece):
        #         core += 1

        # for index in range(0, len(edges)):
        #     tile = edges[index]
        #     ctile = corners[index]

        #     piece = state.getPosition(tile[0], tile[1])
        #     cpiece = state.getPosition(ctile[0], ctile[1])

        #     if (player == piece and player != cpiece):
        #         edge += 1

        # if state._turn % 2 == 0:
        #     player = 0

        # print("\nMobility 0: {0} | Mobility 1: {1}".format(state.mobility(0), state.mobility(1)))
        # print("\nCorner 0: {0} | Corner 1: {1}".format(state.corner(0), state.corner(1)))
        # print("\nFrontier 0: {0} | Frontier 1: {1}".format(state.frontier(0), state.frontier(1)))
        # print("\nStable 0: {0} | Stable 1: {1}".format(state.stable(0), state.stable(1)))
        # print("\n\n")
        # return .4 * mobility + .3 * corner + .1 * frontier + .2 * stable  # state.score()

        # if edge > 0:
            # print("Edge: {0}".format(edge))

        return stable

    def stats(self):
        print(f'Average depth: {self._depthCount/self._count}')
        print(f'Branching factor: {self._childCount / self._parentCount}')
