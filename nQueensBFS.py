'''
Created on Sep 15, 2017
@author: ishank mishra

~ The objective is to place a certain number of queens on N x N grid/board. 
~ The board also has pawns. Positions of pawns specified in the input.
~ The pawns are non attacking.
~ The Pawns prevent queens from attacking each other, if placed in between them.

~ The input to this program is as follows:

    First Line:     The algorithm to be used for search. In this program, BFS.
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

# The search states are stored in a queue using a linked list
# A state is removed from the front, and, is expanded by appending the next child (queen position) to the end
class ListNode(object):
    def __init__(self, x):
        self.val = x        # Stores positions of queens in a state, separated by "-"
        self.next = None    # Points to the next state in the queue  
         
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

def nQueensBFS(n, board, s, finalBoard):
    # q: Number of queens to be placed
    # board: Intermediate N x N grid with 0 or more queens already placed. 
    # n: Represents the size of the board. N x N grid.
    # finalBoard: Used to store the board positions once a solution is found.
    
    # nodeLevel: Contains level:indexes, available free locations (with value 0) at each level    
    nodeLevels = calNodeLevels(board, s)
    # Number of levels (horizontally contiguous positions where a queen can be placed)
    level = len(nodeLevels)
    
    #Heuristic: Number of queens to be placed cannot be greater than number of levels
    if n > level: 
        return False
    
    # Heuristic: Number of free segments i.e. segments without queen placements, should be at least 0.
    freeSegAllowed = level - n
    
    # startNode points to the front of the queue. Initialized with a dummy value.
    startNode = ListNode("0")
    startNode.next = None
    
    # points to the end of the queue
    last = startNode
    
    # Add to queue all the locations where the first queen can be placed
    for k in range(freeSegAllowed + 1):           
        for i in nodeLevels[k]:
            newNode = ListNode(str(i))
            newNode.next = None
            last.next = newNode
            last = last.next
    # Since the start node is holding a dummy value
    startNode = startNode.next
    
    while startNode != None:
#         print(startNode.val)
        
        # Retrieve the positions of queens 
        nodes = startNode.val.split("-")
        # nodeIndexList: Stores the positions of the queens in integer
        nodeIndexList = [int(j) for j in nodes]
        
        # tempBoard: used to place queen positions on the board
        tempBoard = list(board)
        
        # Block the board with current queen positions
        for i in nodeIndexList:
            tempBoard[i] = 1
            blockBoard(i, tempBoard, s)
        
        
        # if only one queen has to be placed, then the solution is found
        if n == 1:
            for i in range(len(finalBoard)):                
                if tempBoard[i] != 3:
                    finalBoard[i] = tempBoard[i] 
            return True
        
        # lenNodeIndexList: Number of queens already placed
        lenNodeIndexList = len(nodeIndexList)
        
        # Number of queens already placed cannot be greater than number of levels
        if lenNodeIndexList < level: 
            # At each state, the levels that can contain a possible child state is bounded by number of free segments allowed
            for k in range(freeSegAllowed + 1):
                # Add to the queue, a new state for every possible child state
                for i in nodeLevels[lenNodeIndexList + k]:
                    
                    # Find the next valid position to place the queen
                    if tempBoard[i] == 0:
                        tempBoard[i] = 1
                    
                        # Solution Found
                        if lenNodeIndexList == (n - 1):                                           
                            for j in range(len(tempBoard)):
                                if tempBoard[j] != 3:
                                    finalBoard[j] = tempBoard[j] 
                            return True
                        
                        # Create a new state by appending the newly found position to current state
                        newNode = ListNode(startNode.val)
                        newNode.val = newNode.val + "-" + str(i)
                        
                        # Add this new state to the end of the queue
                        last.next = newNode
                        last = last.next
                        
            # This particular state is no longer required in the queue because 
            #     all its possible child states are now in the queue            
            startNode = startNode.next
    
    # If this point is reached no solution is possible at all
    return False
    
def main():
    
    board = [] # Stores the starting board position
    finalBoard = board # Used to store the final result, if found later.
    
    ipFile = open("input.txt")
    opFile = open("output.txt","w")
    
    _algoType = ipFile.readline() # Runs BFS irrespective of which algorithm is specified in the input
    boardSize = int(ipFile.readline())
    lizards = int(ipFile.readline())
    
    # Read the input file to obtain the starting board position
    for i in range(boardSize):
            
        line = ipFile.readline()
        arrLine = list(line.rstrip())
        
        for j in range(boardSize):
            board.append(int(arrLine[j]))
    
    t0 = time()
    
    result = nQueensBFS(lizards, board, boardSize, finalBoard)
   
    t1 = time()
    
    print(result)
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
    
    print(t1 - t0)
    printBoard(finalBoard, boardSize)
    
if __name__ == "__main__":
    main()
