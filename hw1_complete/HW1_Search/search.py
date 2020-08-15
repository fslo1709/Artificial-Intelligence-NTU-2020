# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def mySearch(problem, MyDS):
    """
    So I can use other DS in all the problems. Since all of them have pop and push, is easier to implement this way
    """
    EX_array = []		#Pacman hasn't moved yet
    MyDS.push([(problem.getStartState(), 'Stop', 0)])  #Push the initial state into the structure
    while not MyDS.isEmpty():
        step = MyDS.pop()  		#Start by popping the latest path in DS
        #temp = step[-1][0]		#Step[-1][0] gives us the last element of the DS, [0] means the tuple
        if problem.isGoalState(step[-1][0]):
            return [i[1] for i in step][1:]     #Just return all the steps if we've reached the goal (first step is Stop, so we start from index 1)
        if step[-1][0] not in EX_array:     #New step taken
            EX_array.append(step[-1][0])    #Add this step to the list of explored states
            for i in problem.getSuccessors(step[-1][0]):    #i being the iterator of all successors of the current position
                if i[0] not in EX_array:
                    SPath = step[:]  	#If it's not in the visited path, just copy the one where it came from
                    SPath.append(i)		#Just add the original guy to the path
                    MyDS.push(SPath)    #Push the path of this one into the structure to log it in
    #Only happens if above fails:
    return False

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    myStack = util.Stack()
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())
    return mySearch(problem, myStack)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    myQueue = util.Queue()
    return mySearch(problem, myQueue)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    #C gets the cost of the actions
    C = lambda path: problem.getCostOfActions([i[1] for i in path][1:])
    myPQueue = util.PriorityQueueWithFunction(C)
    return mySearch(problem, myPQueue)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    #C gets the cost of the actions, add heuristic to the path cost, almost the same as uCS
    C = lambda path: problem.getCostOfActions([i[1] for i in path][1:]) + heuristic(path[-1][0], problem)
    myPQueue = util.PriorityQueueWithFunction(C)
    return mySearch(problem, myPQueue)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
