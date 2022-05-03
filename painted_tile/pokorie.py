
import math
from turtle import position, width

class PopState():
    def __init__(self) -> None:
        self.preconditions = {};
        self.actions = {};
        self.effects = {};

class PopAlgorithm():

    def __init__(self, input) -> None:
        self.__input = input


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

    def backtrack():
        pass

    
    def run(self) -> str:

        input_ls = self.__input.split('),')
        input_ls = self.fix_input(input_ls)

        dimensions = self.get_dimensions(input_ls)

        goals = self.get_goals(input_ls)
        starts = self.get_start(input_ls)


        for goal in goals:

            flaws = self.get_flaws(goal, dimensions, input_ls)

            flaw = flaws[0]

            



        
        print(goals)
        print(starts)

        return input_ls[0]
        



def main():
    while True:
        pm = PopAlgorithm(input())
        print(pm.run())

if __name__ == "__main__":
    main()