include("FifteenPuzzle.jl")
include("pokorie.jl")

puzzles = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 11, 13, 14, 16, 12],
    [1, 3, 4, 16, 5, 2, 7, 8, 9, 6, 10, 12, 13, 14, 11, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 16, 11, 9, 13, 14, 12],
    [5, 1, 3, 4, 9, 2, 7, 8, 6, 11, 16, 12, 13, 10, 14, 15],
    [1, 2, 7, 3, 5, 10, 6, 4, 9, 12, 8, 16, 13, 14, 11, 15],
    [1, 2, 7, 3, 9, 5, 6, 4, 13, 10, 15, 8, 14, 16, 12, 11],
    [5, 1, 3, 4, 16, 2, 8, 12, 11, 6, 7, 15, 9, 13, 10, 14],
    [1, 3, 8, 4, 5, 16, 2, 7, 9, 10, 6, 12, 13, 14, 11, 15],
    [1, 6, 2, 3, 9, 5, 4, 7, 10, 16, 15, 11, 13, 8, 14, 12],
    [6, 7, 3, 4, 2, 1, 12, 16, 5, 9, 15, 8, 13, 14, 10, 11],
    [1, 2, 6, 8, 7, 4, 14, 3, 5, 15, 16, 11, 13, 10, 9, 12],
    [1, 7, 6, 8, 16, 2, 4, 10, 5, 3, 11, 9, 13, 14, 15, 12],
    [3, 4, 5, 11, 1, 10, 6, 15, 9, 14, 2, 8, 16, 13, 12, 7],
    [6, 10, 2, 7, 1, 12, 3, 16, 9, 14, 15, 4, 13, 5, 8, 11],
    [6, 3, 5, 2, 9, 14, 8, 4, 13, 1, 16, 15, 10, 11, 12, 7],
]

puzzleLen = length(puzzles)

expectedSolutionLengths = [3, 7, 8, 10, 11, 14, 17, 18, 21, 26, 28, 29, 33, 34, 36]

for index in 1:puzzleLen
    puzzle = State(puzzles[index])

    @time moves = pokorie.findSolution(puzzle)
    actual = length(moves)
    expected = expectedSolutionLengths[index]
    optimal = actual <= expected
    print("\n$index) Expected: $expected; Actual: $actual; Optimal: $optimal\n")
end