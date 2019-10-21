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
        return self.minmax(gameState, 0)[1]

    def terminalTest(self, gameState, counter):
        if counter == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return True

    def minmax(self, gameState, counter):
        if self.terminalTest(gameState, counter):
            return (self.evaluationFunction(gameState), None)
        if counter % gameState.getNumAgents() == 0:
            return self.maxValue(gameState, counter)
        else:
            return self.minValue(gameState, counter)

    def minValue(self, gameState, counter):
        v = (float('inf'), None)
        ghost = counter % gameState.getNumAgents()
        actions = gameState.getLegalActions(ghost)
        for action in actions:
            successor = gameState.generateSuccessor(ghost, action)
            successor_value = self.minmax(successor, counter+1)
            if successor_value[0] < v[0]:
               v = (successor_value[0], action)
        return v

    def maxValue(self, gameState, counter):
        v = (float('-inf'), None)
        actions = gameState.getLegalActions(0)
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            successor_value = self.minmax(successor, counter+1)
            if successor_value[0] > v[0]:
                v = (successor_value[0], action)
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        return self.minmax(gameState, 0, -float('inf'), float('inf'))[1]

    def terminalTest(self, gameState, counter):
        if counter == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return True

    def minmax(self, gameState, counter, alpha, beta):
        if self.terminalTest(gameState, counter):
            return (self.evaluationFunction(gameState), None)
        # if agent is pacman
        if counter % gameState.getNumAgents() == 0:
            return self.maxValue(gameState, counter, alpha, beta)
        # else ghost
        else:
            return self.minValue(gameState, counter, alpha, beta)

    def maxValue(self, gameState, counter, alpha, beta):
        # set to minnus infinity
        v = (float('-inf'), None)
        # get all legal actions
        actions = gameState.getLegalActions(0)
        for action in actions:
            # generate next node
            successor = gameState.generateSuccessor(0, action)
            # recursively do the same for next node
            successor_value = self.minmax(successor, counter+1, alpha, beta)
            if successor_value[0] > v[0]:
                v = (successor_value[0], action)
            if v[0] >  beta:
                return v
            alpha = max(alpha, v[0])
        return v

    def minValue(self, gameState, counter, alpha, beta):
        v = (float('inf'), None)
        ghost = counter % gameState.getNumAgents()
        actions = gameState.getLegalActions(ghost)
        for action in actions:
            successor = gameState.generateSuccessor(ghost, action)
            successor_value = self.minmax(successor, counter+1, alpha, beta)
            if successor_value[0] < v[0]:
               v = (successor_value[0], action)
            if v[0] < alpha:
                return v
            beta = min(beta, v[0])
        return v


