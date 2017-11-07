'''
Created on Sep 16, 2017

@author: ishan
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

def calNodeLevels(board, s):
    
    nodeLevels = {}
    indexes = []
    level = 0
    
    for i in range(s*s):
        
        if board[i]== 2 or (i % s) == 0 or i == (s*s - 1):
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

def blockBoard(n, board, s):
            
#     #Go Left
    for i in range(0, n % s):
        if board[n - i - 1] == 0: #or board[n - i - 1] == 3:
            board[n - i - 1] = 3
        elif board[n - i - 1] == 2:
            break
            
#     #Go Right
    for i in range(0, (s - 1) - (n % s)):
        if board[n + i + 1] == 0: #or board[n + i + 1] == 3:
            board[n + i + 1] = 3
        elif board[n + i + 1] == 2:
            break
#     
#     #Go up  
    up = n - s
    while up >= 0:
        if board[up] == 0: #or board[up] == 3:
            board[up] = 3
        elif board[up] == 2:
            break
        up -= s
#     
#     #Go Down
    dn = n + s
    while dn < s*s:
        if board[dn] == 0:# or board[dn] == 3:
            board[dn] = 3
        elif board[dn] == 2:
            break
        dn += s
#     
#     #Go Diagonal Left Up
    dg = n
    while (dg % s) != 0 and dg > s:
        dg -= (s + 1)
        if board[dg] == 0 :#or board[dg] == 3:
            board[dg] = 3
        elif board[dg] == 2:
            break
#         
#     
#     #Go Diagonal Right Down
    dg = n
    while (dg % s) != (s - 1) and dg < (s*s - s - 1):
        dg += (s + 1)
        if board[dg] == 0 :#or board[dg] == 3:
            board[dg] = 3
        elif board[dg] == 2:
            break
#         
#     #Go Diagonal Right Up
    dg = n
    while (dg % s) != (s - 1) and dg > (s - 1):
        if board[dg - s + 1] == 0 :#or board[dg - s + 1] == 3:
            board[dg - s + 1] = 3
        elif board[dg - s + 1] == 2:
            break
        dg -= (s - 1)
#     
#    #Go Diagonal Left Down
    dg = n
    while (dg % s) != 0 and dg < s * (s - 1):        
        if board[dg + (s - 1)] == 0 :#or board[dg + (s - 1)] == 3:
            board[dg + (s - 1)] = 3
        elif board[dg + (s - 1)] == 2:
            break
        dg += (s - 1)

def energyLevel(posLiz, s, board):
     
    l = len(posLiz)
    energy = 0
     
    for i in range(l):
        
        tempBoard = list(board)
        blockBoard(posLiz[i], tempBoard, s)
        
        for j in range(i+1,l):   
            if tempBoard[posLiz[j]] == 3:
                energy += 1
     
    return energy

def acceptState(delta, temp):
    
    pwr = float(delta)/float(temp)   
    prob = math.exp(pwr)
    
    randProb =  random()
    
    if randProb < prob:
        return True
    
    return False

def nQueensSA(n, board, s):
    
    nodeLevels = calNodeLevels(board, s)
    level = len(nodeLevels)
    
    freeSegAllowed = level - n
       
    posLiz = []
    posTrees = []
    
    tempBoard = list(board)
    
    if n > level: 
        return False
    
    for i in range(s*s):
        if board[i] == 2:
            posTrees.append(i)
    
    for i in range(n):        
        while(True):
            pos = choice(range(s*s))
            if tempBoard[pos] == 0:
                tempBoard[pos] = 1
                posLiz.append(pos)
                break
    
    currentEnergy = energyLevel(posLiz, s,board)    
    print("currentEnergy: ",currentEnergy)
    
    currentTemp = 10.0
    x = 1.1
    while currentEnergy != 0 and currentTemp > 0 and x < 120:          
        
        currentTemp = float(1) / (math.log(x))
        
        randLiz = choice(range(len(posLiz)))
        randPos = choice(range(s*s))
        
        newPosLiz = list(posLiz)
        
        if tempBoard[randPos] == 0:
               
            newPosLiz[randLiz] = randPos            
            newEnergy = energyLevel(newPosLiz, s, board)
            
            if newEnergy < currentEnergy:
                tempBoard[randPos] = 1
                tempBoard[posLiz[randLiz]] = 0
                posLiz[randLiz] = randPos 
                currentEnergy = newEnergy  

            elif newEnergy >= currentEnergy:
                if acceptState(currentEnergy - newEnergy, currentTemp):
                    tempBoard[randPos] = 1
                    tempBoard[posLiz[randLiz]] = 0
                    posLiz[randLiz] = randPos 
                    currentEnergy = newEnergy 
        
        
        x += 0.0002
            
    print("NewEnergy: ",currentEnergy)
    print("currentTemp: ",currentTemp)
    
    if currentEnergy == 0:
        for j in range(len(tempBoard)):
            if tempBoard[j] != 3:
                finalBoard[j] = tempBoard[j]
        return True
    
    
    
    return False


board = []
finalBoard = board

ipFile = open("input.txt")
opFile = open("output.txt","w")

algoType = ipFile.readline()
boardSize = int(ipFile.readline())
lizards = int(ipFile.readline())

for i in range(boardSize):
        
    line = ipFile.readline()
    arrLine = list(line.rstrip())
    
    for j in range(boardSize):
        board.append(int(arrLine[j]))

t0 = time()
print(nQueensSA(lizards, board, boardSize))
t1 = time()
print(t1 - t0)
printBoard(finalBoard, boardSize)



