# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import sys
import copy
import pacman

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

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    You are not required to implement this, but you may find it useful for Q5.
    """
    queue = util.Queue()
    frontier = set()
    explored = set()
    startState = problem.getStartState()
    queue.push((startState, []))
    frontier.add(startState)
    while (not queue.isEmpty()):
        state, actions = queue.pop()
        frontier.remove(state)
        if problem.isGoalState(state):
            return actions
        explored.add(state)
        successors = problem.getSuccessors(state)
        for s in successors:
            s_state, s_action = s[0], s[1]
            if s_state not in explored and s_state not in frontier:
                queue.push((s_state, actions + [s_action]))
                frontier.add(s_state)
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth.

    Begin with a depth of 1 and increment depth by 1 at every step.
    """
    i=0
    while True:
        result = depthLimitedSearch(problem, i)
        if (result != None):
            return result
        i+=1


def depthLimitedSearch(problem, depth):
    stack = util.Stack()
    frontier = set()
    explored = set()
    startState = problem.getStartState()
    stack.push((startState, 0, []))
    frontier.add(startState)
    while (not stack.isEmpty()):
        state, d, actions = stack.pop()
        frontier.remove(state)
        if problem.isGoalState(state):
            return actions
        explored.add(state)
        if d < depth:
            successors = problem.getSuccessors(state)
            for s in successors:
                s_state, s_action = s[0], s[1]
                if s_state not in explored and s_state not in frontier:
                    stack.push((s_state, d + 1, actions + [s_action]))
                    frontier.add(s_state)
    return None

    

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    pqueue = util.PriorityQueue()
    frontier = set()
    explored = set()
    startState = problem.getStartState()
    pqueue.push((startState, [], 0), heuristic(startState, problem))
    frontier.add(startState)
    while (not pqueue.isEmpty()):
        state, actions, cost = pqueue.pop()
        if state in explored:
            continue
        frontier.remove(state)
        if problem.isGoalState(state):
            return actions
        explored.add(state)
        successors = problem.getSuccessors(state)
        for s in successors:
            s_state, s_action, s_cost = s[0], s[1], s[2]
            if s_state not in explored:
                pqueue.push((s_state, actions + [s_action], cost + s_cost), cost + s_cost + heuristic(s_state, problem))
                frontier.add(s_state)
    return None

# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
