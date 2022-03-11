"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

################################
### I did write something in ###
###    bfs in search.py .    ###
###     Plz look at it.      ###
###    Regards, Lian Huan    ###
################################

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    ### If someone is reading this :)
    ### My English is really poor :) Thanks to PyCharm :)
    ### My Python skill is poor, too :) This work cost me over 30 hours in this week.
    ### Using the form of (import from) is ok, but I would like to import the whole py file.
    ### I do believe using some similar variable names as teacher in class is not sort of cheating :)
    ### I do refer some other student's idea, e.g. I cannot get 5/4 in Q7, which I can't now, either,
    ### but I do not use their codes.
    ### Indeed there are some variables redundant, e.g. in Q8_3, but I did those just for better understanding.
    ### The First two function will be hardly any notes(since not that hard)

    ### Notes in search.py: Only in this part the notes are concentrated.
    ### Notes for myself: Using Stack you have to search the new added nodes, then deep first.
    ### Notes for myself: Using Queue you will search the original node, then wide first.
    ### Notes for myself: Using Priority Queue you can save a priority, but the cost function is additive, so push
    ### three items in the queue.
    ### Notes for myself: h(n) will calculate the priority, while g(n) also, but h(n) is not additive, so
    ### g(n) and g(n)+h(n) should be placed separately.

    frontier = util.Stack()
    passed = []
    frontier.push((problem.getStartState(),[]))

    while not frontier.isEmpty():
        node, solution = frontier.pop()
        if problem.isGoalState(node):
            return solution
        if node not in passed:
            passed.append(node)
            nodeSuccessors = problem.getSuccessors(node)
        for location, direction, costFun in nodeSuccessors:
            if location not in passed:
                frontier.push((location, solution + [direction]))

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    frontier = util.Queue()
    passed = []
    frontier.push((problem.getStartState(), []))

    while not frontier.isEmpty():
        node, solution = frontier.pop()
        ### Unhashable type existed so cannot use nextsteps = node
        if problem.isGoalState(node):
            return solution
        if node not in passed:
            passed.append(node)
            nodeSuccessors = problem.getSuccessors(node)
        for location, direction, costFun in nodeSuccessors:
            if location not in passed:
                frontier.push((location, solution + [direction]))



    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    nodeStart = problem.getStartState()
    passed = []     ### For Graph Search
    frontier = util.PriorityQueue()
    frontier.push((nodeStart,[],0),0)

    while not frontier.isEmpty():
        node, solution, costFun = frontier.pop()
        if problem.isGoalState(node):
            return solution
        if node not in passed:
            passed.append(node)
            nodeSuccessors = problem.getSuccessors(node)
            for SuccessorPoints in nodeSuccessors:
                position = SuccessorPoints[0]
                if position not in passed:
                    direction = SuccessorPoints[1]
                    gCostFun = SuccessorPoints[2] + costFun
                    frontier.push((position, solution + [direction], gCostFun), gCostFun)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    nodeStart = problem.getStartState()
    passed = []     ### For Graph Search
    frontier = util.PriorityQueue()
    frontier.push((nodeStart, [], 0), 0)
    ### Set to nullHeuristic is unwise.
    while not frontier.isEmpty():
        node, solution, costFun = frontier.pop()
        if problem.isGoalState(node):
            break
        if node not in passed:
            passed.append(node)
            nodeSuccessors = problem.getSuccessors(node)
            for SuccessorPoints in nodeSuccessors:
                position = SuccessorPoints[0]
                if position not in passed:
                    direction = SuccessorPoints[1]
                    gCostFun = costFun + SuccessorPoints[2]
                    frontier.push((position, solution + [direction], gCostFun), gCostFun + heuristic(position, problem))
    return solution
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
