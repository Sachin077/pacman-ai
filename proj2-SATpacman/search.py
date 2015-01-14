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
import logic
import game

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

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostSearchProblem)
        """
        util.raiseNotDefined()

    def terminalTest(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionSearchProblem
        """
        util.raiseNotDefined()

    def result(self, state, action):
        """
        Given a state and an action, returns resulting state and step cost, which is
        the incremental cost of moving to that successor.
        Returns (next_state, cost)
        """
        util.raiseNotDefined()

    def actions(self, state):
        """
        Given a state, returns available actions.
        Returns a list of actions
        """        
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

    def getWidth(self):
        """
        Returns the width of the playable grid (does not include the external wall)
        Possible x positions for agents will be in range [1,width]
        """
        util.raiseNotDefined()

    def getHeight(self):
        """
        Returns the height of the playable grid (does not include the external wall)
        Possible y positions for agents will be in range [1,height]
        """
        util.raiseNotDefined()

    def isWall(self, position):
        """
        Return true if position (x,y) is a wall. Returns false otherwise.
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


def atLeastOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at least one of the expressions in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    return logic.Expr('|', *expressions)

def atMostOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at most one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    clauses = []
    for i in xrange(0, len(expressions)):
        for j in xrange(i + 1, len(expressions)):
            clauses.append(~expressions[i] | ~expressions[j])
    return logic.Expr('&', *clauses)

def exactlyOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that exactly one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    clauses = [logic.Expr('|', *expressions)]
    for i in xrange(0, len(expressions) - 1):
        for j in xrange(i + 1, len(expressions)):
            clauses.append(~expressions[i] | ~expressions[j])
    return logic.Expr('&', *clauses)

def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    actions_taken = []
    for symbol, val in model.items():
        parsed = logic.PropSymbolExpr.parseExpr(symbol)
        if parsed[0] in actions and val:
            actions_taken.append(parsed)
    result = [None]*len(actions_taken)
    for action, time in actions_taken:
        index = int(time)
        result[index] = action
    return result

def positionLogicPlan(problem):
    """
    Given an instance of a PositionSearchProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    ACTIONS = [game.Directions.NORTH, game.Directions.SOUTH, game.Directions.EAST, game.Directions.WEST]
    T = 0
    KB = []
    model = None
    #Start state axiom.
    x, y = problem.getStartState()
    KB.append(logic.PropSymbolExpr('Pos', x, y, 0))
    #Position domain constraints.
    positions = []
    for i in xrange(1, problem.getWidth()+1):
        for j in xrange(1, problem.getHeight()+1):
            if not problem.isWall((i, j)):
                positions.append(logic.PropSymbolExpr('Pos', i, j, T))
    KB.append(exactlyOne(positions))
    while not model:
        if T != 0:
            #Action domain constraints.
            action_times = []
            action_times.append(logic.PropSymbolExpr('North', T-1))
            action_times.append(logic.PropSymbolExpr('South', T-1))
            action_times.append(logic.PropSymbolExpr('East', T-1))
            action_times.append(logic.PropSymbolExpr('West', T-1))
            KB.append(exactlyOne(action_times))
            #State successor axioms.
            for i in xrange(1, problem.getWidth()+1):
                for j in xrange(1, problem.getHeight()+1):
                    if not problem.isWall((i, j)):
                        pos = logic.PropSymbolExpr('Pos', i, j, T)
                        legal_actions = problem.actions((i, j))
                        prev_pos = []
                        if game.Directions.NORTH in legal_actions:
                            a = logic.PropSymbolExpr('Pos', i, j+1, T-1)
                            b = logic.PropSymbolExpr('South', T-1)
                            prev_pos.append(a & b)
                        if game.Directions.SOUTH in legal_actions:
                            a = logic.PropSymbolExpr('Pos', i, j-1, T-1)
                            b = logic.PropSymbolExpr('North', T-1)
                            prev_pos.append(a & b)
                        if game.Directions.EAST in legal_actions:
                            a = logic.PropSymbolExpr('Pos', i+1, j, T-1)
                            b = logic.PropSymbolExpr('West', T-1)
                            prev_pos.append(a & b)
                        if game.Directions.WEST in legal_actions:
                            a = logic.PropSymbolExpr('Pos', i-1, j, T-1)
                            b = logic.PropSymbolExpr('East', T-1)
                            prev_pos.append(a & b)
                        KB.append(logic.to_cnf(pos % logic.Expr('|', *prev_pos)))
        #Goal state axiom.
        x, y = problem.getGoalState()
        model = logic.pycoSAT(KB + [logic.PropSymbolExpr('Pos', x, y, T)])
        T += 1
    return extractActionSequence(model, ACTIONS)

def foodLogicPlan(problem):
    """
    Given an instance of a FoodSearchProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    ACTIONS = [game.Directions.NORTH, game.Directions.SOUTH, game.Directions.EAST, game.Directions.WEST]
    T = 0
    KB = []
    model = None
    #Start state axiom.
    (x, y), food_grid = problem.getStartState()
    KB.append(logic.PropSymbolExpr('Pos', x, y, 0))
    #Food positions.
    for x, y in food_grid.asList():
        KB.append(logic.PropSymbolExpr('Food', x, y, T))
    #Position domain constraints.
    positions = []
    for i in xrange(1, problem.getWidth()+1):
        for j in xrange(1, problem.getHeight()+1):
            if not problem.isWall((i, j)):
                positions.append(logic.PropSymbolExpr('Pos', i, j, T))
    KB.append(exactlyOne(positions))
    while not model:
        if T != 0:
            #Action domain constraints.
            action_times = []
            action_times.append(logic.PropSymbolExpr('North', T-1))
            action_times.append(logic.PropSymbolExpr('South', T-1))
            action_times.append(logic.PropSymbolExpr('East', T-1))
            action_times.append(logic.PropSymbolExpr('West', T-1))
            KB.append(exactlyOne(action_times))
            #Position transition model.
            for i in xrange(1, problem.getWidth()+1):
                for j in xrange(1, problem.getHeight()+1):
                    if not problem.isWall((i, j)):
                        pos = logic.PropSymbolExpr('Pos', i, j, T)
                        legal_actions = problem.actions(((i, j), None))
                        prev_pos = []
                        if game.Directions.NORTH in legal_actions:
                            a = logic.PropSymbolExpr('Pos', i, j+1, T-1)
                            b = logic.PropSymbolExpr('South', T-1)
                            prev_pos.append(a & b)
                        if game.Directions.SOUTH in legal_actions:
                            a = logic.PropSymbolExpr('Pos', i, j-1, T-1)
                            b = logic.PropSymbolExpr('North', T-1)
                            prev_pos.append(a & b)
                        if game.Directions.EAST in legal_actions:
                            a = logic.PropSymbolExpr('Pos', i+1, j, T-1)
                            b = logic.PropSymbolExpr('West', T-1)
                            prev_pos.append(a & b)
                        if game.Directions.WEST in legal_actions:
                            a = logic.PropSymbolExpr('Pos', i-1, j, T-1)
                            b = logic.PropSymbolExpr('East', T-1)
                            prev_pos.append(a & b)
                        KB.append(logic.to_cnf(pos % logic.Expr('|', *prev_pos)))
            #Food transition model.
            for x, y in food_grid.asList():
                food = logic.PropSymbolExpr('Food', x, y, T)
                food_prev = logic.PropSymbolExpr('Food', x, y, T-1)
                legal_actions = problem.actions(((x, y), None))
                prev_pos = []
                if game.Directions.NORTH in legal_actions:
                    a = logic.PropSymbolExpr('Pos', x, y+1, T-1)
                    b = logic.PropSymbolExpr('South', T-1)
                    prev_pos.append(a & b)
                if game.Directions.SOUTH in legal_actions:
                    a = logic.PropSymbolExpr('Pos', x, y-1, T-1)
                    b = logic.PropSymbolExpr('North', T-1)
                    prev_pos.append(a & b)
                if game.Directions.EAST in legal_actions:
                    a = logic.PropSymbolExpr('Pos', x+1, y, T-1)
                    b = logic.PropSymbolExpr('West', T-1)
                    prev_pos.append(a & b)
                if game.Directions.WEST in legal_actions:
                    a = logic.PropSymbolExpr('Pos', x-1, y, T-1)
                    b = logic.PropSymbolExpr('East', T-1)
                    prev_pos.append(a & b)
                not_eaten = ~atLeastOne(prev_pos)
                KB.append(logic.to_cnf(food % (food_prev & not_eaten)))
        #Goal state axiom.
        food_pos = []
        for x, y in food_grid.asList():
            food_pos.append(logic.PropSymbolExpr('Food', x, y, T))
        model = logic.pycoSAT(KB + [logic.to_cnf(~atLeastOne(food_pos))])
        T += 1
    return extractActionSequence(model, ACTIONS)

def foodGhostLogicPlan(problem):
    """
    Given an instance of a FoodGhostSearchProblem, return a list of actions that help Pacman
    eat all of the food and avoid patrolling ghosts.
    Ghosts only move east and west. They always start by moving East, unless they start next to
    and eastern wall. 
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    ACTIONS = [game.Directions.NORTH, game.Directions.SOUTH, game.Directions.EAST, game.Directions.WEST]
    T = 0
    KB = []
    model = None
    #Start state axiom.
    (x, y), food_grid = problem.getStartState()
    KB.append(logic.PropSymbolExpr('Pos', x, y, 0))
    #Food positions.
    for x, y in food_grid.asList():
        KB.append(logic.PropSymbolExpr('Food', x, y, T))
    #Initial ghost positions.
    for ghostState in problem.getGhostStartStates():
        x, y = ghostState.getPosition()
        if problem.isWall((x+1, y)):
            KB.append(logic.PropSymbolExpr('GhostWest', x, y, T))
        else:
            KB.append(logic.PropSymbolExpr('GhostEast', x, y, T))
    #Position domain constraints.
    positions = []
    for i in xrange(1, problem.getWidth()+1):
        for j in xrange(1, problem.getHeight()+1):
            if not problem.isWall((i, j)):
                positions.append(logic.PropSymbolExpr('Pos', i, j, T))
    KB.append(exactlyOne(positions))
    while not model:
        if T != 0:
            #Action domain constraints.
            action_times = []
            action_times.append(logic.PropSymbolExpr('North', T-1))
            action_times.append(logic.PropSymbolExpr('South', T-1))
            action_times.append(logic.PropSymbolExpr('East', T-1))
            action_times.append(logic.PropSymbolExpr('West', T-1))
            KB.append(exactlyOne(action_times))
            #Position transition axioms.
            for i in xrange(1, problem.getWidth()+1):
                for j in xrange(1, problem.getHeight()+1):
                    if not problem.isWall((i, j)):
                        pos = logic.PropSymbolExpr('Pos', i, j, T)
                        legal_actions = problem.actions(((i, j), None))
                        prev_pos = []
                        ghost_incoming = []
                        if game.Directions.NORTH in legal_actions:
                            a = logic.PropSymbolExpr('Pos', i, j+1, T-1)
                            b = logic.PropSymbolExpr('South', T-1)
                            prev_pos.append(a & b)
                        if game.Directions.SOUTH in legal_actions:
                            a = logic.PropSymbolExpr('Pos', i, j-1, T-1)
                            b = logic.PropSymbolExpr('North', T-1)
                            prev_pos.append(a & b)
                        if game.Directions.EAST in legal_actions:
                            a = logic.PropSymbolExpr('Pos', i+1, j, T-1)
                            b = logic.PropSymbolExpr('West', T-1)
                            prev_pos.append(a & b)
                            ghost_incoming.append(logic.PropSymbolExpr('GhostWest', i+1, j, T-1))
                        if game.Directions.WEST in legal_actions:
                            a = logic.PropSymbolExpr('Pos', i-1, j, T-1)
                            b = logic.PropSymbolExpr('East', T-1)
                            prev_pos.append(a & b)
                            ghost_incoming.append(logic.PropSymbolExpr('GhostEast', i-1, j, T-1))
                        threat = logic.PropSymbolExpr('GhostEast', i, j, T-1) | logic.PropSymbolExpr('GhostWest', i, j, T-1)
                        if ghost_incoming:
                            threat = threat | logic.Expr('|', *ghost_incoming)
                        condition = ~threat & logic.Expr('|', *prev_pos)
                        KB.append(logic.to_cnf(pos % condition))
            #Ghost position transition model.
            for i in xrange(1, problem.getWidth()+1):
                for j in xrange(1, problem.getHeight()+1):
                    if not problem.isWall((i, j)):
                        pos = logic.PropSymbolExpr('GhostEast', i, j, T)
                        legal_actions = problem.actions(((i, j), None))
                        if game.Directions.WEST in legal_actions and game.Directions.EAST in legal_actions:
                            a = logic.PropSymbolExpr('GhostEast', i-1, j, T-1)
                            KB.append(logic.to_cnf(pos % a))
                        elif game.Directions.EAST in legal_actions:
                            a = logic.PropSymbolExpr('GhostWest', i+1, j, T-1)
                            KB.append(logic.to_cnf(pos % a))
                        pos = logic.PropSymbolExpr('GhostWest', i, j, T)
                        if game.Directions.WEST in legal_actions and game.Directions.EAST in legal_actions:
                            a = logic.PropSymbolExpr('GhostWest', i+1, j, T-1)
                            KB.append(logic.to_cnf(pos % a))
                        elif game.Directions.WEST in legal_actions:
                            a = logic.PropSymbolExpr('GhostEast', i-1, j, T-1)
                            KB.append(logic.to_cnf(pos % a))
            #Food transition model.
            for x, y in food_grid.asList():
                food = logic.PropSymbolExpr('Food', x, y, T)
                food_prev = logic.PropSymbolExpr('Food', x, y, T-1)
                legal_actions = problem.actions(((x, y), None))
                prev_pos = []
                if game.Directions.NORTH in legal_actions:
                    a = logic.PropSymbolExpr('Pos', x, y+1, T-1)
                    b = logic.PropSymbolExpr('South', T-1)
                    prev_pos.append(a & b)
                if game.Directions.SOUTH in legal_actions:
                    a = logic.PropSymbolExpr('Pos', x, y-1, T-1)
                    b = logic.PropSymbolExpr('North', T-1)
                    prev_pos.append(a & b)
                if game.Directions.EAST in legal_actions:
                    a = logic.PropSymbolExpr('Pos', x+1, y, T-1)
                    b = logic.PropSymbolExpr('West', T-1)
                    prev_pos.append(a & b)
                if game.Directions.WEST in legal_actions:
                    a = logic.PropSymbolExpr('Pos', x-1, y, T-1)
                    b = logic.PropSymbolExpr('East', T-1)
                    prev_pos.append(a & b)
                not_eaten = ~atLeastOne(prev_pos)
                KB.append(logic.to_cnf(food % (food_prev & not_eaten)))
        #Goal state axiom.
        food_pos = []
        for x, y in food_grid.asList():
            food_pos.append(logic.PropSymbolExpr('Food', x, y, T))
        model = logic.pycoSAT(KB + [logic.to_cnf(~atLeastOne(food_pos))])
        T += 1
    return extractActionSequence(model, ACTIONS)

# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)



