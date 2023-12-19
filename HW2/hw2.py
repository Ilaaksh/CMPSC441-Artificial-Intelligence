########################################################
#
# CMPSC 441: Homework 2
#
########################################################


student_name = 'Ilaaksh Mishra'
student_email = 'ijm5304@psu.edu'




########################################################
# Import
########################################################


from hw2_utils import *
from collections import deque


# Add your imports here if used





##########################################################
# 1. Uninformed Any-Path Search Algorithms
##########################################################
def depth_first_search(problem):
    node = Node(problem.init_state)
    edge = deque([node])
    visited = [problem.init_state]

    while(edge):
        node = edge.pop()
        if(problem.goal_test(node.state)):
            return node
        for n in node.expand(problem):
            if(n.state not in visited):
                edge.append(n)
                visited.append(n.state)

    return Node(None)


def breadth_first_search(problem):
    node = Node(problem.init_state)
    edge = deque([node])
    visited = [problem.init_state]

    while(edge):
        node = edge.popleft()
        if(problem.goal_test(node.state)):
            return node
        for n in node.expand(problem):
            if(n.state not in visited):
                edge.append(n)
                visited.append(n.state)

    return Node(None)


##########################################################
# 2. N-Queens Problem
##########################################################


class NQueensProblem(Problem):
    # This is a subclass of the class Problem.
    #   See hw2_utils.py for what each method does.
    # You need to orverride the following methods
    #   so that it works for NQueenProblem

    def __init__(self, n):
        super().__init__(tuple([-1] * n))
        self.n = n
    def actions(self, state):
        Column = state.index(-1)
        List = []

        for r in range(len(state)):
            if all(state[c] != r and abs(state[c] - r) != abs(Column - c) for c in range(Column)):
                List.append(r)

        return List
    def result(self, state, action):
        actionColumn = state.index(-1)
        returnTuple = list(state)

        returnTuple[actionColumn] = action

        return tuple(returnTuple)
    def goal_test(self, state):
        for row in range(self.n):
            if state[row] == -1:
                return False
            for row2 in range(row):
                if state[row2] == state[row] or abs(state[row2] - state[row]) == abs(row2 - row):
                    return False
        return True




##########################################################
# 3. Farmer's Problem
##########################################################


class FarmerProblem(Problem):
    # This is a subclass of the class Problem.
    #   See hw2_utils.py for what each method does.
    # You need to orverride the following methods
    #   so that it works for FarmerProblem

    def __init__(self, init_state, goal_state = (False,False,False,False)):
        super().__init__(init_state, goal_state)


    def actions(self, state):
        green = []

        if(state[1] != state[2] and state[2] != state[3]):
            green.append('F')

        if(state[0] == state[1] and state[2] != state[3]):
            green.append('FG')

        if(state[0] == state[2]):
            green.append('FC')

        if(state[0] == state[3] and state[1] != state[2]):
            green.append('FX')

        return green
    def result(self, state, action):
        solved = list(state)

        if action == 'F':
            solved[0] = not state[0]
        elif action == 'FC':
            solved[0] = not state[0]
            solved[2] = not state[2]
        elif action == 'FG':
            solved[0] = not state[0]
            solved[1] = not state[1]
        elif action == 'FX':
            solved[0] = not state[0]
            solved[3] = not state[3]

        return tuple(solved)

    def goal_test(self, state):
        return state == self.goal_state

##########################################################
# 4. Graph Problem
##########################################################


class GraphProblem(Problem):
    # This is a subclass of the class Problem.
    #   See hw2_utils.py for what each method does.
    # You need to orverride the following methods
    #   so that it works for GraphProblem

    def __init__(self, init_state, goal_state, graph):
        super().__init__(init_state, goal_state)
        self.graph = graph

    def actions(self, state):
        return list(self.graph.get(state).keys())

    def result(self, state, action):
        return action

    def goal_test(self, state):
        return state == self.goal_state