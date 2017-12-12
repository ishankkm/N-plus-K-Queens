'''
Created on Sep 15, 2017
@author: ishank mishra

~ The objective is to place a certain number of queens on N x N grid/board. 
~ The board also has pawns. Positions of pawns specified in the input.
~ The pawns are non attacking.
~ The Pawns prevent queens from attacking each other, if placed in between them.

~ The input to this program is as follows:

    First Line:     The algorithm to be used for search. In this program, DFS(Recursive).
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

#  Use Depth First Search to place the queens on the board.
#  DFS is implemented using recursion.
def nQueensDFS(q, board, n, k, finalBoard):
    # q: Number of queens to be placed
    # board: Intermediate N x N grid with 0 or more queens already placed. 
    # n: Represents the size of the board. N x N grid.
    # k: Placement of the previous queen.
    # finalBoard: Used to store the board positions once a solution is found.
    
    # Create a copy of current board position, to remember the state when backtracking
    tempBoard = list(board)
    
    
    if q == 0:  # No more queens to be placed. Solution is found.
        for i in range(len(board)):
            if tempBoard[i] != 3:   # Output should not contain 3.  
                finalBoard[i] = tempBoard[i] 
        return True 
    
    if k > -1: 
        # Block the board positions that are under attack by previous queen
        blockBoard(k, tempBoard, n)
     
    # Find the next valid position (with value 0) to place the queen.
    # (q - 1)*2 : Heuristic that suggests that q queens can not be placed in last (q - 1)*2 positions
    for i in range( k + 1, len(tempBoard) - (q - 1)*2):
        
        if tempBoard[i] == 0: # A valid position has been found
                   
            tempBoard[i] = 1 # Place the queen in the position
            if nQueensDFS(q - 1, tempBoard, n, i, finalBoard) == False:
                # No solution is found in further recursions  
                tempBoard[i] = 0 # REmove the queen from the position
                continue # Check next position             
            else:
                # Solution exists in further recursions
                return True
    # If reached here means that no solution is possible in current state. Backtrack.
    return False  

def main():
    board = []  # Stores the starting board position
    finalBoard = board  # Used to store the final result, if found later.
    
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
    
    # Here k = -1, since no queen has been place in the start
    result = nQueensDFS(numQueens, board, boardSize, -1, finalBoard)
    
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
    
    printBoard(finalBoard, boardSize)  
    ipFile.close()
    opFile.close()
    
    print(t1 - t0)
    
if __name__ == "__main__":
    main()
