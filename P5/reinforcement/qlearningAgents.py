# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    # *********************
    #    Question 6 
    # *********************
    def __init__(self, **args):
        """ 
        Question 6
        """
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.QValues = util.Counter()

    # *********************
    #    Question 6 
    # *********************
    def getQValue(self, state, action):
        """
        Question 6 

          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        pair = (state, action)
        return 0 if pair not in self.QValues.keys() else self.QValues[pair]

    # *********************
    #    Question 6 
    # *********************
    def computeValueFromQValues(self, state):
        """
        Question 6 

          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        actions = self.getLegalActions(state)
        if actions == ():
            return 0
        elif "isWin" in dir(state) and (state.isWin() or state.isLose()):
            return 0
        else:
            maxValue = float('-inf')
            for action in actions:
                QValue = self.getQValue(state, action)
                maxValue = QValue if QValue > maxValue else maxValue
            return maxValue

    # *********************
    #    Question 6 
    # *********************
    def computeActionFromQValues(self, state):
        """
        Question 6 

          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.getLegalActions(state)
        if actions == ():
            return None
        elif  ("isWin" in dir(state)) and (state.isWin() or state.isLose()):
            return 0
        else:
            qState = util.Counter()
            for action in actions:
                qState.update({(state, action): self.getQValue(state, action)})
            maxValue = float('-inf')
            bestActions = []
            for i in qState.items():
                if i[1] > maxValue:
                    maxValue = i[1]
                    bestActions = [i[0][1]]
                if i[1] == maxValue:
                    bestActions.append(i[0][1])
            bestAction = random.choice(bestActions)
            return bestAction

    # *********************
    #    Question 7 
    # *********************
    def getAction(self, state):
        """
        Question 7 

          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        if legalActions == ():
            return None
        elif  ("isWin" in dir(state)) and (state.isWin() or state.isLose()):
            return 0
        else:
            #act randomly 
            if util.flipCoin(self.epsilon):
                action = random.choice(legalActions)
            else:
                #act optimally
                action = self.computeActionFromQValues(state)
        return action

    # *********************
    #    Question 6 
    # *********************
    def update(self, state, action, nextState, reward):
        """
        Question 6 

          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        pari = (state, action)
        self.QValues[pari] = (1 - self.alpha) * self.QValues[pari] + self.alpha * (reward + self.discount * self.computeValueFromQValues(nextState))

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    # *********************
    #    Question 10
    # *********************
    def getQValue(self, state, action):
        """
        Question 10 

          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        features = self.featExtractor.getFeatures(state, action)
        self.weights.incrementAll(features.keys(), 0)
        QValue = features * self.weights
        return QValue

    # *********************
    #    Question 10 
    # *********************
    def update(self, state, action, nextState, reward):
        """
        Question 10 
        
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        diff = reward + self.discount * self.getValue(nextState) - self.getQValue(state, action)
        features = self.featExtractor.getFeatures(state, action)
        for i in self.weights.keys():
            self.weights[i] = self.weights[i] + self.alpha * diff * features[i]

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
