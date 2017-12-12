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

# A node level consists of horizontally contiguous positions that are not under attack (value 0).
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
def nQueensDFS(n, board, s):
    
    nodeLevels = calNodeLevels(board, s)
    level = len(nodeLevels)
    
    freeSegAllowed = level - n
    
    nodeStack = []
    
    for i in range(freeSegAllowed + 1):
        for j in nodeLevels[i]:
            nodeStack.append([j])
    
    nodeStack.reverse()
    
    while nodeStack != []:
        
        curNodes = nodeStack.pop()
        tempBoard = list(board)
        
        for i in curNodes:
            tempBoard[i] = 1
            blockBoard(i, tempBoard, s)
        
        if n == 1:
            for i in range(len(finalBoard)):                
                if tempBoard[i] != 3:
                    finalBoard[i] = tempBoard[i] 
            return True
        
        nextPos = -1
        
        for i in range(curNodes[-1], s*s):
            if tempBoard[i] == 0:
                nextPos = i
                break
        
        if nextPos != -1 and len(curNodes) == (n-1):
            for i in range(len(finalBoard)):                
                if tempBoard[i] != 3:
                    finalBoard[i] = tempBoard[i] 
            finalBoard[nextPos] = 1
            return True
        elif nextPos == -1:
            continue
   
        childNodes = []
        passFreeSeg = freeSegAllowed
        while True:
                          
            if tempBoard[nextPos] == 0:
                childNodes.append(nextPos)
              
            nextPos += 1
                             
            if nextPos > (s*s - 1):                
                break                      
            
            if (nextPos % s) == 0 and tempBoard[nextPos] != 2 and tempBoard[nextPos - 1] != 2:
                if passFreeSeg == 0:
                    break
                else:
                    passFreeSeg -= 1  
            
            if tempBoard[nextPos] == 2 and tempBoard[nextPos - 1] != 2:
                if passFreeSeg == 0:
                    break
                else:
                    passFreeSeg -= 1
        
        lenChNodes = len(childNodes)
        for k in range(lenChNodes):
            newNodes = list(curNodes)
            newNodes.append(childNodes[lenChNodes - k - 1])
            nodeStack.append(newNodes)

#         print(nextPos)
                    
    return False  

board = []
finalBoard = board

ipFile = open("input.txt")
# opFile = open("output.txt","w")

algoType = ipFile.readline()
boardSize = int(ipFile.readline())
lizards = int(ipFile.readline())

for i in range(boardSize):
        
    line = ipFile.readline()
    arrLine = list(line.rstrip())
    
    for j in range(boardSize):
        board.append(int(arrLine[j]))


t0 = time()

result = nQueensDFS(lizards, board,boardSize)
print(result)

t1 = time()

# if result == True:
#     opFile.write("OK\n")
#     for i in range(0,boardSize):
#         for j in range(0,boardSize):
#             opFile.write(str(finalBoard[i * boardSize + j]))        
#         opFile.write("\n")
# else:
#     opFile.write("FAIL")
ipFile.close()
# opFile.close()

printBoard(finalBoard, boardSize)
print(t1 - t0)
