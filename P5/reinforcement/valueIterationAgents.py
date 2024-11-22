# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    # *********************
    #    Question 1
    # *********************
    def runValueIteration(self):
        # Write value iteration code here
        """ 
        Question 1: runValueIteration method 
        """
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        for _ in range(self.iterations):
            copyValues = self.values.copy()
            for state in states:
                if self.mdp.isTerminal(state):
                    copyValues[state] = 0
                else:
                    actions = self.mdp.getPossibleActions(state)
                    maxQValue = max(self.computeQValueFromValues(state, action) for action in actions)
                    copyValues[state] = maxQValue
            self.values = copyValues

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    # *********************
    #    Question 1
    # *********************
    def computeQValueFromValues(self, state, action):
        """
        Question 1 

          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        ans = 0
        if self.mdp.isTerminal(state):
            return 0
        nextStatePorb = self.mdp.getTransitionStatesAndProbs(state, action)
        for pairStateProb in nextStatePorb:
            ans = ans + pairStateProb[1] * (self.mdp.getReward(state, action, pairStateProb[0]) + self.discount * self.getValue(pairStateProb[0]))
        return ans

    # *********************
    #    Question 1 
    # *********************
    def computeActionFromValues(self, state):
        """
        Question 1 

          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        import random
        if self.mdp.isTerminal(state):
            return None
        actions = self.mdp.getPossibleActions(state)
        maxValue = float('-inf')
        bestActions = []
        for action in actions:
            valueOfAction = self.computeQValueFromValues(state, action)
            if valueOfAction > maxValue:
                bestActions = [action]
                maxValue = valueOfAction
            elif valueOfAction == maxValue:
                bestActions.append(action)
            else:
                pass
        return random.choice(bestActions)

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    # *********************
    #    Question 4
    # *********************
    def runValueIteration(self):
        """
        Question 4
        """
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        actions = self.mdp.getPossibleActions
        for limit in range(self.iterations):
            state = states[limit % len(states)]
            if not self.mdp.isTerminal(state) and actions(state):
                maxValue = max(self.computeQValueFromValues(state, action) for action in actions(state))
                self.values[state] = maxValue


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    # *********************
    #    Question 5 
    # *********************
    def runValueIteration(self):
        """
        Question 5 - Extra Credit
        """
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        priorityQueue = util.PriorityQueue()
        predecessors = {}

        for state in states:
            if not self.mdp.isTerminal(state):
                maxActionValue = float('-inf')
                for action in self.mdp.getPossibleActions(state):
                    actionvalue = self.computeQValueFromValues(state, action)
                    if maxActionValue <= actionvalue:
                        maxActionValue = actionvalue
                    diff = abs(self.values[state] - maxActionValue)
                    priorityQueue.update(state, -diff)

                    for nextState, _ in self.mdp.getTransitionStatesAndProbs(state, action):
                        if nextState in predecessors:
                            predecessors[nextState].add(state)
                        else:
                            predecessors[nextState] = {state}
                            
        for _ in range(self.iterations):
            if priorityQueue.isEmpty():
                return 
            highestPriorityState = priorityQueue.pop()
            if not self.mdp.isTerminal(highestPriorityState):
                maxActionValue = float('-inf')
                actions = self.mdp.getPossibleActions(highestPriorityState)
                for action in actions:
                    actionvalue = self.getQValue(highestPriorityState, action)
                    if maxActionValue <= actionvalue:
                        maxActionValue = actionvalue 
                self.values[highestPriorityState] = maxActionValue

            for nextState in predecessors[highestPriorityState]:
                if not self.mdp.isTerminal(nextState):
                    maxActionValue = float('-inf')
                    for possibleAction in self.mdp.getPossibleActions(nextState):
                        posActionValue = self.getQValue(nextState, possibleAction)
                        if maxActionValue <= posActionValue:
                            maxActionValue = posActionValue
                    difference = abs( self.values[nextState] - maxActionValue)
                    if difference > self.theta:
                        priorityQueue.update(nextState, -difference)
