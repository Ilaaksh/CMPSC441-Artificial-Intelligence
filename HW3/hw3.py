########################################################
#
# CMPSC 441: Homework 3
#
########################################################


student_name = 'Ilaaksh Mishra'
student_email = 'ijm5304@psu.edu'



########################################################
# Import
########################################################

from hw3_utils import *
from collections import deque
import math
# Add your imports here if used






##########################################################
# 1. Best-First, Uniform-Cost, A-Star Search Algorithms
##########################################################


def best_first_search(problem):
    node = Node(problem.init_state, heuristic=problem.h(problem.init_state))
    frontier = deque([node])         # queue: popleft/append-sorted
    explored = [problem.init_state]  # used as "visited"

    while(frontier):
        frontier = deque(sorted(frontier, key = lambda n: n.heuristic))
        node = frontier.popleft()
        if(problem.goal_test(node.state)):
            return node
        for n in node.expand(problem):
            if n.state not in explored:
                frontier.append(n)
                explored.append(n.state)
    return Node(None)




def uniform_cost_search(problem):
    node = Node(problem.init_state)
    frontier = deque([node])  # queue: popleft/append-sorted
    explored = set()  # used as "expanded" (not "visited")

    while frontier:
        node = frontier.popleft()

        if problem.goal_test(node.state):
            return node

        explored.add(node.state)

        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            child_node = Node(child_state, parent=node, action=action, path_cost=node.path_cost + 1)

            if child_state not in explored and child_state not in [n.state for n in frontier]:
                frontier.append(child_node)

    return None




def a_star_search(problem):
    node = Node(problem.init_state, heuristic=problem.h(problem.init_state))
    frontier = deque([node])
    explored = set()

    while frontier:
        node = frontier.popleft()

        if problem.goal_test(node.state):
            return node

        explored.add(node.state)

        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            child_node = Node(child_state, parent=node, action=action, path_cost=node.path_cost + 1, heuristic=problem.h(child_state))

            if child_state not in explored and child_state not in [n.state for n in frontier]:
                frontier.append(child_node)

    return None




##########################################################
# 2. N-Queens Problem
##########################################################


class NQueensProblem(Problem):
    def __init__(self, n):
        super().__init__(tuple([-1] * n))
        self.n = n

    def actions(self, state):
        if state[-1] != -1:  # if all columns are filled
            return []  # then no valid actions exist

        valid_actions = list(range(self.n))
        col = state.index(-1)  # index of leftmost unfilled column
        for row in range(self.n):
            for c, r in enumerate(state[:col]):
                if self.conflict(row, col, r, c) and row in valid_actions:
                    valid_actions.remove(row)

        return valid_actions

    def result(self, state, action):
        col = state.index(-1)  # leftmost empty column
        new = list(state[:])
        new[col] = action  # queen's location on that column
        return tuple(new)

    def goal_test(self, state):
        if state[-1] == -1:  # if there is an empty column
            return False  # then the state is not a goal state

        for c1, r1 in enumerate(state):
            for c2, r2 in enumerate(state):
                if (r1, c1) != (r2, c2) and self.conflict(r1, c1, r2, c2):
                    return False
        return True

    def conflict(self, row1, col1, row2, col2):
        return row1 == row2 or col1 == col2 or abs(row1 - row2) == abs(col1 - col2)

    def g(self, cost, from_state, action, to_state):
        return cost + 1

    def h(self, state):
        """
        Returns the heuristic value for the given state.
        Use the total number of conflicts in the given
        state as a heuristic value for the state.
        """
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.conflict(state[i], i, state[j], j):
                    conflicts += 1
        return conflicts


##########################################################
# 3. Graph Problem
##########################################################



class GraphProblem(Problem):

    def __init__(self, init_state, goal_state, graph):
        super().__init__(init_state, goal_state)
        self.graph = graph

    def actions(self, state):
        return list(self.graph.get(state).keys())

    def result(self, state, action):
        return action

    def goal_test(self, state):
        return state == self.goal_state

    def g(self, cost, from_state, action, to_state):
        """
        Returns the path cost from the root to to_state.
        Note that the path cost from the root to from_state
        is the given cost, and the given action taken at from_state
        will lead you to to_state with the cost associated with
        the action.
        """
        return cost + self.graph.get(from_state).get(to_state)


    def h(self, state):
        """
        Returns the heuristic value for the given state. Heuristic
        value of the state is calculated as follows:
        1. if an attribute called 'heuristics' exists:
           - heuristics must be a dictionary of states as keys
             and corresponding heuristic values as values
           - so, return the heuristic value for the given state
        2. else if an attribute called 'locations' exists:
           - locations must be a dictionary of states as keys
             and corresponding GPS coordinates (x, y) as values
           - so, calculate and return the straight-line distance
             (or Euclidean norm) from the given state to the goal
             state
        3. else
           - cannot find nor calculate heuristic value for the given state
           - so, just return a large value (i.e., infinity)
        """
        if hasattr(self.graph, 'heuristics'):
            return self.heuristics.get(state, float('inf'))
        elif hasattr(self.graph, 'locations'):
            frloc = self.graph.locations.get(state)
            tloc = self.graph.locations.get(self.goal_state)
            if frloc and tloc:
                return math.sqrt((tloc[0] - frloc[0]) ** 2 + (tloc[1] - frloc[1]) ** 2)
        return float('inf')

    def __str__(self):
        return f"GraphProblem - Initial State: {self.initial_state}, Goal State: {self.goal_state}"





##########################################################
# 4. Eight Puzzle
##########################################################


class EightPuzzle(Problem):
    def __init__(self, init_state, goal_state=(1,2,3,4,5,6,7,8,0)):
        self.goal_state = goal_state
        super().__init__(init_state)

    def actions(self, state):
        actions = []
        blank_index = state.index(0)

        if blank_index // 3 > 0:
            actions.append("UP")
        if blank_index // 3 < 2:
            actions.append("DOWN")
        if blank_index % 3 > 0:
            actions.append("LEFT")
        if blank_index % 3 < 2:
            actions.append("RIGHT")

        return actions

    def result(self, state, action):
        state = list(state)
        blank_index = state.index(0)

        if action == "UP":
            state[blank_index], state[blank_index - 3] = state[blank_index - 3], state[blank_index]
        elif action == "DOWN":
            state[blank_index], state[blank_index + 3] = state[blank_index + 3], state[blank_index]
        elif action == "LEFT":
            state[blank_index], state[blank_index - 1] = state[blank_index - 1], state[blank_index]
        elif action == "RIGHT":
            state[blank_index], state[blank_index + 1] = state[blank_index + 1], state[blank_index]

        return tuple(state)


    def goal_test(self, state):
        return state == self.goal_state
        pass


    def g(self, cost, from_state, action, to_state):
        """
        Return path cost from root to to_state via from_state.
        The path from root to from_state costs the given cost
        and the action that leads from from_state to to_state
        costs 1.
        """
        return cost + 1


    def h(self, state):
        """
        Returns the heuristic value for the given state.
        Use the sum of the Manhattan distances of misplaced
        tiles to their final positions.
        """
        misplaced = 0
        for i in range(len(state)):
            if state[i] != 0 and state[i] != self.goal_state[i]:
                goal_index = self.goal_state.index(state[i])
                row_diff = abs(i // 3 - goal_index // 3)
                col_diff = abs(i % 3 - goal_index % 3)
                misplaced += row_diff + col_diff
        return misplaced


