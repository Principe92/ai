
from itertools import permutations
import math
from typing import Dict, List, Set, Tuple


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
                if input.formatX() == self.formatX():
                    literals.append(input)

        return literals
    
    def toTuple(self) -> Tuple[str, int, int]:
        return self.__literal

    def isGoal(self) -> bool:
        return self.__isgoal

    def isPosition(self) -> bool:
        return self.__isposition

    def isAdjacent(self) -> bool:
        return not self.isGoal() and not self.isPosition()

    def isAction(self) -> bool:
        return self.__isaction

    def getY(self) -> int:
        return self.__literal[2]

    def formatY(self) -> int:
        y = str(self.getY())
        y = y if len(y) > 1 else f'0{y}'
        return f't{y}'

    def formatX(self) -> int:
        x = str(self.getX())
        x = x if len(x) > 1 else f'0{x}'
        return f't{x}'

    def getX(self) -> int:
        return self.__literal[1]

    def getMarker(self) -> str:
        return self.__literal[0]

    def canPaint(self, goals: list) -> Tuple[bool, str]:

        for goal in goals:
            goalliteral: Literal = goal

            x = self.formatX()
            goalX = goalliteral.formatX()

            if x == goalX:
                return True, goalliteral.getMarker()

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

    def fillPaintAction(self) -> None:
        if 'Set' not in self.__action:
            return

        t1 = self.__literal.formatX()
        t2 = self.__literal.formatY()
        marker = self.__literal.getMarker().replace('Set', '')

        self.precondition_positive.add(Literal(f'At({t1})'))
        # self.precondition_positive.add(Literal(f'Adj({t1},{t2})'))

        self.precondition_negative.add(Literal(f'Blue({t2})'))
        self.precondition_negative.add(Literal(f'Red({t2})'))

        self.effect_positive.add(Literal(f'{marker}({t2})'))

    def fillMoveAction(self, input_ls: List[Literal], dimensions: Tuple[int, int]) -> None:
        if 'Move' not in self.__action:
            return

        t1 = self.__literal.formatX()
        t2 = self.__literal.formatY()

        self.precondition_positive.add(Literal(f'At({t1})'))
        # self.precondition_positive.add(Literal(f'Adj({t1},{t2})'))

        self.precondition_negative.add(Literal(f'Blue({t2})'))
        self.precondition_negative.add(Literal(f'Red({t2})'))

        effect = Literal(f'At({t2})')
        self.effect_positive.add(effect)

        _, width = dimensions

        # Add negative effect
        for pos in range(width * width):
            if pos != self.__literal.getY():
                ty = str(pos)
                ty = ty if len(ty) > 1 else f'0{ty}'
                ty = f'At(t{ty})'
                self.effect_negative.add(Literal(ty))

        # for adj in effect.getAdjacents(input_ls):
        #     self.effect_positive.add(adj)


class Plan():
    def __init__(self):
        self._plan: List[Action] = []

    def __eq__(self, other):
        if self._plan == other.plan:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Plan object. {self._plan}"

    def append(self, action: Action):
        self._plan.append(action)

    def remove(self, action: Action):
        self._plan.remove(action)

    @property
    def plan(self):
        return self._plan


class Graph():
    def __init__(self) -> None:
        self.levels = 0
        self.actions: Dict[int, List[Action]] = {}
        self.action_mutexes: Dict[int, List[Tuple[Action, Action]]] = {}
        self.preconditions: Dict[int, Set[Literal]] = {}
        self.precondition_mutexes: Dict[int, Set[Literal]] = {}
        self.fixed_point = False

        self._init()

    def _init(self):
        self.actions = {0: None}
        self.action_mutexes = {0: None}
        self.precondition_mutexes = {0: None}


class PlanningGraph():
    def __init__(self, input: str) -> None:
        self.__pp = PlanningProblem(input)
        self._graph = Graph()

    @property
    def goals(self) -> Set[Literal]:
        return self.__pp.goals

    def create(self, maxLevels=10):
        self._graph.preconditions = {0: self.__pp.initials}
        self._graph.levels = 1

        for i in range(1, maxLevels):
            self._graph = self.expand(self._graph)

            goal_set = self.__pp.goals
            index = self._graph.levels - 1
            precondition_list = self._graph.preconditions[index]
            precondition_mutex_list = self._graph.precondition_mutexes[index]
            print(f'Trial #{i}: {precondition_list}')

            if goal_set.issubset(precondition_list):
                # goals in proposition list and
                # goals not in mutex proposition list
                goal_found = True
                for goal_pair in list(permutations(goal_set, 2)):
                    if goal_pair in precondition_mutex_list:
                        goal_found = False
                        break

                if goal_found:
                    break

            elif index > 0 and self._graph.preconditions[index-1] == precondition_list:
                self._graph.fixed_point = True
                break

        return self._graph

    def expand(self, graph: Graph) -> Graph:
        level = graph.levels

        if level <= 0:
            raise ValueError("Input Graph should not be empty")

        self.buildActions(graph)
        self.buildPreconditions(graph)
        self.buildActionsMutex(graph)
        self.buildPreconditionsMutex(graph)

        # update number of levels
        graph.levels = level + 1

        graph.fixed_point = graph.preconditions[level -
                                                1] == graph.preconditions[level]

        return graph

    def buildActions(self, graph: Graph) -> None:
        actions: List[Literal] = []
        level = graph.levels

        for action in self.__pp.actions:

            if self.__canApplyAction(action, graph.preconditions[level-1], graph.precondition_mutexes[level-1]):
                actions.append(action)

        graph.actions[level] = actions

    def buildPreconditions(self, graph: Graph) -> None:
        level = graph.levels
        action_list: Set[Action] = graph.actions[level]

        precondition_list: Set[Literal] = set()

        for action in action_list:
            for effect in action.effect_positive:
                precondition_list.add(effect)

        graph.preconditions[level] = precondition_list

    def buildActionsMutex(self, graph: Graph) -> None:
        level = graph.levels
        action_list = graph.actions[level]

        action_mutex_list: List[Tuple[Action, Action]] = []

        for pair in list(permutations(action_list, 2)):
            if self.__isActionPairMutex(pair, graph.precondition_mutexes[level - 1]):
                action_mutex_list.append(pair)

        graph.action_mutexes[level] = action_mutex_list

    def buildPreconditionsMutex(self, graph: Graph):
        level = graph.levels
        action_list = graph.actions[level]
        action_mutex_list = graph.action_mutexes[level]
        precondition_list = graph.preconditions[level]

        precondition_mutex_list = []

        for pair in list(permutations(precondition_list, 2)):
            if self.__isPreconditionPairMutex(pair, action_list, action_mutex_list):
                if pair not in precondition_mutex_list:
                    swapped = (pair[1], pair[0])
                    if swapped not in precondition_mutex_list:
                        precondition_mutex_list.append(pair)

        graph.precondition_mutexes[level] = precondition_mutex_list

    def __isPreconditionPairMutex(self, proposition_pair, action_list: List[Action], action_mutex):
        p = proposition_pair[0]
        q = proposition_pair[1]

        for action in action_list:
            if p in action.effect_positive and q in action.effect_positive:
                # (p, q) are not mutex if they both are produced by the
                # same action
                return False

        # every action that produces p
        actions_with_p = set()
        for action in action_list:
            if p in action.effect_positive:
                actions_with_p.add(action)

        # every action that produces q
        actions_with_q = set()
        for action in action_list:
            if q in action.effect_positive:
                actions_with_q.add(action)

        all_mutex = True
        for p_action in actions_with_p:
            for q_action in actions_with_q:
                if p_action == q_action:
                    return False
                if (p_action, q_action) not in action_mutex:
                    all_mutex = False
                    break
            if not all_mutex:
                break

        return all_mutex

    def __canApplyAction(self, action: Action, state: set, preconditions_mutex) -> bool:
        if action.precondition_positive.issubset(state) and \
                action.precondition_negative.isdisjoint(state):
            applicable = True

            if preconditions_mutex is not None:
                for precondition in list(permutations(action.precondition_positive, 2)):
                    if precondition in preconditions_mutex:
                        applicable = False
                        break
        else:
            applicable = False

        return applicable

    def __isActionPairMutex(self, pair: Tuple[Action, Action], preconditions_mutex) -> bool:
        a = pair[0]
        b = pair[1]

        # two actions are dependent
        if a.effect_negative.intersection(b.precondition_positive.union(b.effect_positive)) != set():
            return True

        if b.effect_negative.intersection(a.precondition_positive.union(a.effect_positive)) != set():
            return True

        # their preconditions are mutex
        if preconditions_mutex is not None:
            for mutex in preconditions_mutex:
                # (p, q)
                p = mutex[0]
                q = mutex[1]
                if p in a.precondition_positive and q in b.precondition_positive:
                    return True

        return False


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

        for plan in self._layered_plan.values():
            for action in plan.plan:
                result = str(action) if len(result) == 0 else f'{result},{str(action)}'

        return result

    @property
    def data(self):
        return self._layered_plan


class GraphPlanner():
    def __init__(self) -> None:
        self._layered_plan: LayeredPlan = LayeredPlan()
        self._mutex = {}

    def extract(self, graph: Graph, goals: set, index: int):
        if index == 0:
            return Plan()

        return self.search(graph, goals, Plan(), index)

    def search(self, graph: Graph, goals: Set[Literal], plan: Plan, index: int):
        if goals == set():
            new_goals = set()
            for action in plan.plan:
                for precondition in action.precondition_positive:
                    if 'Adj' not in precondition.getMarker():
                        new_goals.add(precondition)

            extracted_plan = self.extract(graph, new_goals, index-1)
            if extracted_plan is None:
                return None
            else:
                self._layered_plan[index-1] = extracted_plan
                self._layered_plan[index] = plan
                return plan
        else:
            # select any p in g
            precondition = goals.pop()

            # compute resolvers
            resolvers = []
            for action in graph.actions[index]:
                if precondition in action.effect_positive:
                    if plan.plan:
                        mutex = False
                        for action2 in plan.plan:
                            if (action, action2) in graph.action_mutexes[index]:
                                mutex = True
                                break

                        if not mutex:
                            resolvers.append(action)
                    else:
                        resolvers.append(action)

            # no resolvers
            if not resolvers:
                return None

            # choose non-deterministically and backtrack if failed
            while resolvers:
                resolver = resolvers.pop()
                plan.append(resolver)
                plan_result = self.search(
                    graph, goals - resolver.effect_positive, plan, index)
                if plan_result is not None:
                    return plan_result
                else:
                    plan.remove(resolver)
                    goals.add(precondition)
            return None

    def plan(self, graph: Graph, goal: set):
        index = graph.levels - 1

        if not goal.issubset(graph.preconditions[index]):
            return None

        plan = self.extract(graph, goal, index)
        if plan:
            return self._layered_plan

        if graph.fixed_point:
            n = 0
            try:
                props_mutex = self._mutex[graph.levels - 1]
            except KeyError:
                props_mutex = None
            if props_mutex:
                n = len(props_mutex)
        else:
            n = 0

        while True:
            index += 1
            graph = PlanningGraph.expand(graph)
            plan = self.extract(graph, goal, index)
            if plan:
                return self._layered_plan
            elif graph.fixed_point:
                try:
                    props_mutex = self._mutex[graph.levels-1]
                except KeyError:
                    props_mutex = None

                if props_mutex:
                    if n == len(props_mutex):
                        # this means that it has stabilised
                        return None
                    else:
                        n = len(props_mutex)


class PlanningProblem():

    def __init__(self, input: str) -> None:
        self.__input = input

        self.__literals: List[Literal] = self.get_input()

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
                t1 = literal.formatY()
                t2 = literal.formatX()

                canPaint, color = literal.canPaint(self.__goals)

                if canPaint:
                    # Add Set action
                    action = Action(f'Set{color}({t1},{t2})')
                    action.fillPaintAction()
                    actions.add(action)

                else:
                    # Add Move action
                    action = Action(f'Move({t1},{t2})')
                    action.fillMoveAction(self.__literals, self.__dimensions)
                    actions.add(action)

            # if literal.isPosition():


        return actions

    def get_input(self) -> List[Literal]:
        input_ls = self.__input.split('),')
        input_ls = self.fix_input(input_ls)
        return list(map(lambda x: Literal(x), input_ls))

    def fix_input(self, input_ls):
        res = []

        for input in input_ls:
            input += ')'
            res.append(input)

        return res

    def getDimensions(self, input_ls):
        greatest = 0

        for input in input_ls:
            if input.isAdjacent():
                x = input.getX()
                y = input.getY()

                gt = x if x > y else y
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


# What are our constants: robot, position (t0, ..., t24)
# Initial state: At(tx). Has no preconditions. The same as effects
# Goal state: Red(tx) & Blue(tx) & Blue(tx). Has no effects. The same as preconditions
# How many actions can achieve the goal? SetRed(tx, ty), SetBlue(tx, ty)
# A Plan is made up of:
#  1. A set of steps
#  2. A set of bindings
#  3. A set of orderings
#  4. A set of causal links


def main(arg):
    # while True:
    #     # pm = PlanningProblem(arg)
    #     pm = PopAlgorithm(input())
    #     print(pm.run())

    planning_graph = PlanningGraph(arg)
    graph = planning_graph.create(100)

    goals = planning_graph.goals
    graph_planner = GraphPlanner()
    layered_plan = graph_planner.plan(graph, goals)

    print(layered_plan)


if __name__ == "__main__":
    arg = 'Blue(t02),At(t03),Blue(t04),Blue(t17),Adj(t00,t05),Adj(t00,t01),Adj(t01,t06),Adj(t01,t00),Adj(t01,t02),Adj(t02,t07),Adj(t02,t01),Adj(t02,t03),Adj(t03,t08),Adj(t03,t02),Adj(t03,t04),Adj(t04,t09),Adj(t04,t03),Adj(t05,t00),Adj(t05,t10),Adj(t05,t06),Adj(t06,t01),Adj(t06,t11),Adj(t06,t05),Adj(t06,t07),Adj(t07,t02),Adj(t07,t12),Adj(t07,t06),Adj(t07,t08),Adj(t08,t03),Adj(t08,t13),Adj(t08,t07),Adj(t08,t09),Adj(t09,t04),Adj(t09,t14),Adj(t09,t08),Adj(t10,t05),Adj(t10,t15),Adj(t10,t11),Adj(t11,t06),Adj(t11,t16),Adj(t11,t10),Adj(t11,t12),Adj(t12,t07),Adj(t12,t17),Adj(t12,t11),Adj(t12,t13),Adj(t13,t08),Adj(t13,t18),Adj(t13,t12),Adj(t13,t14),Adj(t14,t09),Adj(t14,t19),Adj(t14,t13),Adj(t15,t10),Adj(t15,t20),Adj(t15,t16),Adj(t16,t11),Adj(t16,t21),Adj(t16,t15),Adj(t16,t17),Adj(t17,t12),Adj(t17,t22),Adj(t17,t16),Adj(t17,t18),Adj(t18,t13),Adj(t18,t23),Adj(t18,t17),Adj(t18,t19),Adj(t19,t14),Adj(t19,t24),Adj(t19,t18),Adj(t20,t15),Adj(t20,t21),Adj(t21,t16),Adj(t21,t20),Adj(t21,t22),Adj(t22,t17),Adj(t22,t21),Adj(t22,t23),Adj(t23,t18),Adj(t23,t22),Adj(t23,t24),Adj(t24,t19),Adj(t24,t23)'
    # arg = 'Blue(t02),At(t03),Blue(t04),Adj(t00,t05),Adj(t00,t01),Adj(t01,t06),Adj(t01,t00),Adj(t01,t02),Adj(t02,t07),Adj(t02,t01),Adj(t02,t03),Adj(t03,t08),Adj(t03,t02),Adj(t03,t04),Adj(t04,t09),Adj(t04,t03),Adj(t05,t00),Adj(t05,t10),Adj(t05,t06),Adj(t06,t01),Adj(t06,t11),Adj(t06,t05),Adj(t06,t07),Adj(t07,t02),Adj(t07,t12),Adj(t07,t06),Adj(t07,t08),Adj(t08,t03),Adj(t08,t13),Adj(t08,t07),Adj(t08,t09),Adj(t09,t04),Adj(t09,t14),Adj(t09,t08),Adj(t10,t05),Adj(t10,t15),Adj(t10,t11),Adj(t11,t06),Adj(t11,t16),Adj(t11,t10),Adj(t11,t12),Adj(t12,t07),Adj(t12,t17),Adj(t12,t11),Adj(t12,t13),Adj(t13,t08),Adj(t13,t18),Adj(t13,t12),Adj(t13,t14),Adj(t14,t09),Adj(t14,t19),Adj(t14,t13),Adj(t15,t10),Adj(t15,t20),Adj(t15,t16),Adj(t16,t11),Adj(t16,t21),Adj(t16,t15),Adj(t16,t17),Adj(t17,t12),Adj(t17,t22),Adj(t17,t16),Adj(t17,t18),Adj(t18,t13),Adj(t18,t23),Adj(t18,t17),Adj(t18,t19),Adj(t19,t14),Adj(t19,t24),Adj(t19,t18),Adj(t20,t15),Adj(t20,t21),Adj(t21,t16),Adj(t21,t20),Adj(t21,t22),Adj(t22,t17),Adj(t22,t21),Adj(t22,t23),Adj(t23,t18),Adj(t23,t22),Adj(t23,t24),Adj(t24,t19),Adj(t24,t23)'
    main(arg)
