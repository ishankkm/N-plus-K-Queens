'''
Created on Sep 16, 2017
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
from random import choice
from random import random
import math
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


# Energy Level corresponds the number of queens attacking each other
# Two queens attacking each other is counted only once
def energyLevel(posLiz, s, board):
     
    l = len(posLiz)
    energy = 0
     
    # For each queen check the number of queens it can attack
    for i in range(l):
        
        # Block the board assuming this is the only queen on the board
        tempBoard = list(board)
        blockBoard(posLiz[i], tempBoard, s)
        
        # For every other queen with position higher than the current
        # check if their position holds he value 3
        for j in range(i+1,l):   
            if tempBoard[posLiz[j]] == 3:
                energy += 1
     
    return energy

# Accept the new state with a probability calculated by the formula e^( (Change in Energy) / Temperature )
def acceptState(delta, temp):
    # delta: Change in energy level
    # temp: Current Temperature
    
    pwr = float(delta)/float(temp)   
    prob = math.exp(pwr)
    
    # Generate a random probability
    randProb =  random()
    
    # Accept only if the random probability is greater
    if randProb < prob:
        return True
    
    return False

def nQueensSA(q, board, n, finalBoard):
    # q: Number of queens to be placed
    # board: Intermediate N x N grid with 0 or more queens already placed. 
    # n: Represents the size of the board. N x N grid.
    # finalBoard: Used to store the board positions once a solution is found.
    
    # nodeLevel: Contains level:indexes, available free locations (with value 0) at each level
    nodeLevels = calNodeLevels(board, n)
    # Number of levels (horizontally contiguous positions where a queen can be placed)
    level = len(nodeLevels)
         
    posQueens = []  # Holds the current state i.e position of each queen on the board
    
    tempBoard = list(board)
    
    #Heuristic: Number of queens to be placed cannot be greater than number of levels
    if q > level: 
        return False
    
    # Randomly place the queens on the board
    for _ in range(q):        
        while(True):
            pos = choice(range(n*n))
            if tempBoard[pos] == 0:
                tempBoard[pos] = 1
                posQueens.append(pos)
                break
    
    # Current Energy: Number of Queens attacking each other
    currentEnergy = energyLevel(posQueens, n, board)    
    print("currentEnergy: ",currentEnergy)
    
    '''
     * Temperature is decreased gradually from a starting point
     * The choice of values for starting Temperature is made by trying out different values
       and selecting one which gives best results. In this case, 10.0 turned out to be a suitable value.
     * The current temperature is decremented using the function 1 / log (x); x is Number of iterations.
     * Range of x and value of each increment step determines the number of iterations. These values are 
       calculated experimentally.
    '''
    
    # Initialize the current temperature with a value 10
    currentTemp = 10.0
    # range of x is (1.1, 120)
    x = 1.1    
    
    # Loop until Energy Level becomes 0 (Solution is found), or, Temperature hits zero, for 
    #     a certain nuber of iterations depending on x
    while currentEnergy != 0 and currentTemp > 0 and x < 120:          
        
        # Decrement temperature at each step
        currentTemp = float(1) / (math.log(x))
        
        # Choose a queen randomly
        randQueen = choice(range(len(posQueens)))
        # Choose a random position for this random queen
        randPos = choice(range(n*n))
        
        newPosLiz = list(posQueens)
        
        # Newly chosen position should be free
        if tempBoard[randPos] == 0:
            
            # Assign the new position to the randomly selected queen   
            newPosLiz[randQueen] = randPos
            
            # Calculate the new energy            
            newEnergy = energyLevel(newPosLiz, n, board)
            
            # if the new energy is less than current energy accept right away
            if newEnergy < currentEnergy:
                tempBoard[randPos] = 1
                tempBoard[posQueens[randQueen]] = 0
                posQueens[randQueen] = randPos 
                currentEnergy = newEnergy  
            # Otherwise accept with a probability
            elif newEnergy >= currentEnergy:
                # Call method which determines whether or not the new state should be accepted
                if acceptState(currentEnergy - newEnergy, currentTemp):
                    tempBoard[randPos] = 1
                    tempBoard[posQueens[randQueen]] = 0
                    posQueens[randQueen] = randPos 
                    currentEnergy = newEnergy 
        
        # Increment x at each step
        x += 0.0002
            
    print("NewEnergy: ",currentEnergy)
    print("currentTemp: ",currentTemp)
    
    # Solution Found
    if currentEnergy == 0:
        for j in range(len(tempBoard)):
            if tempBoard[j] != 3:
                finalBoard[j] = tempBoard[j]
        return True
    
    return False

def main():
    
    board = [] # Stores the starting board position
    finalBoard = board # Used to store the final result, if found later.
    
    ipFile = open("input.txt")
    opFile = open("output.txt","w")
    
    _algoType = ipFile.readline() # Runs Simulated Annealing irrespective of which algorithm is specified in the input
    boardSize = int(ipFile.readline())
    numQueens = int(ipFile.readline())
    
    # Read the input file to obtain the starting board position
    for i in range(boardSize):
            
        line = ipFile.readline()
        arrLine = list(line.rstrip())
        
        for j in range(boardSize):
            board.append(int(arrLine[j]))
    
    t0 = time()
    result = nQueensSA(numQueens, board, boardSize, finalBoard) 
    t1 = time()
    
    print(result)
    print(t1 - t0)    
    
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

if __name__ == "__main__":
    main()

