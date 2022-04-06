from ShikakuSolver import *


class PartiallySolvedPuzzle:
    def __init__(self, board, options):
        self.board = board
        self.options = options


class pokorie(ShikakuSolver):
    def __init__(self, problem, maxTime, visualizer):
        ShikakuSolver.__init__(self, problem, maxTime, visualizer)

    def infer(self, state):

        infer = False
        keys = list(state.options.keys())

        for key in keys:
            rectangles = state.options[key]
            options = []

            for rect in rectangles:
                consistent = numpy.all(numpy.logical_or(
                    state.board == -1, state.board == key)[rect[0]:rect[0]+rect[2], rect[1]:rect[1]+rect[3]])

                if (consistent):
                    options.append(rect)

            state.options[key] = options

            size = len(options)

            # if no options, stop and backtrack
            if (size == 0):
                return

            # if only an option, fill it
            if (size == 1):
                infer = True
                rect = options[0]
                state.options.pop(key)

                for row in range(rect[0], rect[0]+rect[2]):
                    for col in range(rect[1], rect[1]+rect[3]):
                        state.board[row, col] = key

        if infer:
            return self.infer(state)

    def includesRegion(self, regionId, rectangle, originalRow, originalCol):
        rows = {x: x for x in range(rectangle[0], rectangle[0]+rectangle[2])}
        cols = {x: x for x in range(rectangle[1], rectangle[1]+rectangle[3])}

        return (originalRow in rows and originalCol in cols)

    def solve(self):

        # Setup the possible options
        options = {}

        for i in range(self._problem.numRegions()):
            # Build all possible rectangles of the correct size and add them to
            # the options for that region.  Note there are much better ways
            # to do this.
            size = self._problem.getRegionSize(i)
            originalCordinate = self._problem.getRegionOrigin(i)
            originalRow = originalCordinate[0]
            originalCol = originalCordinate[1]
            rectangles = []

            for height in range(1, size+1):
                if size % height == 0:
                    width = size // height

                    for row in range(0, self._problem.size() - height+1):
                        for col in range(0, self._problem.size() - width+1):

                            if (self.includesRegion(i, (row, col, height, width), originalRow, originalCol)):
                                rectangles.append((row, col, height, width))

            options[i] = rectangles
       
        options = { a[0] : a[1] for a in sorted(options.items(), key = lambda x : self._problem.getRegionSize(x[0]), reverse=True) }

        root = PartiallySolvedPuzzle(copy.copy(self._problem._known), options)

        if self._visualizer:
            self._visualizer.draw(root.board)

        if self._problem.isGoal(root.board):  # We found the solution
            return root.board

        solution = self.backtrack(root)

        if solution is not None:
            return solution.board

        return None  # Time is out, return nothing

    def getSortParams(self, x, total):
        size = len(x[1])

        order = 0
        originalCordinate = self._problem.getRegionOrigin(x[0])
        originalRow = originalCordinate[0]
        originalCol = originalCordinate[1]

        if (originalCol == 0 or originalRow == 1):
            order = 1

        if (size == 0):
            return (0, order, self._problem.getRegionSize(x[0]))

        else:            
            return (-1 * size, order, self._problem.getRegionSize(x[0]))

    def orderRegion(self, state):

        keys = list(state.options.keys())
        total = self._problem.numRegions()
        remain = len(state.options)

        # return largest region for the first pick
        if total == remain:
            return keys[0]

        sort = sorted(state.options.items(), key = lambda x : self.getSortParams(x, total), reverse=True)

        return sort[0][0]

    def backtrack(self, state):

        if not self.timeRemaining():
            return None

        if self._problem.isGoal(state.board):  # We found the solution
            return state

        if self._visualizer:
            self._visualizer.draw(state.board, state.options)

        if (len(state.options) == 0):
            return None

        # Choose an region to fix

        regionId = self.orderRegion(state)
        regionOptions = state.options.pop(regionId)
        self._numExpansions += 1

        originalCordinate = self._problem.getRegionOrigin(regionId)
        originalRow = originalCordinate[0]
        originalCol = originalCordinate[1]

        # sort by descending order the manhattan distance b/w
        regionOptions = sorted(regionOptions, key = lambda x : -1 * (abs(x[0] - originalRow) + abs(x[1] - originalCol)), reverse=True)

        for rectangle in regionOptions:
            # Check if this choice is consistent with selections
            # that have already been made.  It is consistent if every
            # square has either the region id or -1 in it.
            consistent = numpy.all(numpy.logical_or(state.board == -1, state.board == regionId)[
                                   rectangle[0]:rectangle[0]+rectangle[2], rectangle[1]:rectangle[1]+rectangle[3]])

            if consistent:
                newState = copy.deepcopy(state)

                for row in range(rectangle[0], rectangle[0]+rectangle[2]):
                    for col in range(rectangle[1], rectangle[1]+rectangle[3]):
                        newState.board[row, col] = regionId

                self.infer(newState)

                if self._visualizer:
                    self._visualizer.draw(newState.board)

                solution = self.backtrack(newState)

                if solution is not None:
                    return solution

                self._backTracks += 1

        return None
