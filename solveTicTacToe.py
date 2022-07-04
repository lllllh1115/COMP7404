#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Chen Guanying 
#     Creation Date       :     [2017-03-18 19:17]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :      
#################################################################################

import copy
import util 
import sys
import random
import time
from optparse import OptionParser
import numpy as np

class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything, 
      however.
    """
    def __init__(self):
        """
          Represent 3 boards with lists of boolean value 
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board) 
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append( chr(b+ASCII_OF_A) + str(i) )
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]: 
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)

class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe. 
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}
        
    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            #check every row
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            #check every column
            if board[i] and board[i+3] and board[i+6]:
                return True
        return False

    def isGameOver(self, boards):
        """
          Check whether the game is over  
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])
    def FingerprintONE(self, board):
        """
            Check whether a board contains one TRUE
            Ouput number 1 or c^2 = 25
        """
        if board[0] or board[2] or board[6] or board[8] or board[1] or board[3] or board[5] or board[7]:
            return 1
        else:
            return 5*5

    def FingerprintTWO(self, board):
        """
            Check a board contains two TRUE
            Output number b = 3 or a*d = 14, or a = 2
        """
        boardnp = np.array([board[0:3], board[3:6], board[6:9]])
        posnp = np.argwhere(boardnp == True)
        trueDis = []
        trueDis.append(util.manhattanDistance(posnp[0], posnp[1]))
        t1 = sum([board[0], board[2], board[6], board[8]])
        t2 = sum([board[1], board[3], board[5], board[7]])
        totalDis = sum(trueDis)
        if board[4]:
            return 3
        elif t2 == 2:
            return 2
        elif t1 == 2 and totalDis == 4:
            return 2
        elif t1 == 2 and totalDis == 2:
            return 3
        elif totalDis == 1:
            return 14
        elif totalDis == 2 or totalDis == 3:
            return 3
        else:
            print("Warning! There is an error!!! Two-Generalcase")
            return 1

    def FingerprintTHREE(self, board):
        """
            Check a board contains three TRUE
            Output a = 2, b = 3, c = 5, d = 7
        """
        t1 = sum([board[0], board[2], board[6], board[8]])
        t2 = sum([board[1], board[3], board[5], board[7]])

        if board[4]:
            boardnp = np.array([board[0:3], board[3:6], board[6:9]])
            posnp = np.argwhere(boardnp == True)
            trueDis = []
            trueDis.append(util.manhattanDistance(posnp[0], posnp[1]))
            trueDis.append(util.manhattanDistance(posnp[0], posnp[2]))
            trueDis.append(util.manhattanDistance(posnp[1], posnp[2]))
            totalDis = sum(trueDis)
            if t1 != 1:
                return 6-2*t1    ### TFT FTF FFF  or FTF FTT FFF
                ### t = 2 return a = 2, t = 0 return 6
            elif totalDis == 4:
                return 6         ### TTF FTF FFF or FTF TTF FFF
            elif totalDis == 6:
                return 2         ### TFF FTT FFF
            else:
                print("Warning!!! There is a error!!! Three-board[4]")
                return 1
        elif t2 == 2:
            #if (abs(posnp[0][0]-posnp[1][0]) == 0 and abs(posnp[0][1]-posnp[1][1]) == 2) or \
            #    (abs(posnp[2][0]-posnp[1][0]) ==0 and abs(posnp[2][1]-posnp[1][1]) == 2) or \
            #    (abs(posnp[0][0] - posnp[2][0]) == 0 and abs(posnp[0][1] - posnp[2][1]) == 2) or \
            #    (abs(posnp[0][0] - posnp[1][0]) == 2 and abs(posnp[0][1] - posnp[1][1]) == 0) or \
            #    (abs(posnp[2][0] - posnp[1][0]) == 2 and abs(posnp[2][1] - posnp[1][1]) == 0) or \
            #    (abs(posnp[0][0] - posnp[2][0]) == 2 and abs(posnp[0][1] - posnp[2][1]) == 0):
            boardnp = np.array([board[0:3], board[3:6], board[6:9]])
            posnp = np.argwhere(boardnp == True)
            trueDis = []
            trueDis.append(util.manhattanDistance(posnp[0], posnp[1]))
            trueDis.append(util.manhattanDistance(posnp[0], posnp[2]))
            trueDis.append(util.manhattanDistance(posnp[1], posnp[2]))
            totalDis = sum(trueDis)
            if totalDis == 4:
                return 3   ### TTF TFF FFF
            elif totalDis == 6:
                return 7   ### TTF FFT FFF or TTF FFF FTF
            elif totalDis == 8:
                return 1   ### TFF FFT FTF
            else:
                print("Warning!!! There is a error!!! Three-t2==2")
                return 1
        elif t2 == 3:
            return 3       ### FTF TFT FFF
        elif t2 == 0:
            return 6       ### TFT FFF TFF
        elif t2 == 1:
            if (board[0] and board[8]) or (board[2] and board[6]):
                return 7   ### TTF FFF FFT
            else:
                return 2   ### TFT FFF FTF or TFT FFT FFF
        else:
            print("Warning! There is an error!!! Three-Generalcase")
            return 1

    def FingerprintFOUR(self, board):
        """
            Check a board contains Four TRUE
            Output a = 2, b = 3, c = 5, d = 7
        """
        t1 = sum([board[0], board[2], board[6], board[8]])
        t2 = sum([board[1], board[3], board[5], board[7]])

        if board[4]:
            if t1 == 2:
                return 3  ### TTF FTF TFF or TFF FTT TFF
            elif t1 == 1:
                boardnp = np.array([board[0:3], board[3:6], board[6:9]])
                posnp = np.argwhere(boardnp == True)
                trueDis = []
                for i in range(0,3):
                    for j in range(i+1,4):
                        trueDis.append(util.manhattanDistance(posnp[i], posnp[j]))
                totalDis = sum(trueDis)
                if totalDis == 8:
                    return 2 ### TTF TTF FFF
                else:
                    return 3 ### TTF FTT FFF or TFF FTT FTF
        elif t1 == 0 or t1 == 4:
            return 2  ### TFT FFF TFT or FTF TFT FTF
        elif t1 == 3:
            return 3  ### TTF FFF TFT
        elif t2 == 3:
            boardnp = np.array([board[0:3], board[3:6], board[6:9]])
            posnp = np.argwhere(boardnp == True)
            trueDis = []
            for i in range(0, 3):
                for j in range(i + 1, 4):
                    trueDis.append(util.manhattanDistance(posnp[i], posnp[j]))
            totalDis = sum(trueDis)
            if totalDis == 11:
                return 2 ### TTF TFT FFF
            elif totalDis == 13:
                return 6 ### TTF FFT FTF
            else:
                print("Warning! There is an error!!! Four-t2==3")
        elif (board[0] and board[2]) or (board[0] and board[6]) or (board[8] and board[2]) or (board[8] and board[6]):
            return 3 ### TTF FFT TFF or TTF FFF TTF
        else:
            if (board[0] and board[8]):
                if (board[1] and board[3]) or (board[5] and board[7]):
                    return 2  ### TTF TFF FFT
                elif (board[1] and board[5]) or (board[3] and board[7]):
                    return 6  ### TTF FFT FFT
                elif (board[1] and board[7]) or (board[3] and board[5]):
                    return 2  ### TTF FFF FTT
                else:
                    print("Warning! There is an error!!! Four-Difficultcase-W1")
                    return 1
            elif  (board[2] and board[6]):
                if (board[1] and board[5]) or (board[3] and board[7]):
                    return 2
                elif (board[1] and board[3]) or (board[5] and board[7]):
                    return 6
                elif (board[1] and board[7]) or (board[3] and board[5]):
                    return 2
                else:
                    print("Warning! There is an error!!! Four-Difficultcase-W2")
                    return 1
            else:
                print("Warning! There is an error!!! Four-Generalcase")
                print(board)
                return 1

    def FingerprintFIVE(self,board):
        """
                   Check a board contains Four TRUE
                   Output a = 2, b = 3, c = 5, d = 7
               """
        t1 = sum([board[0], board[2], board[6], board[8]])
        t2 = sum([board[1], board[3], board[5], board[7]])
        if board[4]:
            return 2
        elif t1 == 3:
            return 2
        elif t2 == 3:
            if (board[0] and board[8]) or (board[2] and board[6]):
                return 3
            else:
                return 2
        elif t2 == 4:
            return 3
        else:
            print("Warning! There is an error!!! Five-Generalcase")
            print(board)
            return 1

    def FingerprintSIX(self,board):
        return 2

    def FingerprintZERO(self,board):
        return 5

class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat 
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the 
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8. 

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.
      
      However, please don't modify the name and input parameters of the function getAction(), 
      because autograder will call this function to check your algorithm.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}

    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        bestAction = random.choice(actions)
        #print(gameState.boards)
        for action in actions:
            fgpMult = 1
            successor = gameState.generateSuccessor(action)
            boards = successor.boards
            for board in boards:
                if not gameRules.deadTest(board):
                    num = sum(board)
                    if num == 1:
                        fgp = gameRules.FingerprintONE(board)
                    elif num == 2:
                        fgp = gameRules.FingerprintTWO(board)
                    elif num == 3:
                        fgp = gameRules.FingerprintTHREE(board)
                    elif num == 4:
                        fgp = gameRules.FingerprintFOUR(board)
                    elif num == 5:
                        fgp = gameRules.FingerprintFIVE(board)
                    elif num == 6:
                        fgp = gameRules.FingerprintSIX(board)
                    elif num == 0:
                        fgp = gameRules.FingerprintZERO(board)
                    else:
                        print("ERROR!")
                else:
                    fgp = 1
                fgpMult = fgpMult * fgp
            if fgpMult == 2 or fgpMult == 15 or fgpMult == 9 or fgpMult == 25:
                bestAction = action
                #print(fgpMult)
                #print("10")
                break
        #print("20")
        #print(gameState.boards)
        #print(gameState.generateSuccessor(bestAction).boards)
        return bestAction
        util.raiseNotDefined()


class randomAgent():
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two 
      random agents fight with each other.
    """
    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)


class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """
    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):
        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action 

class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """
    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        self.numOfGames  = numOfGames
        self.muteOutput  = muteOutput
        self.maxTimeOut  = 30 

        self.AIforHuman  = AIforHuman
        self.gameRules   = GameRules()
        self.AIPlayer    = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()
        if AIforHuman:
            self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = keyboardAgent()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        numOfWins = 0;
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0: 
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex  = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i+1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i+1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    #random.seed(1)  
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()
