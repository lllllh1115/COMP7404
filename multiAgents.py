from util import manhattanDistance
from game import Directions

##################################
### Something mentioned below! ###
### Best Regards,   Lian Huan  ###
##################################

###    In order to make the solution widely used, I added loads of warnings, to help other users.
### Q1 setting randomnumber (80,100) will get an average of 1250
###    setting 100 will get an average of 1050
###    setting (98,102) will get an average of 1150
###    the randomized decision is risky.
###    This work well on python pacman.py --frameTime 0 -p ReflexAgent -k 2
###    Usually win with 900-1900 points.
### Q2 a minimaxFunction which return a score and a legalMove is time-consuming
###    and till the last "floor" there is no need to record the movement.
### Q3 minimax with pruning, no need to continue calculating sometimes.
### Q4 expectimax, change of minimax.
### Q5 Please read the DESCRIPTION.

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
        prevFood = currentGameState.getFood()
        ### print("preFood",prevFood)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        ### print("newPos",newPos)
        newFood = successorGameState.getFood()
        ### print("newFood",newFood)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        ### print("ST",newScaredTimes,type(newScaredTimes))

        "*** YOUR CODE HERE ***"
        ### .asList() is still a useful function, rather than in assignment 1.
        ###                                                  ---Lian Huan, Oct. 6th.
        prevCap = currentGameState.getCapsules()
        newCap = successorGameState.getCapsules()
        newFoodList = newFood.asList()
        prevFoodList = prevFood.asList()
        outputScore = 0

        ### Consider the distances.

        ### Consider ghost distances and find the minimized one.
        ghostDis = []
        if len(newGhostStates) > 0:
            for ghost in newGhostStates:
                ghostDis.append(manhattanDistance(ghost.getPosition(), newPos))
        else:
            ghostDis = [-1]
            print("Warning: There is no Ghost! We will consider the ghostDis as 0!")

        closeGhost = min(ghostDis)
        if closeGhost > 1:
            outputScore += 2*closeGhost
        elif min(newScaredTimes) >= 2 or closeGhost == -1:
            ### print(newScaredTimes)
            outputScore += 0
        else:
            outputScore += -500

        ### Consider food distances.
        foodDis = []
        if len(newFoodList) > 0:
            for food in newFoodList:
                foodDis.append(manhattanDistance(food,newPos))

        if len(foodDis) > 0:
            minfood = min(foodDis)
            farfood = max(foodDis)
            if minfood != farfood:
                outputScore += 40 / minfood
                outputScore += 15 / farfood
            else:
                outputScore += 40 / minfood
        else:
            return 1000

        ### Consider Capsule distances.
        capDis = []
        if len(newCap) > 0:
            for cap in newCap:
                capDis.append(manhattanDistance(cap, newPos))
            mincap = min(capDis)
            outputScore += 40/mincap

        ### Consider what we have done.

        ### Consider whether a new step will eat a food:
        scoreOfEatFood = 0
        if len(prevFoodList) > len(newFoodList):
            scoreOfEatFood = 30
        outputScore += scoreOfEatFood

        ### Consider whether we can eat the capsule:
        scoreOfEatCap = 0
        if len(prevCap) > len(newCap):
            scoreOfEatCap = 100
        outputScore += scoreOfEatCap

        ### The above solution will get 2/3.
        ### From my observation, it is key to avoid stop for too much, some times find a way.

        if action == "Stop":
            randomplus = random.randint(98,102)
            outputScore += -randomplus

        return outputScore
        

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
        # Collect legal moves and successor states
        ### pacman always 0
        legalMoves = gameState.getLegalActions(0)

        ### This step we need to record the action, while other steps do not.
        ### So we start the recursive steps via a function from agent = 1 !
        score = -99999
        agentNum = gameState.getNumAgents()

        if agentNum <= 1:
            print("Warning: There are less than 2 agents!")

        for lgm in legalMoves:
            stateAhead = gameState.generateSuccessor(0, lgm)
            ghostMinimaxScore = self.minimaxFunction(1, range(gameState.getNumAgents()), stateAhead, self.depth, self.evaluationFunction)

            if ghostMinimaxScore > score:
                score = ghostMinimaxScore
                minimaxAction = lgm

        if len(minimaxAction) > 0:
            return minimaxAction
        else:
            print("Warning: There is no legalMoves!")
            util.raiseNotDefined()

    def minimaxFunction(self,agent, agents, stateAhead, depth, evaluationFunc):
        '''
            A function created for minimax tree. By Lian Huan in Oct. 6th, 2021

            Input the current agent(0 in pacman, others are ghosts)
            agents is a list [0,1] or [0,1,2]
            stateAhead is successor state.
        '''
        if depth <= 0 or \
                stateAhead.isWin() or stateAhead.isLose():
            return evaluationFunc(stateAhead)

        if agent == 0:
            score = -99999
        else:
            score = 99999

        legalMoves = stateAhead.getLegalActions(agent)
        for lgm in legalMoves:
            successor= stateAhead.generateSuccessor(agent, lgm)
            if agent == 0:
                score = max(score, self.minimaxFunction(agents[agent + 1], agents, successor, depth, evaluationFunc))
                if score <= -99999:
                    print("Warning: Scores overflow!")
            ### depth go down in the last agent
            elif agent == agents[-1]:
                score = min(score, self.minimaxFunction(agents[0], agents, successor, depth - 1, evaluationFunc))
                if score >= 99999:
                    print("Warning: Scores overflow!")
            else:
                score = min(score, self.minimaxFunction(agents[agent + 1], agents, successor, depth, evaluationFunc))
                if score >= 99999:
                    print("Warning: Scores overflow!")

        return score

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # Collect legal moves and successors states
        ### pacman always 0
        legalMoves = gameState.getLegalActions(0)

        ### This step we need to record the action, while other steps do not.
        ### So we start the recursive steps via a function from agent = 1 !
        score = -99999.0
        alpha = -99999.0
        beta = 99999.0
        agentNum = gameState.getNumAgents()

        if agentNum <= 1:
            print("Warning: There are less than 2 agents!")

        for lgm in legalMoves:
            stateAhead = gameState.generateSuccessor(0, lgm)
            ghostMinimaxScore = self.minimaxFunction(1, range(0,agentNum), stateAhead, self.depth,
                                                     self.evaluationFunction,alpha,beta)

            if ghostMinimaxScore > score:
                score = ghostMinimaxScore
                minimaxAction = lgm
            if ghostMinimaxScore > beta:
                return minimaxAction
            alpha = max(alpha, ghostMinimaxScore)

        if len(minimaxAction) > 0:
            return minimaxAction
        else:
            print("Warning: There is no legalMoves!")
            util.raiseNotDefined()

    def minimaxFunction(self, agent, agents, stateAhead, depth, evaluationFunc, alpha, beta):
        '''
            A function created for minimax tree. By Lian Huan in Oct. 7th, 2021

            Input the current agent(0 in pacman, others are ghosts)
            agents is a list [0,1] or [0,1,2]
            stateAhead is successor state.
            alpha, beta is the pruning value.
        '''
        if depth <= 0 or stateAhead.isWin() or stateAhead.isLose():
            return evaluationFunc(stateAhead)

        if agent == 0:
            score = -99999.0
        else:
            score = 99999.0

        legalMoves = stateAhead.getLegalActions(agent)
        for lgm in legalMoves:
            successor = stateAhead.generateSuccessor(agent, lgm)

            if agent == 0:
                score = max(score, self.minimaxFunction(agents[agent + 1], agents, successor, depth, evaluationFunc, alpha, beta))
                if score > beta:
                    return score
                alpha = max(score, alpha)
                if score <= -99999:
                    print("Warning: Scores overflow!")
            ### depth go down in the last agent
            elif agent == agents[-1]:
                score = min(score, self.minimaxFunction(agents[0], agents, successor, depth - 1, evaluationFunc, alpha, beta))
                if score < alpha:
                    return score
                beta = min(score, beta)
                if score >= 99999:
                    print("Warning: Scores overflow!")
            else:
                score = min(score, self.minimaxFunction(agents[agent + 1], agents, successor, depth, evaluationFunc, alpha, beta))
                if score < alpha:
                    return score
                beta = min(score, beta)
                if score >= 99999:
                    print("Warning: Scores overflow!")

        return score

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
        # Collect legal moves and successor states
        ### pacman always 0
        legalMoves = gameState.getLegalActions(0)

        ### This step we need to record the action, while other steps do not.
        ### So we start the recursive steps via a function from agent = 1 !
        score = -99999
        agentNum = gameState.getNumAgents()

        if agentNum <= 1:
            print("Warning: There are less than 2 agents!")

        for lgm in legalMoves:
            stateAhead = gameState.generateSuccessor(0, lgm)
            ghostMinimaxScore = self.expectimaxFunction(1, range(gameState.getNumAgents()), stateAhead, self.depth,
                                                     self.evaluationFunction)

            if ghostMinimaxScore > score:
                score = ghostMinimaxScore
                minimaxAction = lgm

        if len(minimaxAction) > 0:
            return minimaxAction
        else:
            print("Warning: There is no legalMoves!")
            util.raiseNotDefined()

    def expectimaxFunction(self,agent, agents, stateAhead, depth, evaluationFunc):
        '''
            A function created for minimax tree. By Lian Huan in Oct. 6th, 2021

            Input the current agent(0 in pacman, others are ghosts)
            agents is a list [0,1] or [0,1,2]
            stateAhead is successor state.
        '''
        if depth <= 0 or \
                stateAhead.isWin() or stateAhead.isLose():
            return evaluationFunc(stateAhead)

        if agent == 0:
            score = -9999
        else:
            score = 0

        legalMoves = stateAhead.getLegalActions(agent)
        weight = len(legalMoves)
        for lgm in legalMoves:
            successor= stateAhead.generateSuccessor(agent, lgm)
            if agent == 0:
                score = max(score, self.expectimaxFunction(agents[agent + 1], agents, successor, depth, evaluationFunc))
                if score <= -99999:
                    print("Warning: Scores overflow!")
            ### depth go down in the last agent
            elif agent == agents[-1]:
                score = score + self.expectimaxFunction(agents[0], agents, successor, depth - 1, evaluationFunc)

            else:
                score = score + self.expectimaxFunction(agents[agent + 1], agents, successor, depth, evaluationFunc)

        if agent == 0:
            return score
        else:
            return score/weight


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:
      Similar to Question 1, we can obtain some useful information.

      However, it is easy to gain an average of 900-1000, but really hard to gain an average over 1000.
      My current solution is silghtly over 1000 and gain 1041.0 and receive 5/5 in the autograder.

      All weights are specially-designed, and they basically reflect my opinion against those factors.
      General formula of the outputScore is:
      outputScore =  80 / mincap + 2 * closeGhost + 60 / minfood + 15 / farfood + C/foodNum + 4 * originalScore
                     + 45 / foodDis[2] + 15 / sum(foodDis),
      while some specific situation we will have different changes.

      Good Luck, Lian Huan, Oct. 7th.
    """
    # Useful information you can extract from a GameState (pacman.py)
    Food = currentGameState.getFood()
    Position = currentGameState.getPacmanPosition()
    FoodList = Food.asList()
    foodNum = currentGameState.getNumFood()
    ghostStates = currentGameState.getGhostStates()
    originScore = currentGameState.getScore()
    Capsules = currentGameState.getCapsules()

    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    ### print(scaredTimes),  it is a list!!!
    agentNum = currentGameState.getNumAgents()
    outputScore = 0

    if agentNum <= 1:
        print("Warning: There is only one agent!")

    if currentGameState.isWin():
        return 9999
    elif currentGameState.isLose():
        return -9999

    ### Consider the distances.

    ### Consider ghost distances and find the minimized one.
    ghostDis = []
    if len(ghostStates) > 0:
        for ghost in ghostStates:
            ghostDis.append(manhattanDistance(ghost.getPosition(), Position))
    else:
        ghostDis = [-1]
        print("Warning: There is no Ghost! We will consider the ghostDis as -1!")

    closeGhost = min(ghostDis)
    if closeGhost > 1:
        outputScore += 2 * closeGhost

    ### Only slightly influence on setting min >= 1 or 2
    elif min(scaredTimes) >= 1 or closeGhost == -1:
        ### print(newScaredTimes)
        outputScore += 300
    else:
        outputScore += -600

    ### Consider food distances.
    foodDis = []
    if foodNum > 0:
        for food in FoodList:
            foodDis.append(manhattanDistance(food, Position))

    if len(foodDis) > 0:
        minfood = min(foodDis)
        farfood = max(foodDis)
        if minfood != farfood:
            outputScore += 60 / minfood
            outputScore += 15 / farfood
        else:
            outputScore += 80 / minfood
    else:
        return 9999


    ### Consider Capsule distances.
    capDis = []
    if len(Capsules) > 0:
        for cap in Capsules:
            capDis.append(manhattanDistance(cap, Position))
        mincap = min(capDis)
        outputScore += 80 / mincap

    ### Consider a bit about the original evalFunction:
    outputScore += 4 * originScore

    ### Consider whether we eat a food.
    ### Note: we only estimate this state, so it is best to use a "Global Function"

    if foodNum > 10:
        outputScore += 80/foodNum
    elif foodNum > 5:
        outputScore += 100/foodNum
    elif foodNum > 3:
        outputScore += 105/foodNum
    else:
        outputScore += 200/foodNum
    ### Any such operation resulted a 900-1000 result.
    #legalMoves = currentGameState.getLegalActions()
    #counter = 0
    #for moves in legalMoves:
    #    successor = currentGameState.generateSuccessor(0, moves)
    #    successorNumFood = successor.getNumFood()
    #    if successorNumFood < foodNum:
    #        counter += 1
    #outputScore += counter*10 + outputScore

    ### Before this part the average is 1015.3.
    foodDis.sort()
    if foodNum > 3:
        outputScore += (45/foodDis[2]+15/sum(foodDis))

    return outputScore

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

