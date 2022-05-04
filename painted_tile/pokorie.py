
import math
from turtle import position, width

class Plan():
    def __init__(self) -> None:
        pass

class Graph():
    def __init__(self) -> None:
        self.levels = 0
        self.act = {}
        self.act_mutexes = {}
        self.prop = {}
        self.prop_mutexes = {}

class Goal():
    def __init__(self) -> None:
        pass

class PopState():
    def __init__(self) -> None:
        self.preconditions = {};
        self.actions = {};
        self.effects = {};

class PopAlgorithm():

    def __init__(self, input) -> None:
        self.__input = input


    def get_input(self, input: str) -> list:
        input_ls = self.__input.split('),')
        return self.fix_input(input_ls)

    def fix_input(self, input_ls):
        res = []

        for input in input_ls:
            input += ')'
            res.append(input)

        return res

    def get_dimensions(self, input_ls):
        greatest = 0

        for input in input_ls:
            if 'Adj' in input:
                aa = input.split(',')
                a1 = int(aa[0].split('(')[1].replace('t', ''))
                a2 = int(aa[1].split(')')[0].replace('t', ''))

                gt = a1 if a1 > a2 else a1
                greatest = greatest if greatest > gt else gt
        
        print(greatest)
        val = int(math.sqrt(greatest + 1))
        return (val, val)


    def get_flaws(self, goal, dimensions, input_ls):
        _, width = dimensions
        flaws = []

        position = goal[1]

        for input in input_ls:
           key = f'Adj({position}'

           if key in input:
               flaws.append({
                   'precondition': input,
                   'effect': goal
               })
            
        return flaws



    def get_start(self, input_ls: list) -> list:
        start = [];

        for input in input_ls:
            if 'At' in input:
                start.append(input)
                break
        
        return start

    
    def build_link(self, input: str):
        a1 = input.split('(')
        a2 = a1[1].split(')')
        link = ('At', a2[0], a1[0])

        return link

    def get_goals(self, input_ls: list) -> list:
        goals = [];

        for input in input_ls:
            if 'Red' in input or 'Blue' in input:
                goals.append(self.build_link(input))            
    
        return goals

    # TODO:
    def get_steps(self, gvalues):

        steps = []

        for gvalue in gvalues:

            pass

        return steps

    def backtrack(self, plan, level):

        if level == 0:
            return plan

        
        new_g = []
        satisified = True

        for goal in plan['g']:

            steps = self.get_steps(goal)

            plan['plan'] += steps
            new_g += self.get_preconditions(steps)

        
        self.backtrack(plan, level-1)


    def extract(self, graph: Graph, goal: set, index:int):
        if index == 0:
            return Plan()

        return self.search(graph, goal, Plan(), index)

    def search(self, graph: Graph, goal: set, plan: Plan, index: int):
        pass

    def plan(self, graph:Graph, goal:set):

        index = graph.levels - 1

        plan = self.extract(graph, goal, index)
        if plan:
            return plan

        
        while True:
            index += 1
            plan = self.extract(graph, goal, index)

            if plan:
                return plan

    def run(self) -> str:

        input_ls = self.get_input()

        dimensions = self.get_dimensions(input_ls)

        goals = self.get_goals(input_ls)
        starts = self.get_start(input_ls)



        # plan = {
        #     'g': [],
        #     'plan': []
        # }

        # level = 1


        # for goal in goals:
        #     # flaws = self.get_flaws(goal, dimensions, input_ls)
        #     plan['g'] += [goal]

        
        # result = backtrack(plan, level)

        



            



        
        print(goals)
        print(starts)

        return input_ls[0]
        

# What are our constants: robot, position (t0, ..., t24)
# Initial state: At(tx). Has no preconditions. The same as effects
# Goal state: Red(tx) & Blue(tx) & Blue(tx). Has no effects. The same as preconditions
# How many actions can achieve the goal? SetRed(tx, ty), SetBlue(tx, ty)
# A Plan is made up of: 
#  1. A set of steps
#  2. A set of bindings
#  3. A set of orderings
#  4. A set of causal links 


def main():
    while True:
        pm = PopAlgorithm(input())
        print(pm.run())

if __name__ == "__main__":
    main()