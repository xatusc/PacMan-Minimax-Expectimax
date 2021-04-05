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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
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
        This question is not included in project for CSCI360
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return childGameState.getScore()

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
    Your minimax agent (question 1)
    """
    def miniMax(self, gameState, curDepth, maxDepth, ghostNum, agentID):
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), None)
        elif curDepth == maxDepth:
            return (self.evaluationFunction(gameState), None)
        else:
            #Pacman
            if agentID == 0:
                max = -99999999
                maxAction = None
                #For each successor of the current state
                actions = gameState.getLegalActions(agentID)
                for a in actions:
                    sucVal = self.miniMax(gameState.getNextState(agentID, a), curDepth+1, maxDepth, ghostNum, 1)[0]
                    if sucVal > max:
                        max = sucVal
                        maxAction = a
                return (max, maxAction)
                
            #Ghost
            else:
                min = 99999999
                minAction = None
                actions = gameState.getLegalActions(agentID)
                #Last ghost
                if agentID == ghostNum:
                    nextAgentID = 0
                #Not last ghost
                else:
                    nextAgentID = agentID + 1
                for a in actions:
                        sucVal = self.miniMax(gameState.getNextState(agentID, a), curDepth+1, maxDepth, ghostNum, nextAgentID)[0]
                        if sucVal < min:
                            min = sucVal
                            minAction = a
                return (min, minAction)

    def getAction(self, gameState):
        num = gameState.getNumGhost()
        maxDepth = self.depth * (1 + num)
        return self.miniMax(gameState, 0, maxDepth, num, 0)[1]

        util.raiseNotDefined()
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumGhost():
        Returns the total number of ghosts in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """
    def miniMax(self, gameState, curDepth, maxDepth, ghostNum, agentID, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), None)
        elif curDepth == maxDepth:
            return (self.evaluationFunction(gameState), None)
        else:
            #Pacman
            if agentID == 0:
                maxVal = -99999999
                maxAction = None
                #For each successor of the current state
                actions = gameState.getLegalActions(agentID)
                for a in actions:
                    sucVal = self.miniMax(gameState.getNextState(agentID, a), curDepth+1, maxDepth, ghostNum, 1, alpha, beta)[0]
                    if sucVal > maxVal:
                        maxVal = sucVal
                        maxAction = a
                    if maxVal > beta: return (maxVal, maxAction)
                    alpha = max(alpha, maxVal)
                return (maxVal, maxAction)
                
            #Ghost
            else:
                minVal = 99999999
                minAction = None
                actions = gameState.getLegalActions(agentID)
                #Last ghost
                if agentID == ghostNum:
                    nextAgentID = 0
                #Not last ghost
                else:
                    nextAgentID = agentID + 1
                for a in actions:
                        sucVal = self.miniMax(gameState.getNextState(agentID, a), curDepth+1, maxDepth, ghostNum, nextAgentID, alpha, beta)[0]
                        if sucVal < minVal:
                            minVal = sucVal
                            minAction = a
                        if minVal < alpha: return (minVal, minAction)
                        beta = min(beta, minVal)
                return (minVal, minAction)

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        num = gameState.getNumGhost()
        maxDepth = self.depth * (1 + num)
        return self.miniMax(gameState, 0, maxDepth, num, 0, -99999999, 99999999)[1]
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """
    def expectiMax(self, gameState, curDepth, maxDepth, ghostNum, agentID):
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), None)
        elif curDepth == maxDepth:
            return (self.evaluationFunction(gameState), None)
        else:
            #Pacman
            if agentID == 0:
                maxVal = -99999999
                maxAction = None
                #For each successor of the current state
                actions = gameState.getLegalActions(agentID)
                for a in actions:
                    sucVal = self.expectiMax(gameState.getNextState(agentID, a), curDepth+1, maxDepth, ghostNum, 1)[0]
                    if sucVal > maxVal:
                        maxVal = sucVal
                        maxAction = a
                return (maxVal, maxAction)
                
            #Ghost
            #Expect
            else:
                expectVal = 0
                action = None
                actions = gameState.getLegalActions(agentID)
                p = 1/len(actions)
                #Last ghost
                if agentID == ghostNum:
                    nextAgentID = 0
                #Not last ghost
                else:
                    nextAgentID = agentID + 1
                for a in actions:
                        expectVal += p * self.expectiMax(gameState.getNextState(agentID, a), curDepth+1, maxDepth, ghostNum, nextAgentID)[0]
                return (expectVal, action)

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        num = gameState.getNumGhost()
        maxDepth = self.depth * (1 + num)
        return self.expectiMax(gameState, 0, maxDepth, num, 0)[1]
        util.raiseNotDefined()



def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 4).

    DESCRIPTION: Combining win/lose/neutral, pellets left, distance to closest pellet, distance to closest ghosts (which is weighted depending on the ghost scared time)
    """
    "*** YOUR CODE HERE ***"
    
    currentPosition = currentGameState.getPacmanPosition()

    #Getting win lose score
    score = 0
    if currentGameState.isWin(): score = 999999
    elif currentGameState.isLose(): score = -999999

    #Getting number of food left
    foodLeft = currentGameState.getNumFood()
    foodWeight = 100000
    if foodLeft == 0:
        foodValue = 100
    else:
        foodValue = foodWeight / foodLeft

    #Getting the closest food distance
    #iterate through the grid
    grid = currentGameState.getFood()
    rowNum = grid.height
    colNum = grid.width
    foodList = [(x, y) for x in range(colNum) for y in range(rowNum) if grid[x][y] == True ]
    #Calculating shortest distance
    closestFoodDistance = 99999999
    for food in foodList:
        if manhattanDistance(food, currentPosition) < closestFoodDistance: closestFoodDistance = manhattanDistance(food, currentPosition)
    closestFoodDistanceWeight = 10
    closestFoodDistanceValue = 0
    if closestFoodDistance != 0:
        closestFoodDistanceValue = closestFoodDistanceWeight / closestFoodDistance

    #Getting distance to closest capsule
    capsules = currentGameState.getCapsules()
    remainCapsuleWeight = 10000
    remainCapsuleValue = 0
    closestCapsule = 0
    #If more capsules left
    if capsules:
        #More capsule left, lower score
        remainCapsuleValue -= remainCapsuleWeight * len(capsules)
        closestCapsule = 99999999
        for capsule in capsules:
            if (manhattanDistance(currentPosition, capsule) < closestCapsule):
                closestCapsule = manhattanDistance(currentPosition, capsule)
    #Converting capsule distance to value
    capsuleValue = 1
    capsuleWeight = 100
  
    if closestCapsule == 0:
        capsuleValue *= capsuleWeight
    else:
        capsuleValue = capsuleWeight / closestCapsule 

    #Getting ghosts proximity
    ghostPositions = currentGameState.getGhostPositions()
    manDistances = [manhattanDistance(currentPosition, ghostPosition) for ghostPosition in ghostPositions]

    #Getting ghost scared time (controlls the weight of ghost proximity)
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    #Converting ghost distance to value
    scaredWeight = 0.6
    distanceValues = []
    for (manDistance, scaredTime) in zip(manDistances, scaredTimes):
        if scaredTime != 0:
            distanceValues.append(manDistance * scaredWeight / scaredTime)
        else: distanceValues.append(manDistance)
    distanceValue = sum(distanceValues)

    return score + foodValue + capsuleValue + distanceValue + remainCapsuleValue + closestFoodDistanceValue

    util.raiseNotDefined()



# Abbreviation
better = betterEvaluationFunction
