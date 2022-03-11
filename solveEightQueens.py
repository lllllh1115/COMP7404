import random
import copy
from optparse import OptionParser
import util

################################
### I did write something in ###
###    bfs in search.py .    ###
###     Plz look at it.      ###
###    Regards, Lian Huan    ###
################################

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board  ### Replaced by newBoards.
        oldBoard = board  ### The originall Board.
        i = 0

        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()

            i += 1
            ### We will come back to the previous step once we get stuck in a local best solution.
            ### We have the old chest board, and we will return another better board's squareArray
            ### and skip the search newRow, newCol.

            if (currentNumberOfAttacks <= newNumberOfAttacks and i >= 100) or newNumberOfAttacks == 0:
                break
            else:
                oldBoardOtherNewBoard = oldBoard.checkNumOfBetterPosition(minNumOfAttack=newNumberOfAttacks,
                                                                          newRow=newRow, newCol=newCol)
                oldBoardOtherNewBoardPairs = oldBoardOtherNewBoard[0]
                counter = oldBoardOtherNewBoard[1]

                if counter > 0:
                    for pairs in oldBoardOtherNewBoardPairs:
                        newOtherRow = pairs[0]
                        newOtherCol = pairs[1]
                        newOtherBoard = Board(squareArray=
                                              oldBoard.changeBoardArray(newRow=newOtherRow, newCol=newOtherCol))
                        (newOtherBoard, newOtherNumberOfAttacks, irRow, irCol) = newOtherBoard.getBetterBoard()
                        if newOtherNumberOfAttacks < newNumberOfAttacks:
                            newBoard = newOtherBoard
                            newNumberOfAttacks = newOtherNumberOfAttacks
                        else:
                            continue

        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            #Rare Situation Added?
                            #if testboard.squareArray[r][c]+testboard[rr][c] == 1:
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        position = self.squareArray
        oldBoard = self.getCostBoard()
        oldBoardArray = oldBoard.squareArray
        Attack0 = self.getNumberOfAttacks()
        currentAttack = Attack0
        newRow = 0
        newCol = random.randint(0,7)
        ### A randomized newCol, to help the chess not get stuck in the worst place.
        rowcolSwitch = 0
        ### Find the minimum attack ,and newRow, newCol
        for r in range(0,8):
            for c in range(0,8):
                if oldBoardArray[r][c] == "q":
                    ### Though there is not supposed to be a queen here.
                    print("Warning: There is a queen!")
                    continue
                elif oldBoardArray[r][c] < currentAttack:
                    currentAttack = oldBoardArray[r][c]
                    newRow = r
                    newCol = c
                    rowcolSwitch += 1
        ### rowcolSwitch == 0 then will switch the random col and perhaps a larger cost now(perhaps smaller)
        ### indeed rowcolSwitch is redundant, but useful when we check the situation.

        position = self.changeBoardArray(newRow=newRow,newCol=newCol)
        betterBoard = Board(squareArray=position)

        return (betterBoard, betterBoard.getNumberOfAttacks(), newRow, newCol )

        util.raiseNotDefined()

    def checkNumOfBetterPosition(self, minNumOfAttack, newRow, newCol):
        """
        This Function is created by Lian Huan in Sep 25th.

        If you implemented getBetterBoard, then the returned value should be used.
        perhaps it will return counter = 0, which means:
            only one place real better or
            only one place real keep the original NumOfAttack

        Returned a list with listOfPoints and a counter shows the num of pairs in listOfPoints.

        """

        oldBoardArray = self.getCostBoard().squareArray
        counter = 0
        listOfPoints = []
        if True:
            for a in range(0,8):
                for b in range(0,8):
                    if oldBoardArray[a][b] <= minNumOfAttack and (a != newRow and b != newCol):
                        counter += 1
                        listOfPoints.append((a,b))
                    else:
                        continue
        return [listOfPoints, counter]

    def changeBoardArray(self, newRow, newCol):
        """
        This Function is created by Lian Huan in Sep 25th, 2021.

        changing the BoardArray to another one, in special row and column.

        return a squareArray!!! Not a Board!!!
        """
        position = self.squareArray
        for j in range(0,8):
            if position[j][newCol] == 1:
                position[j][newCol] = 0
                position[newRow][newCol] = 1
        return position

        util.raiseNotDefined()

    def getNumberOfAttacks(self):
        """
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        counter = 0

        boardarray = self.squareArray
        #print(boardarray)
        for r in range(8):
            for c in range(8):
                if boardarray[r][c] == 1:
                    for subc in range(8):
                        for subr in range(r,8):
                            if (boardarray[subr][subc] == 1)\
                                        and ((abs(subc - c) == abs(subr - r) and (subc - c) != 0 and (subr - r != 0)) \
                                        or ((subr - r) != 0 and (subc - c) == 0)  \
                                        or ((subr - r) == 0 and (subc - c) > 0)):
                                    #print(subr, subc, r, c)
                                    counter += 1

        return counter
        util.raiseNotDefined()

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
