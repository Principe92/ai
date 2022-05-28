
from copy import deepcopy
from itertools import combinations, permutations
import math
from typing import Any, Deque, Dict, List, Set, Tuple
import os
from queue import PriorityQueue, Queue
from collections import deque

import sys
sys.setrecursionlimit(1500)

MAX_INT = 9999

class Literal():
    def __init__(self, input: str) -> None:
        self.__input = input
        self.__isgoal = False
        self.__isposition = False
        self.__isaction = False

        self.__literal: Tuple[str, int, int] = self._init()

    def __eq__(self, other):
        if self.__str__() == str(other):
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return self.__input

    def __str__(self) -> str:
        return self.__input

    def __hash__(self) -> int:
        return hash(self.__literal)

    def getAdjacents(self, input_ls: list) -> list:

        literals = []

        for input in input_ls:
            if input.isAdjacent():
                if input.formatT1() == self.formatT1():
                    literals.append(input)

        return literals

    def toTuple(self) -> Tuple[str, int, int]:
        return self.__literal

    def isAtTheEdge(self, dimension: Tuple[int, int]) -> bool:
        if not self.isAdjacent():
            return False

        _, width = dimension

        edges = [x for x in list(range(width))]  # top
        edges += [(width - 1)*width + x for x in list(range(width))]  # bottom
        edges += [width * x for x in list(range(width))]  # left
        edges += [width * (x+1) - 1 for x in list(range(width))]  # right

        edges = set(edges)

        t2 = self.getT2()

        return t2 in edges

    def isGoal(self) -> bool:
        return self.__isgoal

    def isPosition(self) -> bool:
        return self.__isposition

    def isAdjacent(self) -> bool:
        return not self.isGoal() and not self.isPosition()

    def isAction(self) -> bool:
        return self.__isaction

    def getT2(self) -> int:
        return self.__literal[2]

    def formatT2(self) -> int:
        y = str(self.getT2())
        y = y if len(y) > 1 else f'0{y}'
        return f't{y}'

    def formatT1(self) -> int:
        x = str(self.getT1())
        x = x if len(x) > 1 else f'0{x}'
        return f't{x}'

    def getT1(self) -> int:
        return self.__literal[1]

    def getMarker(self) -> str:
        return self.__literal[0]

    def canPaint(self, goals: list, input_ls: list) -> Tuple[bool, str]:

        goalKeys = {}

        for goal in goals:
            goalliteral: Literal = goal
            goalt1 = goalliteral.formatT1()

            goalKeys[goalt1] = goal

        t2 = self.formatT2()

        canPaint = t2 in goalKeys.keys()

        if canPaint:
            return canPaint, goalKeys[t2].getMarker()

        return False, None

    def __toInt(self, input: str) -> int:

        return int(input
                   .replace('(', '')
                   .replace(')', '')
                   .replace('Adj', '')
                   .replace('At', '')
                   .replace('Move', '')
                   .replace('Set', '')
                   .replace('Blue', '')
                   .replace('Red', '')
                   .replace('None', '')
                   .replace('t', '')
                   )

    def _init(self):
        if ',' in self.__input:
            left, right = tuple(self.__input.split(','))
            marker, _ = tuple(left.split('('))
            positionX = self.__toInt(left)
            positionY = self.__toInt(right)
            self.__isaction = 'Set' in marker or 'Move' in marker
            return marker, positionX, positionY

        else:
            self.__isposition = 'At' in self.__input
            self.__isgoal = not self.__isposition
            left, right = tuple(self.__input.split('('))
            positionX = self.__toInt(right)
            positionY = -1
            marker = left
            return marker, positionX, positionY

class Action():
    def __init__(self, action: str) -> None:
        self.__action: str = action
        self.precondition_positive: Set[Literal] = set()
        self.precondition_negative: Set[Literal] = set()
        self.effect_positive: Set[Literal] = set()
        self.effect_negative: Set[Literal] = set()
        self.__literal: Literal = Literal(action)

    def toLiteral(self) -> Literal:
        return self.__literal

    def __hash__(self) -> int:
        return hash(self.__literal.toTuple())

    def __repr__(self) -> str:
        return self.__literal.__repr__()

    def __str__(self) -> str:
        return self.__literal.__str__()

    def __eq__(self, other):
        if self.__str__() == str(other):
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def fillPersistentAction(self, literal: Literal) -> None:
        # if 'None' not in self.__action:
        #     return

        self.precondition_positive.add(literal)
        self.effect_positive.add(literal)

    def fillPaintAction(self) -> None:
        if 'Set' not in self.__action:
            return

        t1 = self.__literal.formatT1()
        t2 = self.__literal.formatT2()
        marker = self.__literal.getMarker().replace('Set', '')

        self.precondition_positive.add(Literal(f'At({t1})'))
        # self.precondition_positive.add(Literal(f'Adj({t1},{t2})'))

        self.precondition_negative.add(Literal(f'Blue({t2})'))
        self.precondition_negative.add(Literal(f'Red({t2})'))
        # self.precondition_negative.add(Literal(f'At({t2})'))

        # self.precondition_negative.add(Literal(f'Blue({t1})'))
        # self.precondition_negative.add(Literal(f'Red({t1})'))

        notMarker = 'Blue' if marker == 'Red' else 'Red'

        self.effect_positive.add(Literal(f'{marker}({t2})'))
        self.effect_negative.add(Literal(f'At({t2})'))
        # self.effect_negative.add(Literal(f'{notMarker}({t2})'))

    def fillMoveAction(self, input_ls: List[Literal], dimensions: Tuple[int, int]) -> None:
        if 'Move' not in self.__action:
            return

        t1 = self.__literal.formatT1()
        t2 = self.__literal.formatT2()

        self.precondition_positive.add(Literal(f'At({t1})'))
        # self.precondition_positive.add(Literal(f'Adj({t1},{t2})'))

        self.precondition_negative.add(Literal(f'Blue({t2})'))
        self.precondition_negative.add(Literal(f'Red({t2})'))

        # self.precondition_negative.add(Literal(f'Red({t1})'))
        # self.precondition_negative.add(Literal(f'Blue({t1})'))

        self.effect_positive.add(Literal(f'At({t2})'))

        self.effect_negative.add(Literal(f'At({t1})'))
        self.effect_negative.add(Literal(f'Blue({t2})'))
        self.effect_negative.add(Literal(f'Red({t2})'))

        _, width = dimensions

        for x in input_ls:
            if x.isAdjacent():
                if x.formatT1() == t1:
                    if x.formatT2() != t2:
                        # Add negative effect
                        # print(f'from: {t1} to: {t2} and not: {x.formatT2()}')
                        self.effect_negative.add(
                            Literal(f'At({x.formatT2()})'))

class Flaw():
    def __init__(self, literal: Literal) -> None:
        self.__literal = literal
        self.__link : Action = None
        self.__tail : Action = None
        self.__threat : Flaw = None
        self.__level: int = 0

    def __repr__(self) -> str:
        return f'flaw #{self.level}: {self.literal} | link: {self.link} | threat: {self.threat != None}'

    def __lt__(self, other):
        return self.level < other.level
    
    @property
    def literal(self) -> Literal:
        return self.__literal

    @property
    def level(self) -> int:
        return self.__level

    @property
    def link(self) -> Action:
        return self.__link

    @property
    def tail(self) -> Action:
        return self.__tail

    @property
    def threat(self) -> Any:
        return self.__threat

    
    def addLink(self, action: Action) -> None:
        self.__link = action
    
    def isOpen(self) -> bool:
        return self.__link == None

    
    def changeLevel(self, level: int) -> None:
        self.__level = level

    
    def setThreat(self, threat: Any) -> None:
        self.__threat = threat

    
    def isThreatened(self) -> bool:
        if self.isOpen():
            return False

        return self.__threat != None

class Step():
    def __init__(self, action:Action, flaw: Flaw, level: int) -> None:
        self.action = action
        self.flaw = flaw
        self.level = level
        self.flaw.changeLevel(level)
    
    def __repr__(self) -> str:
        return str(self.flaw)

    # def setThreat(self, threat: Flaw) -> None:
    #     self.flaw.setThreat(threat)

class Plan():
    def __init__(self):
        self.flaws: Set[Flaw] = set()
        self.steps_ls: Dict[str, Step] = {}

    def __repr__(self):
        result = ''

        steps = sorted(self.steps_ls.values(), key=lambda x: x.level)

        for step in steps:
            print(step)
            action =  step.action
            action_str = str(action)

            if action != None:
                result = action_str if len(
                    result) == 0 else f'{result},{action_str}'

        return result

    def hasStep(self, action: Action) -> bool:
        
        for s in self.steps_ls.keys():
            if s == str(action):
                return True

        return False

    def hasLiteral(self, literal: Literal) -> bool:
        
        for step in self.steps_ls.values():
            if step.flaw.literal == literal:
                return True

        return False

    def addStep(self, step: Step, isstart:bool = False) -> None:
        tag = None
        if isstart:
            tag = 'start'
        elif step.flaw.literal.isGoal():
            tag = f'{step.flaw.literal}'
        else:
            tag = str(step.action.toLiteral())

        self.steps_ls[tag] = step

class PlanningGraph():
    def __init__(self, input: str) -> None:
        self.__pp = PlanningProblem(input)
        self.__plan = Plan()

    @property
    def goals(self) -> Set[Literal]:
        return self.__pp.goals

    def hasSetAction(self, actions: Set[Action]) -> bool:
        res = []

        for action in actions:
            if 'Set' in action.toLiteral().getMarker():
                res.append(action)

        return res

    def create(self, maxLevels=10):
        start = Flaw(list(self.__pp.initials)[0])
        self.__plan.addStep(Step(Action(str(start.literal)), start, 0), True)

        for goal in self.goals:
            flaw = Flaw(goal)
            self.__plan.flaws.add(flaw)
            self.__plan.addStep(Step(Action(str(goal)), flaw, MAX_INT))


        self.__plan = self.expand(self.__plan, MAX_INT)

        return self.__plan

    
    def promote(self, plan: Plan, threatened_link: Flaw) -> None:

        if threatened_link.level == MAX_INT:
            return 

        threat : Flaw = threatened_link.threat
        newLevel = threatened_link.level - 2

        threatStep = plan.steps_ls[str(threat.link.toLiteral())]
        threatStep.level = newLevel
        threatStep.flaw.changeLevel(newLevel)
        plan.steps_ls[str(threat.link.toLiteral())] = threatStep

        threatenedLinkStep = plan.steps_ls[str(threatened_link.link.toLiteral())]
        threatenedLinkStep.flaw.setThreat(None)
        plan.steps_ls[str(threatened_link.link.toLiteral())] = threatenedLinkStep

        print(f'Promoted Threat: {threat} BEFORE LINK {threatened_link}')



    def demote(self, plan: Plan, threatened_link: Flaw) -> None:
        stepBefore = None
        steps = sorted(plan.steps_ls.values(), key=lambda x: x.level)

        print(plan.steps_ls.keys())

        for step in steps:
            if step.level < threatened_link.level:
                stepBefore = step
            else:
                break
        
        # if we are at the start level, we cannot demote
        if stepBefore.level == 0:
            return False

        newLevel = stepBefore.level - 2

        threatenedLinkStep = plan.steps_ls[str(threatened_link.link.toLiteral())]
        threatenedLinkStep.level = newLevel
        threatenedLinkStep.flaw.changeLevel(newLevel)
        threatenedLinkStep.flaw.setThreat(None)

        plan.steps_ls[str(threatened_link.link.toLiteral())] = threatenedLinkStep

        print(f'Demoted Link: {threatened_link} BEFORE STEP {stepBefore}')
        return True

    def getFlawsThreatened(self, plan:Plan, threat: Flaw) -> List[Step]:
        flaws = []

        for step in plan.steps_ls.values():

            if step.action == None or threat.link == None:
                continue

            if step.action == threat.link or not step.flaw.literal.isAction():
                continue

            if step.flaw.literal in threat.link.effect_negative:
                step.flaw.setThreat(threat)
                flaws.append(step.flaw)
        
        return flaws

    def expand(self, plan: Plan, level: int) -> Plan:

        if plan == None:
            return plan
        
        if len(plan.flaws) == 0:
            return plan

        
        flaw = plan.flaws.pop()

        if len(plan.flaws) == 0:
            print(f'\n\nFinal Level #{level} | Flaw: {flaw}')

        if flaw.isOpen():
            actions = self.buildActions(flaw)

            if len(actions) == 0:
                return None

            action = actions.pop()
            flaw.addLink(action)
            plan.addStep(Step(action, flaw, level-2))

            if not plan.hasStep(action):
                print(f'\nLevel #{level} | Flaw: {flaw} | Action: {action} | InSteps: {str(action) in plan.steps_ls.keys()}')

                for literal in action.precondition_positive:
                    # if not plan.hasLiteral(literal):
                    plan.flaws.add(Flaw(literal))


            flaws_threat = self.getFlawsThreatened(plan, flaw)
            # print(len(flaws_threat))
            for t in flaws_threat:
                plan.flaws.add(t)


        if flaw.isThreatened():
            hasThreat = True

            # while hasThreat:
            threat = flaw.threat
            if not self.demote(plan, flaw):
                self.promote(plan, flaw)

            # flaws_threat = self.getFlawsThreatened(plan, threat)
            # # print(len(flaws_threat))
            # for t in flaws_threat:
            #     plan.flaws.add(t)

        level -= 2
        return self.expand(plan, level)


    def buildActions(self, flaw: Flaw) -> Set[Action]:
        actions: List[Action] = []

        for action in self.__pp.actions:

            if self.__canApplyAction(action, flaw):
                actions.append(action)

        return set(actions)


    def __canApplyAction(self, action: Action, flaw: Flaw) -> bool:
        has = flaw.literal in action.effect_positive
        return has


class LayeredPlan(object):
    def __init__(self):
        self._layered_plan: Dict[int, Plan] = {}

    def __setitem__(self, key, value):
        self._layered_plan[key] = value

    def __getitem__(self, key):
        try:
            value = self._layered_plan[key]
        except KeyError:
            value = None
        return value

    def __repr__(self):
        result = ''

        print('')
        for plan in self._layered_plan.values():
            # actions = plan.plan
            actions = sorted(plan.plan, reverse=True,
                             key=lambda x: x.toLiteral().getMarker())
            # print(actions)
            for action in actions:
                action_str = str(action)

                if action.toLiteral().isAction():
                    result = action_str if len(
                        result) == 0 else f'{result},{action_str}'

        return result

    @property
    def data(self):
        return self._layered_plan

class PlanningProblem():

    def __init__(self, input: str) -> None:
        self.__input = input

        self.__literals: List[Literal] = self.getInput()

        self.__dimensions = self.getDimensions(self.__literals)

        self.__goals = set(self.getGoalState(self.__literals))
        # self.__goals = set(self.getInitialState(self.__literals))

        self.__initials = set(self.getInitialState(self.__literals))
        # self.__initials = set(self.getGoalState(self.__literals))

        self.__actions = self.getActions()

    @property
    def goals(self) -> Set[Literal]:
        return self.__goals

    @property
    def actions(self) -> Set[Action]:
        return self.__actions

    @property
    def initials(self) -> Set[Literal]:
        return self.__initials

    def getActions(self) -> Set[Action]:
        # TODO: Generate preconditions (positive and negative) & effects (position, negative)

        _, width = self.__dimensions

        actions = set()

        for literal in self.__literals:
            if literal.isAdjacent():
                t1 = literal.formatT1()
                t2 = literal.formatT2()

                canBePainted, color = literal.canPaint(self.__goals, self.__literals)

                if canBePainted:
                    # Add Set action
                    action = Action(f'Set{color}({t1},{t2})')
                    action.fillPaintAction()
                    actions.add(action)

                action = Action(f'Move({t1},{t2})')
                action.fillMoveAction(self.__literals, self.__dimensions)
                actions.add(action)

            # if literal.isPosition():
            #     action = Action(f'{literal}')
            #     action.fillPersistentAction(literal)
            #     actions.add(action)


        return actions

    def getInput(self) -> List[Literal]:
        input_ls = self.__input.split('),')
        input_ls = self.fixInput(input_ls)
        return list(map(lambda x: Literal(x), input_ls))

    def fixInput(self, input_ls: List[Literal]):
        res = []

        for input in input_ls:
            input += ')'
            res.append(input)

        return res

    def getDimensions(self, input_ls: List[Literal]):
        greatest = 0

        for input in input_ls:
            if input.isAdjacent():
                t1 = input.getT1()
                t2 = input.getT2()

                gt = t1 if t1 > t2 else t2
                greatest = greatest if greatest > gt else gt

        val = int(math.sqrt(greatest + 1))
        return (val, val)

    def getInitialState(self, input_ls: List[Literal]) -> List[Literal]:
        start: List[Literal] = []

        for input in input_ls:
            if input.isPosition():
                start += [input]
                # start += input.getAdjacents(input_ls)
                break

        return start

    def getGoalState(self, input_ls: List[Literal]) -> List[Literal]:
        literals = []

        for input in input_ls:
            if input.isGoal():
                # literals.append(self.build_link(input))
                literals.append(input)

        return literals


def save(input_str) -> None:
    dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    with open(os.path.join(dir, 'painted_tile/log.txt'), 'w+') as file:
        file.write(input_str)


def main():
    while True:
        input_str = input()

        if 'Adj' not in input_str:
            continue

        save(input_str)
        planning_graph = PlanningGraph(input_str)
        plan = planning_graph.create(10)

        print(plan)


if __name__ == "__main__":
    main()
