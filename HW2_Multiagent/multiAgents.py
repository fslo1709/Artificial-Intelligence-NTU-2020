# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        curPos = currentGameState.getPacmanPosition()
        curDir = currentGameState.getPacmanState().getDirection()
        if action == Directions.STOP:
            return 0
        
        #See how far away the ghosts would be after moving to each direction
        ClosestGhost = min([manhattanDistance(newPos, S.getPosition()) for S in newGhostStates])
        #If you would bump into a ghost after moving, stop moving
        if (ClosestGhost <= 1):
            return 0
        #Else, if the score would increase:
        if successorGameState.getScore() > currentGameState.getScore():
            return 8
        #Now, check for the food distance if the score doesn't increase (not eating food)
        curNearest = min([manhattanDistance(curPos, f) for f in currentGameState.getFood().asList()])
        #Food distance for new Position
        templist = [manhattanDistance(newPos, f) for f in newFood.asList()]
        if not templist:
            newNearest = 0
        else:
            newNearest = min(templist)
        if newNearest == 0 or curNearest == 0:
            if newNearest < curNearest:
                return 4
        elif 1/newNearest > 1/curNearest:
            return 4
        #If all cases fail, just keep moving
        if action == curDir:
            return 2
        return 1

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def maxF(depth, status):
            NextLevel = status.getLegalActions(0)
            if self.depth == depth or not NextLevel:
                return self.evaluationFunction(status)
            return max(minF(depth+1, 1, status.generateSuccessor(0, move))for move in NextLevel) #Start min per each ghost
        
        def minF(depth, ID, status):
            NextLevel = status.getLegalActions(ID)
            
            if not NextLevel:
                return self.evaluationFunction(status)
            if status.getNumAgents() == ID + 1:
                return min(maxF(depth, status.generateSuccessor(ID, move)) for move in NextLevel)    #When all ghosts moved, we move PACMAN
            else:
                return min(minF(depth, ID + 1, status.generateSuccessor(ID, move)) for move in NextLevel) #Repeat per each ghost
        
        return max(gameState.getLegalActions(0), key=lambda move: minF(1, 1, gameState.generateSuccessor(0, move)))

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxF(a, b, depth, status):
            NextLevel = status.getLegalActions(0)
            if not NextLevel:
                return self.evaluationFunction(status)
            if depth == self.depth:
                return self.evaluationFunction(status)
            #follow the pseudocode
            v = -float('inf')
            if depth == 0:
                ret = NextLevel[0]
            for move in NextLevel:
                temp = status.generateSuccessor(0, move)
                comp = minF(a, b, depth + 1, 0+1, temp)
                if comp > v:
                    v = comp
                    if depth == 0:
                        ret = move
                if v > b:
                    return v
                a = max(a, v)
            if depth == 0:
                return ret
            else:
                return v
            
        def minF(a, b, depth, ID, status):
            NextLevel = status.getLegalActions(ID)
            if not NextLevel:
                return self.evaluationFunction(status)
            #follow the pseudocode
            v = float('inf')
            for move in NextLevel:
                temp = status.generateSuccessor(ID, move)
                if ID < status.getNumAgents() - 1:
                    comp = minF(a, b, depth, ID+1, temp)
                else:
                    comp = maxF(a, b, depth, temp)
                v = min(v, comp)
                if v < a:
                    return v
                b = min(b, v)
            return v
        
        return maxF(-float('inf'), float('inf'), 0, gameState)
            
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxF(status, depth):
            NextLevel = status.getLegalActions(0)
            if not NextLevel:
                return self.evaluationFunction(status)
            if depth == self.depth:
                return self.evaluationFunction(status)
            return max(expValue(status.generateSuccessor(0, move), 0 + 1, depth + 1) for move in NextLevel)
        def expValue(status, ID, depth):
            NextLevel = status.getLegalActions(ID)
            if not NextLevel:
                return self.evaluationFunction(status)
            count = 0
            for move in NextLevel:
                newMove = status.generateSuccessor(ID, move)
                temp = 0
                if ID < status.getNumAgents() - 1:
                    temp = expValue(newMove, ID + 1, depth) * (1.0 / len(NextLevel))
                else:
                    temp = maxF(newMove, depth) * (1.0 / len(NextLevel))
                count += temp
            return count
        return max(gameState.getLegalActions(), key=lambda action: expValue(gameState.generateSuccessor(0, action), 1, 1))
        

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

