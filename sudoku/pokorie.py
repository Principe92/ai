import json
from copy import deepcopy

def to_result(domain):
    print(json.dumps(domain, indent=4))
    dm_ls = [str(domain[dm_key][0]) for dm_key in [*domain]]
    #print(dm_ls)
    result = ''.join(dm_ls)
    print(result)

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
    i=0
    j=0
    k=0

    # generate initial contraints
    for index, num in enumerate(board):
        #if num != 0:
        i = int(index / 6)
        j = index % 6

        key = f'{i},{j}'

        num = int(num)
        domain_list = []

        if num != 0:
            domain_list.append(num)
        else:
            for h in range(1,7):
                if h != num:
                    domain_list.append(h)
                    
        domain[key] = domain_list
            

    first_unsolved = None

    for key in [*domain]:
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


    #check if csp is solved
    solved = True
    for l in [*domain]:
        if len(domain[l]) != 1:
               solved = False
               break


    if solved:
        return to_result(domain)

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

            #if prev_size == 1:
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

                
                        
                    

            #if value in domain[domain_key]:
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
            result = to_result(domain)
            return result
                    

    print(f'Solved: {solved}')
        
    



if __name__ == "__main__":
    input = "006010200500053000600103010030000000"

    CSP(input)