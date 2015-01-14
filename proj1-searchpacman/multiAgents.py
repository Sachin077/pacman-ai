# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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
        pos = util.nearestPoint(currentGameState.getPacmanPosition())
        newPos = util.nearestPoint(newPos)
        ghostPositions = currentGameState.getGhostPositions()
        ghostNear = False
        minGhostDist = float('inf')
        # If any ghost is near, only minimize distance to nearest ghost.
        for gPos in ghostPositions:
          dist = util.manhattanDistance(pos, gPos)
          if dist < minGhostDist:
            minGhostDist = dist
          if dist < 3:
            ghostNear = True
        if ghostNear:
          newGhostPositions = successorGameState.getGhostPositions()
          newMinGhostDist = float('inf')
          for gPos in newGhostPositions:
            dist = util.manhattanDistance(newPos, gPos)
            if dist < newMinGhostDist:
              newMinGhostDist = dist
          return newMinGhostDist
        minFoodDist = float('inf')
        # Find nearest food.
        for p in newFood.asList():
          dist = util.manhattanDistance(p, newPos)
          if dist < minFoodDist:
            minFoodDist = dist
        # Ignore resulting minimum food distance if Pacman can eat food.
        if currentGameState.getNumFood() > successorGameState.getNumFood():
          minFoodDist = 0
        return -minFoodDist

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
      to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

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
      Your minimax agent (question 7)
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
        return self.minimax(gameState)

    def minimax(self, gameState):
        numAgents = gameState.getNumAgents()
        legalActions = gameState.getLegalActions(0)
        bestAction = None
        bestVal = float('-inf')
        for action in legalActions:
          successor = gameState.generateSuccessor(0, action)
          if numAgents == 1:
            val = self.pacmanMinimax(successor, self.depth - 1)
          else:
            val = self.ghostMinimax(successor, 1, self.depth)
          if val > bestVal:
            bestVal = val
            bestAction = action
        return bestAction

    def pacmanMinimax(self, gameState, depth):
        legalActions = gameState.getLegalActions(0)
        if depth == 0 or len(legalActions) == 0:
          return self.evaluationFunction(gameState)
        bestVal = float('-inf')
        numAgents = gameState.getNumAgents()
        for action in legalActions:
          successor = gameState.generateSuccessor(0, action)
          if numAgents == 1:
            val = self.pacmanMinimax(successor, depth - 1)
          else:
            val = self.ghostMinimax(successor, 1, depth)
          if val > bestVal:
            bestVal = val
        return bestVal

    def ghostMinimax(self, gameState, agentIndex, depth):
        legalActions = gameState.getLegalActions(agentIndex)
        if len(legalActions) == 0:
          return self.evaluationFunction(gameState)
        bestVal = float('inf')
        for action in legalActions:
          successor = gameState.generateSuccessor(agentIndex, action)
          if agentIndex == gameState.getNumAgents() - 1:
            val = self.pacmanMinimax(successor, depth - 1)
          else:
            val = self.ghostMinimax(successor, agentIndex + 1, depth)
          if val < bestVal:
            bestVal = val
        return bestVal


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 8)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimax(gameState)

    def expectimax(self, gameState):
        numAgents = gameState.getNumAgents()
        legalActions = gameState.getLegalActions(0)
        bestVal = float('-inf')
        bestActions = []
        for action in legalActions:
          successor = gameState.generateSuccessor(0, action)
          if numAgents == 1:
            val = self.pacmanExpectimax(successor, self.depth - 1)
          else:
            val = self.ghostExpectimax(successor, 1, self.depth)
          if val > bestVal:
            bestActions = []
            bestActions.append(action)
            bestVal = val
          elif val == bestVal:
            bestActions.append(action)
        return random.choice(bestActions)

    def pacmanExpectimax(self, gameState, depth):
        legalActions = gameState.getLegalActions(0)
        if depth == 0 or len(legalActions) == 0:
          return self.evaluationFunction(gameState)
        bestVal = float('-inf')
        numAgents = gameState.getNumAgents()
        for action in legalActions:
          successor = gameState.generateSuccessor(0, action)
          if numAgents == 1:
            val = self.pacmanExpectimax(successor, depth - 1)
          else:
            val = self.ghostExpectimax(successor, 1, depth)
          if val > bestVal:
            bestVal = val
        return bestVal

    def ghostExpectimax(self, gameState, agentIndex, depth):
        legalActions = gameState.getLegalActions(agentIndex)
        if len(legalActions) == 0:
          return self.evaluationFunction(gameState)
        accum = 0.0
        count = 0
        for action in legalActions:
          successor = gameState.generateSuccessor(agentIndex, action)
          if agentIndex == gameState.getNumAgents() - 1:
            val = self.pacmanExpectimax(successor, depth - 1)
          else:
            val = self.ghostExpectimax(successor, agentIndex + 1, depth)
          accum += val
          count += 1
        return accum/count

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 9).

      DESCRIPTION: Evaluation for Pacman states. It moves toward win states, and
      away from lose states. It also takes into account the distance to the closest
      food, the amount of food on the board, the distance to the closest non-scared
      ghost, the number of capsules on the board, and the score.  The resulting
      score is a linear combination of these factors.
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
      return float('inf')
    if currentGameState.isLose():
      return float('-inf')
    pos = util.nearestPoint(currentGameState.getPacmanPosition())
    score = currentGameState.getScore()
    numCapsules = len(currentGameState.getCapsules())
    food = currentGameState.getFood()
    numFood = currentGameState.getNumFood()
    ghostStates = currentGameState.getGhostStates()
    activeGhostStates = []
    # Determine distance to nearest active ghost.
    minGhostDist = float('inf')
    for ghostState in ghostStates:
      if ghostState.scaredTimer < 3:
        activeGhostStates.append(ghostState)
    for ghostState in activeGhostStates:
      dist = util.manhattanDistance(pos, ghostState.getPosition())
      if dist < minGhostDist:
        minGhostDist = dist
    # Find nearest food.
    minFoodDist = float('inf')
    for p in food.asList():
      dist = util.manhattanDistance(p, pos)
      if dist < minFoodDist:
        minFoodDist = dist
    return  -3*minFoodDist - 50*numFood + score - 5*numCapsules + minGhostDist

# Abbreviation
better = betterEvaluationFunction

