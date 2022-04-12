import json
import math
from copy import deepcopy

def printResult(domain):

    if domain is None:
        print('No solution found')
        return ''

    domain_values = [str(domain[dm_key][0]) for dm_key in domain.keys()]
    result = ''.join(domain_values)
    # print(json.dumps(domain, indent=4))
    print(result)
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

            
            print('Backtracking')

    return None


def add_constraints(i, j, constraints, domain):

    for index in range(6):

        if index == i:
            continue

        cs_key = f'{i},{index}|{i},{j}'
        dm_key = f'{i},{index}'
        value_ls = domain[dm_key]

        if len(value_ls) != 1:
            constraints[cs_key] = value_ls[0]

    for index in range(6):

        if index == j:
            continue

        cs_key = f'{index},{j}|{i},{j}'
        dm_key = f'{index},{j}'
        value_ls = domain[dm_key]

        if len(value_ls) != 1:
            constraints[cs_key] = value_ls[0]


def CSP(board):

    constraints = {}
    domain = {}
    i = 0
    j = 0
    k = 0

    # generate initial contraints
    for index, num in enumerate(board):
        # if num != 0:
        i = int(index / 6)
        j = index % 6

        key = f'{i},{j}'

        num = int(num)
        domain_list = []

        if num != 0:
            domain_list.append(num)
        else:
            for h in range(1, 7):
                if h != num:
                    domain_list.append(h)

        domain[key] = domain_list

    first_unsolved = None

    for key in domain.keys():
        if len(domain[key]) != 1:
            first_unsolved = key
            break

    i = int(first_unsolved.split(',')[0])
    j = int(first_unsolved.split(',')[1])

    for index in range(6):

        if index == i:
            continue

        cs_key = f'{i},{j}|{i},{index}'
        dm_key = f'{i},{index}'
        value_ls = domain[dm_key]

        if len(value_ls) == 1:
            constraints[cs_key] = value_ls[0]

    for index in range(6):

        if index == j:
            continue

        cs_key = f'{i},{j}|{index},{j}'
        dm_key = f'{index},{j}'
        value_ls = domain[dm_key]

        if len(value_ls) == 1:
            constraints[cs_key] = value_ls[0]

    #print(json.dumps(constraints, indent=4))

    # check if csp is solved
    solved = True
    for l in domain.keys():
        if len(domain[l]) != 1:
            solved = False
            break

    if solved:
        return printResult(domain)

    orig_list = [b for b in domain[first_unsolved]]
    orig_domain = deepcopy(domain)
    orig_constraints = deepcopy(constraints)

    print(json.dumps(orig_constraints, indent=4))

    for item_ls in orig_list:
        domain = deepcopy(orig_domain)
        constraints = deepcopy(orig_constraints)
        domain[first_unsolved] = [item_ls]

        while len(constraints) != 0:

            key, value = constraints.popitem()

            domain_key = key.split('|')[0]
            cs_key = key.split('|')[1]
            i = int(domain_key.split(',')[0])
            j = int(domain_key.split(',')[1])

            prev_size = len(domain[domain_key])

            # if prev_size == 1:
            #    continue

            print(key)
            print(f'{domain[domain_key]}|{domain[cs_key]}')

            remove_ls = []
            for xi in domain[domain_key]:
                found = False
                for xj in domain[cs_key]:
                    if xi == xj:
                        found = True
                        break

                if found:
                    remove_ls.append(xi)

            for item in remove_ls:
                print(f'Removed {item} from {domain_key}')
                domain[domain_key].remove(item)

            # if value in domain[domain_key]:
            #    domain[domain_key].remove(value)

            print(domain[domain_key])
            print("--- end ---")

            if len(domain[domain_key]) == 0:
                print("Cannot solve CSP")
                break

            domain_has_changed = prev_size != len(domain[domain_key])

            if domain_has_changed:
                add_constraints(i, j, constraints, domain)

        if len(constraints) == 0:
            result = printResult(domain)
            return result

    print(f'Solved: {solved}')


def do(board):

    dimensions = getDimensions(board)
    domain = getDomain(board, dimensions)

    result = backtrack(domain, dimensions)
    printResult(result)


if __name__ == "__main__":
    input = "006010200500053000600103010030000000"

    # CSP(input)
    do(input)