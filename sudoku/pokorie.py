import json
import math
from copy import deepcopy

def printResult(domain):

    if domain is None:
        return ''

    domain_values = [str(domain[dm_key][0]) for dm_key in domain.keys()]
    result = ''.join(domain_values)
    return result


def isSolved(domain, dimensions):
    _, width = dimensions

    # check that all variable has a solution
    for key in domain.keys():
        if len(domain[key]) != 1:
            return False

    # check that the solution is right
    # check horizontally
    for index in range(width):
        values = list(set([domain[toDomainKey(index, j)][0] for j in range(width)]))
        if len(values) != width:
            return False

    # check vertically
    for index in range(width):
        values = list(set([domain[toDomainKey(i, index)][0] for i in range(width)]))
        if len(values) != width:
            return False

    return True


def discardSize(option, domain, dimensions, position):
    counter = 0

    _, width = dimensions
    x, y = toXY(position)

    for index in range(width):
        hKey = toDomainKey(x, index)
        vKey = toDomainKey(index, y)

        if hKey != position and len(domain[hKey]) != 1 and option in domain[hKey]:
            counter += 1

        if vKey != position and len(domain[vKey]) != 1 and option in domain[vKey]:
            counter += 1

    return counter


def getOptions(domain, dimensions, position):

    options = sorted(domain[position], key=lambda x: discardSize(
        x, domain, dimensions, position), reverse=False)

    return options

def getDomain(board, dimensions):

    _, width = dimensions
    domain = {}

    for index, value in enumerate(board):
        i = int(index / width)
        j = index % width

        key = toDomainKey(i, j)

        value = int(value)
        domain_list = None

        if value != 0:
            domain_list = [value]
        else:
            domain_list = [h for h in range(1, width+1)]

        domain[key] = domain_list

    return domain


def getDimensions(board):
    size = int(math.sqrt(len(board)))
    return size, size


def toXY(key):
    x = int(key.split(',')[0])
    y = int(key.split(',')[1])

    return x, y


def toDomainKey(x, y):
    return "%d,%d" % (x, y)


def getPosition(domain):
    options = []
    for key in domain.keys():
        if len(domain[key]) != 1:
            options.append((key, len(domain[key])))

    if len(options) == 0:
        return None

    position, _ = sorted(options, key=lambda x: x[1], reverse=False)[0]

    return position


def isConstraintMet(domain, option, dimensions, position):

    _, width = dimensions
    x, y = toXY(position)

    for index in range(width):
        hKey = toDomainKey(x, index)
        vKey = toDomainKey(index, y)

        violatesHorizontalConstraints = hKey != position and (
            len(domain[hKey]) == 1 and domain[hKey][0] == option
        )

        violatesVerticalConstraints = vKey != position and (
            len(domain[vKey]) == 1 and domain[vKey][0] == option
        )

        if violatesHorizontalConstraints or violatesVerticalConstraints:
            return False

    return True


def infer(domain, position, dimensions):

    _, width = dimensions
    x, y = toXY(position)
    option = domain[position][0]

    for index in range(width):
        hKey = toDomainKey(x, index)
        vKey = toDomainKey(index, y)

        if hKey != position and len(domain[hKey]) != 1 and option in domain[hKey]:
            domain[hKey].remove(option)

        if vKey != position and len(domain[vKey]) != 1 and option in domain[vKey]:
            domain[vKey].remove(option)


def backtrack(domain, dimensions):

    if isSolved(domain, dimensions):
        return domain

    position = getPosition(domain)

    if position is None:
        return None

    options = getOptions(domain, dimensions, position)

    for option in options:

        meetsAllContraints = isConstraintMet(
            domain, option, dimensions, position)

        if meetsAllContraints:
            newDomain = deepcopy(domain)
            newDomain[position] = [option]

            infer(newDomain, position, dimensions)

            solution = backtrack(newDomain, dimensions)

            if solution is not None:
                return solution

    return None


def do(board):
    dimensions = getDimensions(board)
    domain = getDomain(board, dimensions)

    result = backtrack(domain, dimensions)
    return printResult(result)


if __name__ == "__main__":
    while True:

        board = input()

        if isinstance(board, str):
            if board == "Done!":
                break

        if len(str(board)) < 5:
            continue

        result = do(str(board))
        print(int(result))