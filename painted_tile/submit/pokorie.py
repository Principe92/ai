
from itertools import permutations
import math
from typing import Dict, List, Set, Tuple
import os


class Literal():
    def __init__(self, input: str) -> None:
        self.__input = input
        self.__isgoal = False
        self.__isposition = False
        self.__isaction = False

        self.__literal: Tuple[str, int, int] = self._init()

    def __eq__(self, other) -> bool:
        if self.__str__() == str(other):
            return True
        else:
            return False

    def __ne__(self, other) -> bool:
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

    
    def canMove(self, goals: list, input_ls: list) -> Tuple[bool, str]:
        goalKeys = {}

        for goal in goals:
            goalliteral: Literal = goal
            goalt1 = goalliteral.formatT1()

            goalKeys[goalt1] = goal

        t2 = self.formatT2()

        return t2 not in goalKeys.keys()

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
        self.precondition_positive.add(literal)
        self.effect_positive.add(literal)

    def fillPaintAction(self) -> None:
        if 'Set' not in self.__action:
            return

        t1 = self.__literal.formatT1()
        t2 = self.__literal.formatT2()
        marker = self.__literal.getMarker().replace('Set', '')

        self.precondition_positive.add(Literal(f'At({t1})'))

        self.precondition_negative.add(Literal(f'Blue({t2})'))
        self.precondition_negative.add(Literal(f'Red({t2})'))
        # self.precondition_negative.add(Literal(f'At({t2})'))

        # self.precondition_negative.add(Literal(f'Blue({t1})'))
        # self.precondition_negative.add(Literal(f'Red({t1})'))

        notMarker = 'Blue' if marker == 'Red' else 'Red'

        self.effect_positive.add(Literal(f'{marker}({t2})'))
        # self.effect_negative.add(Literal(f'At({t2})'))
        # self.effect_negative.add(Literal(f'{notMarker}({t2})'))

    def fillMoveAction(self, input_ls: List[Literal], dimensions: Tuple[int, int]) -> None:
        if 'Move' not in self.__action:
            return

        t1 = self.__literal.formatT1()
        t2 = self.__literal.formatT2()

        self.precondition_positive.add(Literal(f'At({t1})'))

        self.precondition_negative.add(Literal(f'Blue({t2})'))
        self.precondition_negative.add(Literal(f'Red({t2})'))

        # self.precondition_negative.add(Literal(f'Red({t1})'))
        # self.precondition_negative.add(Literal(f'Blue({t1})'))

        self.effect_positive.add(Literal(f'At({t2})'))

        # self.effect_negative.add(Literal(f'At({t1})'))
        # self.effect_negative.add(Literal(f'Blue({t2})'))
        # self.effect_negative.add(Literal(f'Red({t2})'))

        _, width = dimensions

        # for x in input_ls:
        #     if x.isAdjacent():
        #         if x.formatT1() == t1:
        #             if x.formatT2() != t2:
        #                 # Add negative effect
        #                 self.effect_negative.add(
        #                     Literal(f'At({x.formatT2()})'))


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
        return f"Plan: {self._plan}"

    def append(self, action: Action):
        self._plan.append(action)

    def remove(self, action: Action):
        self._plan.remove(action)

    @property
    def plan(self):
        return self._plan


class Graph():
    def __init__(self) -> None:
        self.layers = 0
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


class GraphBuilder():
    def __init__(self, input: str) -> None:
        self.__pp = Problem(input)
        self._graph = Graph()

    @property
    def goals(self) -> Set[Literal]:
        return self.__pp.goals

    def hasSetAction(self, actions: Set[Action]) -> bool:
        res = []

        for action in actions:
            if 'Set' in action.toLiteral().getMarker():
                res.append(action)

        return res

    def create(self, maxLevels=10) -> Graph:
        self._graph.preconditions = {0: self.__pp.initialLevel}
        self._graph.layers = 1

        for i in range(1, maxLevels):
            self._graph = self.expand(self._graph)

            goal_set = self.__pp.goals
            index = self._graph.layers - 1
            precondition_list = self._graph.preconditions[index]
            precondition_mutex_list = self._graph.precondition_mutexes[index]
            has = goal_set.intersection(precondition_list)
            missing = goal_set.difference(has)
            sameaslast = self._graph.preconditions[index -
                                                   1] == precondition_list

            goal_found = False

            if goal_set.issubset(precondition_list):
                goal_found = True
                for goal_pair in list(permutations(goal_set, 2)):
                    if goal_pair in precondition_mutex_list:
                        goal_found = False
                        break

                if goal_found:
                    break

            # if not goal_found and index > 0 and sameaslast:
            elif index > 0 and sameaslast:
                self._graph.fixed_point = True
                break

        return self._graph

    def expand(self, graph: Graph) -> Graph:
        level = graph.layers

        if level <= 0:
            raise ValueError("Input Graph should not be empty")

        self.buildActions(graph)
        self.buildPreconditions(graph)
        self.buildActionsMutex(graph)
        self.buildPreconditionsMutex(graph)

        # update number of levels
        graph.layers = level + 1

        graph.fixed_point = graph.preconditions[level -
                                                1] == graph.preconditions[level]

        return graph

    def buildActions(self, graph: Graph) -> None:
        actions: List[Action] = []
        noActions: List[Action] = []
        level = graph.layers

        for action in self.__pp.actions:
            if self.__canApplyAction(action, graph.preconditions[level-1], graph.precondition_mutexes[level-1]):
                actions.append(action)

        for literal in graph.preconditions[level - 1]:
            noAction = Action(f'{literal}')
            noAction.fillPersistentAction(literal)
            noActions.append(noAction)

        actions += noActions

        graph.actions[level] = actions

    def buildPreconditions(self, graph: Graph) -> None:
        level = graph.layers
        actions: Set[Action] = graph.actions[level]

        precondition_list: Set[Literal] = set()

        for action in actions:
            for effect in action.effect_positive:
                precondition_list.add(effect)

        graph.preconditions[level] = precondition_list

    def buildActionsMutex(self, graph: Graph) -> None:
        level = graph.layers
        actions = graph.actions[level]

        action_mutex_list: List[Tuple[Action, Action]] = []

        for pair in list(permutations(actions, 2)):
            if self.__isActionPairMutex(pair, graph.precondition_mutexes[level - 1]):
                action_mutex_list.append(pair)

        graph.action_mutexes[level] = action_mutex_list

    def buildPreconditionsMutex(self, graph: Graph) -> None:
        level = graph.layers
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

    def __isPreconditionPairMutex(self, proposition_pair: Tuple[Literal, Literal], action_list: List[Action], action_mutex: List[Tuple[Action, Action]]) -> bool:
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

    def __canApplyAction(self, action: Action, preconditions: Set[Literal], preconditions_mutex: Set[Literal]) -> bool:
        if action.precondition_positive.issubset(preconditions) and \
                action.precondition_negative.isdisjoint(preconditions):
            applicable = True

            if preconditions_mutex is not None:
                for precondition in list(permutations(action.precondition_positive, 2)):
                    if precondition in preconditions_mutex:
                        applicable = False
                        break
        else:
            applicable = False

        return applicable

    def __isActionPairMutex(self, pair: Tuple[Action, Action], preconditions_mutex: Set[Literal]) -> bool:
        firstAction = pair[0]
        secondAction = pair[1]

        # two actions are dependent
        if firstAction.effect_negative.intersection(secondAction.precondition_positive.union(secondAction.effect_positive)) != set():
            return True

        if secondAction.effect_negative.intersection(firstAction.precondition_positive.union(firstAction.effect_positive)) != set():
            return True

        # their preconditions are mutex
        if preconditions_mutex is not None:
            for mutex in preconditions_mutex:
                first = mutex[0]
                second = mutex[1]
                if first in firstAction.precondition_positive and second in secondAction.precondition_positive:
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
            actions = sorted(plan.plan, reverse=True,
                             key=lambda x: x.toLiteral().getMarker())
            for action in actions:
                action_str = str(action)

                if action.toLiteral().isAction():
                    result = action_str if len(
                        result) == 0 else f'{result},{action_str}'

        return result

    @property
    def data(self):
        return self._layered_plan


class PlanBuilder():
    def __init__(self) -> None:
        self._layered_plan: LayeredPlan = LayeredPlan()
        self._mutex = {}

    def extract(self, graph: Graph, goals: set, layer: int):
        # return empty plan if at the base layer
        if layer == 0:
            return Plan()

        return self.search(graph, goals, Plan(), layer)

    def search(self, graph: Graph, goals: Set[Literal], plan: Plan, layer: int):

        # if we have resolved all the goals at this layer,
        # load its preconditions as the new goals and decrease the layer index
        if goals == set():
            new_goals = set()
            for action in plan.plan:
                for precondition in action.precondition_positive:
                    if 'Adj' not in precondition.getMarker():
                        new_goals.add(precondition)

            extracted_plan = self.extract(graph, new_goals, layer-1)
            if extracted_plan is None:
                return None
            else:
                self._layered_plan[layer-1] = extracted_plan
                self._layered_plan[layer] = plan
                return plan
        else:
            # select any goal
            goal = goals.pop()

            # compute resolvers
            resolvers : List[Action] = []
            possible_actions = graph.actions[layer]

            for action in possible_actions:
                if goal in action.effect_positive:

                    # if we already have actions for this goal,
                    # make sure it is mutually exlusive from the new action
                    if plan.plan:
                        mutex = False
                        for action2 in plan.plan:
                            if (action, action2) in graph.action_mutexes[layer]:
                                mutex = True
                                break

                        if not mutex:
                            resolvers.append(action)
                    else:
                        resolvers.append(action)

            
            # if we cannot find an action to resolve this goal
            # return no solution
            if not resolvers:
                return None

            # choose non-deterministically and backtrack if failed
            while resolvers:
                resolver = resolvers.pop()
                plan.append(resolver)

                # choose an action and use it to find a plan
                plan_result = self.search(graph, goals - resolver.effect_positive, plan, layer)

                if plan_result is not None:
                    return plan_result
                else:
                    plan.remove(resolver)
                    goals.add(goal)

            return None

    def plan(self, graph: Graph, goal: set, planning_graph: GraphBuilder):
        layer = graph.layers - 1

        # goals must be in the preconditions of the last layer
        # they are the effects of the last actions that yield the goals
        if not goal.issubset(graph.preconditions[layer]):
            return None

        plan = self.extract(graph, goal, layer)
        if plan:
            return self._layered_plan

        if graph.fixed_point:
            n = 0
            try:
                props_mutex = self._mutex[graph.layers - 1]
            except KeyError:
                props_mutex = None
            if props_mutex:
                n = len(props_mutex)
        else:
            n = 0

        while True:
            layer += 1
            graph = planning_graph.expand(graph)
            plan = self.extract(graph, goal, layer)
            if plan:
                return self._layered_plan
            elif graph.fixed_point:
                try:
                    props_mutex = self._mutex[graph.layers-1]
                except KeyError:
                    props_mutex = None

                if props_mutex:
                    if n == len(props_mutex):
                        # this means that it has stabilised
                        return None
                    else:
                        n = len(props_mutex)


class Problem():

    def __init__(self, input: str) -> None:
        self.__input = input

        self.__literals: List[Literal] = self.getInput()
        self.__dimensions = self.getDimensions(self.__literals)
        self.__goals = set(self.getGoalState(self.__literals))
        self.__initials = set(self.getInitialState(self.__literals))

        self.__actions = self.getActions()

    @property
    def goals(self) -> Set[Literal]:
        return self.__goals

    @property
    def actions(self) -> Set[Action]:
        return self.__actions

    @property
    def initialLevel(self) -> Set[Literal]:
        return self.__initials

    def getActions(self) -> Set[Action]:

        actions = set()

        for literal in self.__literals:
            if literal.isAdjacent():
                t1 = literal.formatT1()
                t2 = literal.formatT2()

                canBePainted, color = literal.canPaint(self.__goals, self.__literals)

                if canBePainted:
                    action = Action(f'Set{color}({t1},{t2})')
                    action.fillPaintAction()
                    actions.add(action)

                action = Action(f'Move({t1},{t2})')
                action.fillMoveAction(self.__literals, self.__dimensions)
                actions.add(action)


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
                break

        return start

    def getGoalState(self, input_ls: List[Literal]) -> List[Literal]:
        literals = []

        for input in input_ls:
            if input.isGoal():
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
        planning_graph = GraphBuilder(input_str)
        graph = planning_graph.create(10)

        goals = planning_graph.goals
        graph_planner = PlanBuilder()
        layered_plan = graph_planner.plan(graph, goals, planning_graph)
        print(layered_plan)


if __name__ == "__main__":
    main()
