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
from game import Actions
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
        foodCount = newFood.count()
        # initialize the pac to ghost and food distances to the max distance in the layout for furthur comparasion
        minPacGhostDis =  newFood.height + newFood.width 
        minPacFoodDis = newFood.height * newFood.width
        safeTime = 0 # the safe time if pacman has eaten the ghost
        
        try:
            for ghostState in newGhostStates:
                pacGhostDis = util.manhattanDistance(newPos, ghostState.configuration.pos)
                # when the time left of scare ghost state is more than the distance between it and pac, refresh the chance
                if pacGhostDis < minPacGhostDis and ghostState.scaredTimer == 0:
                    minPacGhostDis = pacGhostDis
                # calculate the left time if we go to eat the ghost
                leftTime = max([0, ghostState.scaredTimer - pacGhostDis])
                if leftTime > safeTime:
                    safeTime = leftTime
            # if the distance between pac and ghost is greater than 1, we think it is safe
            newPacGhostDistance = min(minPacGhostDis, 1)

            # push foods into a priority queue order by the Manhattan distance
            manhattan_PriorityQueue = util.PriorityQueue()
            for y in range(newFood.height):
                for x in range(newFood.width):
                    # verify the cord whether it is a food, if true, push it
                    if newFood[x][y] == True:
                        manhattan_PriorityQueue.push((x, y), manhattanDistance(newPos, (x, y)))
            # pop the nearest food to get the Manhattan distance
            if(manhattan_PriorityQueue.count > 0):
                minPacFoodDis = util.manhattanDistance(newPos, manhattan_PriorityQueue.pop())
        except Exception as e:
            print(e)
        # evaluation value: add weight to factors
        # the most important is the safe distance, so we add more weight on the newPacGhostDistance
        evaluation = successorGameState.getScore() + safeTime + 5 * newPacGhostDistance + (1 / (minPacFoodDis)) / max(foodCount,1)
        return evaluation

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        action = self.recursiveCalculate(gameState, 0)['action']
        return action

    def recursiveCalculate(self, gameState, currentStep):
        scores = []
        agentCount = gameState.getNumAgents()
        dictActionScore = {}
        try:
            # when it comes to the final state or the last step of search depth
            if gameState.isWin() or gameState.isLose() or currentStep == self.depth * agentCount:
                dictActionScore['action'] = None
                dictActionScore['score'] = self.evaluationFunction(gameState)
                return dictActionScore
            elif currentStep < self.depth * agentCount:
                agentIndex = currentStep % agentCount
                legalActions = gameState.getLegalActions(agentIndex)
                for action in legalActions:
                        nextState = gameState.generateSuccessor(agentIndex, action)
                        nextStep = currentStep + 1
                        nextScore = self.recursiveCalculate(nextState, nextStep)['score']
                        scores.append(nextScore)
                # the ghosts choose their best actions to get min score and pacman needs the max score
                bestScore = max(scores) if agentIndex == 0 else min(scores)

                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = random.choice(bestIndices)
                dictActionScore['action'] = legalActions[chosenIndex]
                dictActionScore['score'] = bestScore
                return dictActionScore
        except Exception as e:
            print(e)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        action = self.recursiveCalculate(gameState, 0)['action']
        return action

    def recursiveCalculate(self, gameState, currentStep = 0, alpha = -float('inf'), beta = float('inf')):
        dictActionScore = {}
        agentCount = gameState.getNumAgents()
        try:
        # when it comes to the final state or the last step of search depth
            if gameState.isWin() or gameState.isLose() or currentStep == self.depth * agentCount:
                dictActionScore['action'] = None
                dictActionScore['score'] = self.evaluationFunction(gameState)
                return dictActionScore
            elif currentStep < self.depth * agentCount :
                agentIndex = currentStep % agentCount 
                legalActions = gameState.getLegalActions(agentIndex)
                maxScore = -float('inf')
                minScore = float('inf')
                for action in legalActions:
                        nextState = gameState.generateSuccessor(agentIndex, action)
                        nextScore = self.recursiveCalculate(nextState, currentStep + 1, alpha, beta)['score']
                        # for pacman, if find a greater score, refresh the maxScore and return this action
                        if agentIndex == 0 and nextScore >= maxScore:
                            maxScore = nextScore
                            bestAction = action
                            if nextScore > beta:
                                dictActionScore['action'] = bestAction
                                dictActionScore['score'] = maxScore
                                return dictActionScore
                            alpha = max(alpha, maxScore)
                        # for ghosts, if there is a smaller score, refresh the minScore and return this action
                        elif agentIndex > 0 and nextScore <= minScore:
                            minScore = nextScore
                            bestAction = action
                            if nextScore < alpha:
                                dictActionScore['action'] = bestAction
                                dictActionScore['score'] = minScore
                                return dictActionScore
                            beta = min(nextScore, minScore)
                if  agentIndex == 0:
                    dictActionScore['action'] = bestAction
                    dictActionScore['score'] = maxScore
                    return dictActionScore
                else:
                    dictActionScore['action'] = bestAction
                    dictActionScore['score'] = minScore
                    return dictActionScore
        except Exception as e:
            print(e)

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
        return self.recursiveCalculate(gameState, 0)['action']
    
    def recursiveCalculate(self, gameState, currentDepth):
        agentCount = gameState.getNumAgents()
        dictActionScore = {}
        scores = []
        try:
            if gameState.isWin() or gameState.isLose() or currentDepth == self.depth * agentCount:
                dictActionScore['action'] = None
                dictActionScore['score'] = self.evaluationFunction(gameState)
                return dictActionScore
            elif currentDepth < self.depth * agentCount :
                agentIndex = currentDepth % agentCount
                legalMoves = gameState.getLegalActions(agentIndex)
                for action in legalMoves:
                        nextState = gameState.generateSuccessor(agentIndex, action)
                        score = self.recursiveCalculate(nextState, currentDepth + 1)['score']
                        scores.append(score)
                if agentIndex == 0:
                    bestScore = max(scores)
                    bestIndices = [i for i in range(len(scores)) if scores[i] == bestScore]
                    selectIndex = random.choice(bestIndices)
                    dictActionScore['action'] = legalMoves[selectIndex]
                    dictActionScore['score'] = bestScore
                    return dictActionScore
                else:
                    dictActionScore['action'] = None
                    dictActionScore['score'] = sum(scores) / len(scores)
                    return dictActionScore
        except Exception as e:
            print(e)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    use the same evaluation function as the q1, we should account for these factors:
    1. newPacGhostDistance: the larger distance between pac and ghost, the more far is more safe, and the more socre can get
    2. minPacFoodDis * foodCount: the more food left on map and the longer distance between pac and food, the less score get
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    foodCount = newFood.count()
    # initialize the pac to ghost and food distances to the max distance in the layout for furthur comparasion
    minPacGhostDis =  newFood.height + newFood.width 
    minPacFoodDis = newFood.height * newFood.width
    safeTime = 0 # the safe time if pacman has eaten the ghost
    
    try:
        for ghostState in newGhostStates:
            pacGhostDis = util.manhattanDistance(newPos, ghostState.configuration.pos)
            # when the time left of scare ghost state is more than the distance between it and pac, refresh the chance
            if pacGhostDis < minPacGhostDis and ghostState.scaredTimer == 0:
                minPacGhostDis = pacGhostDis
            # calculate the left time if we go to eat the ghost
            leftTime = max([0, ghostState.scaredTimer - pacGhostDis])
            if leftTime > safeTime:
                safeTime = leftTime
        # if the distance between pac and ghost is greater than 1, we think it is safe
        # the more smaller safe distance we set, the pacman can action more brave
        newPacGhostDistance = min(minPacGhostDis, 1)

        # push foods into a priority queue order by the Manhattan distance
        manhattan_PriorityQueue = util.PriorityQueue()
        for y in range(newFood.height):
            for x in range(newFood.width):
                # verify the cord whether it is a food, if true, push it
                if newFood[x][y] == True:
                    manhattan_PriorityQueue.push((x, y), manhattanDistance(newPos, (x, y)))
        # pop the nearest food to get the Manhattan distance
        if(manhattan_PriorityQueue.count > 0):
            minPacFoodDis = util.manhattanDistance(newPos, manhattan_PriorityQueue.pop())
    except Exception as e:
        print(e)
    # evaluation value: add weight to factors
    # the most important is the safe distance, so we add more weight on the newPacGhostDistance
    evaluation = currentGameState.getScore() + safeTime + 5 * newPacGhostDistance + 1 / (minPacFoodDis * max(foodCount,1))
    return evaluation

# Abbreviation
better = betterEvaluationFunction
