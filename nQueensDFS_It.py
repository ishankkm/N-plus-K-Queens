'''
Created on Sep 17, 2017
@author: ishank mishra

~ The objective is to place a certain number of queens on N x N grid/board. 
~ The board also has pawns. Positions of pawns specified in the input.
~ The pawns are non attacking.
~ The Pawns prevent queens from attacking each other, if placed in between them.

~ The input to this program is as follows:

    First Line:     The algorithm to be used for search. In this program, DFS(Iterative).
    Second Line:    Height and Width of the grid/board. An integer N indicates N x N grid/board.
    Third Line:     Number of Queens to be placed. 
    Next N Lines:   The N x N grid, which can contain the following numbers
                        0: Free i.e a queen can be placed here
                        1: Queen
                        2: Pawn
                        3: Under Attack- i.e a queen cannot be placed here. Used in intermediate steps only   

~ The output is as defined:
    
    First Line:    OK:     If it is possible to place the specified number of Queens
                   FAIL:   Otherwise
    
    Next N Lines:  The placement of Queens on the board. 
    
Note:   This implementation uses a 1D array to represent a board of size N x N.
'''  

from __future__ import print_function
from time import time

def printBoard(board, n):        
    for i in range(0,n):
        for j in range(0,n):
            print(board[i * n + j],end=" ")        
        print("")
        
# Move vertically, horizontally, and diagonally on the board until an end is reached or a pawn is encountered.
# Block the board positions that are under attack by setting the value to 3.
def blockBoard(pos, board, n):            
    # pos: Position of the queen on the board
    # n: Represents the size of the board. N x N grid.

    #Go Left
    for i in range(0, pos % n):
        if board[pos - i - 1] == 0:
            board[pos - i - 1] = 3
        elif board[pos - i - 1] == 2:
            break
            
    #Go Right
    for i in range(0, (n - 1) - (pos % n)):
        if board[pos + i + 1] == 0:
            board[pos + i + 1] = 3
        elif board[pos + i + 1] == 2:
            break
     
    #Go up  
    up = pos - n
    while up >= 0:
        if board[up] == 0:
            board[up] = 3
        elif board[up] == 2:
            break
        up -= n
             
    #Go Down
    dn = pos + n
    while dn < n*n:
        if board[dn] == 0:
            board[dn] = 3
        elif board[dn] == 2:
            break
        dn += n
     
    #Go Diagonally Left Up
    dg = pos
    while (dg % n) != 0 and dg > n:
        dg -= (n + 1)
        if board[dg] == 0:
            board[dg] = 3
        elif board[dg] == 2:
            break
              
    #Go Diagonally Right Down
    dg = pos
    while (dg % n) != (n - 1) and dg < (n*n - n - 1):
        dg += (n + 1)
        if board[dg] == 0:
            board[dg] = 3
        elif board[dg] == 2:
            break
         
    #Go Diagonally Right Up
    dg = pos
    while (dg % n) != (n - 1) and dg > (n - 1):
        if board[dg - n + 1] == 0:
            board[dg - n + 1] = 3
        elif board[dg - n + 1] == 2:
            break
        dg -= (n - 1)
     
    #Go Diagonally Left Down
    dg = pos
    while (dg % n) != 0 and dg < n * (n - 1):        
        if board[dg + (n - 1)] == 0:
            board[dg + (n - 1)] = 3
        elif board[dg + (n - 1)] == 2:
            break
        dg += (n - 1)

# A node level consists of horizontally contiguous positions where a queen can be placed.
# Heuristic: Number of node levels must be greater than or equal to number of Queens to be placed
def calNodeLevels(board, s):
    
    nodeLevels = {}     # key: Level; value: Fist available position with value 0
    indexes = []        # Set of positions with value 0
    level = 0           # Indicates the current level
    
    for i in range(s*s):
        
        if board[i]== 2 or (i % s) == 0 or i == (s*s - 1):
            
            # If this is the last position on the board
            if i == (s*s - 1) and board[i] == 0:
                indexes.append(i)
            
            
            if len(indexes) > 0:                       
                nodeLevels.update({level:indexes})
                indexes = []
                level = level + 1
                if board[i] == 0:
                    indexes.append(i)
            elif board[i] == 0:
                indexes.append(i)
                
        elif board[i] == 0:        
            indexes.append(i)
    
    return nodeLevels

#  Use Depth First Search to place the queens on the board.
#  DFS is implemented using Iteration.
def nQueensDFS(q, board, n, finalBoard):
    # q: Number of queens to be placed
    # board: Intermediate N x N grid with 0 or more queens already placed. 
    # n: Represents the size of the board. N x N grid.
    # finalBoard: Used to store the board positions once a solution is found.
    
    # nodeLevel: Contains level:indexes, available free locations (with value 0) at each level
    nodeLevels = calNodeLevels(board, n)
    # Number of levels (horizontally contiguous positions where a queen can be placed)
    level = len(nodeLevels)
    
    #Heuristic: Number of queens to be placed cannot be greater than number of levels
    if q > level: 
        return False
    
    # Heuristic: Number of free segments i.e. segments without queen placements, should be at least 0.
    freeSegAllowed = level - q
    
    # nodeStack: Stack of possible locations where the queens can be placed
    nodeStack = []
    
    # Add to nodeStack all the locations where the first queen can be placed at the current iteration
    for i in range(freeSegAllowed + 1):
        for j in nodeLevels[i]:
            nodeStack.append([j])
    
    # Start from first location in the nodeStack: This step is not really necessary. 
    # Performs better in certain test cases.
    nodeStack.reverse()
    
    # If nodeStack is empty then no location is available to place the first queen
    while nodeStack != []:
        
        # Holds the current stack of queen placements
        curNodes = nodeStack.pop()
        # Create a temporary board for backtracking
        tempBoard = list(board)
        
        # Place the queens in the current stack and block the board
        for i in curNodes:
            tempBoard[i] = 1
            blockBoard(i, tempBoard, n)
        
        # Solution Found: The last queen was placed since nodeStack is not empty
        if q == 1:
            for i in range(len(finalBoard)):                
                if tempBoard[i] != 3:
                    finalBoard[i] = tempBoard[i] 
            return True
        
        # Position where the next queen can be placed
        nextPos = -1        
        for i in range(curNodes[-1], n*n):
            if tempBoard[i] == 0:
                nextPos = i
                break
        
        # Solution Found
        if nextPos != -1 and len(curNodes) == (q-1):
            for i in range(len(finalBoard)):                
                if tempBoard[i] != 3:
                    finalBoard[i] = tempBoard[i] 
            finalBoard[nextPos] = 1
            return True
        elif nextPos == -1:
            # No location is available to place the next queen, therefore backtrack
            continue
        
        # Possible candidate nodes that can be appended to the nodeStack
        childNodes = []
        # Copy of freeSegAllowed used for backtracking         
        passFreeSeg = freeSegAllowed
        
        while True:
            
            # A queen can be placed here
            if tempBoard[nextPos] == 0:
                childNodes.append(nextPos)
              
            nextPos += 1
            
            # Next available location is not available
            if nextPos > (n*n - 1):                
                break                      
            
            # Reached the end of a segment by encountering a boundary of the board
            if (nextPos % n) == 0 and tempBoard[nextPos] != 2 and tempBoard[nextPos - 1] != 2:
                
                if passFreeSeg == 0:    # If it was must to place a queen in this segment
                    break               # Solution not possible in the current stack
                else:
                    passFreeSeg -= 1  
            
            # Reached the end of a segment by encountering a pawn
            # If the previous position had a pawn then do nothing (end of segment was already handled)
            if tempBoard[nextPos] == 2 and tempBoard[nextPos - 1] != 2:
                if passFreeSeg == 0:    # If it was must to place a queen in this segment
                    break               # Solution not possible in the current stack
                else:
                    passFreeSeg -= 1     
        
        lenChNodes = len(childNodes)
        
        # Update the nodeStack with current stack (now contains a child node)
        for k in range(lenChNodes):
            newNodes = list(curNodes)
            newNodes.append(childNodes[lenChNodes - k - 1])
            nodeStack.append(newNodes)
    
    # If this point is reached no solution is possible at all            
    return False  

def main():
    board = [] # Stores the starting board position
    finalBoard = board # Used to store the final result, if found later.
    
    ipFile = open("input.txt")
    opFile = open("output.txt","w")
    
    _algoType = ipFile.readline() # Runs DFS irrespective of which algorithm is specified in the input
    boardSize = int(ipFile.readline())
    numQueens = int(ipFile.readline())
    
    # Read the input file to obtain the starting board position
    for i in range(boardSize):
            
        line = ipFile.readline()
        arrLine = list(line.rstrip())
        
        for j in range(boardSize):
            board.append(int(arrLine[j]))
    
    
    t0 = time()
    
    result = nQueensDFS(numQueens, board, boardSize, finalBoard)
    print(result)
    
    t1 = time()
    
    # Handling the final result
    if result == True:
        opFile.write("OK\n")
        for i in range(0,boardSize):
            for j in range(0,boardSize):
                opFile.write(str(finalBoard[i * boardSize + j]))        
            opFile.write("\n")
    else:
        opFile.write("FAIL")
    ipFile.close()
    opFile.close()
    
    printBoard(finalBoard, boardSize)
    print(t1 - t0)
    
if __name__ == '__main__':
    main()
