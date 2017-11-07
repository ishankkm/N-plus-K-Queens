'''
Created on Sep 17, 2017

@author: ishan
'''
from __future__ import print_function
from time import time
from random import choice
from random import random
import math

# 0: Free
# 1: Queen
# 2: Tree
# 3: Under Attack  

class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None 

def printBoard(board, n):        
    for i in range(0,n):
        for j in range(0,n):
            print(board[i * n + j],end="")        
        print("")

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


# main calls

def nQueensBFS(n, board, s):
    
    nodeLevels = calNodeLevels(board, s)
    level = len(nodeLevels)
    
    if n > level: 
        return False
    
    freeSegAllowed = level - n
     
    startNode = ListNode("0")
    startNode.next = None
    
    last = startNode
        
    for k in range(freeSegAllowed + 1):           
        for i in nodeLevels[k]:
            newNode = ListNode(str(i))
            newNode.next = None
            last.next = newNode
            last = last.next
            
    startNode = startNode.next
    
    while startNode != None:
#         print(startNode.val)
        
        nodes = startNode.val.split("-")
        nodeIndexList = [int(j) for j in nodes]
                
        tempBoard = list(board)
        
        for i in nodeIndexList:
            tempBoard[i] = 1
            blockBoard(i, tempBoard, s)
        
        if n == 1:
            for i in range(len(finalBoard)):                
                if tempBoard[i] != 3:
                    finalBoard[i] = tempBoard[i] 
            return True
            
        lenNodeIndexList = len(nodeIndexList)
        
        if lenNodeIndexList < level: 
            for k in range(freeSegAllowed + 1):
                for i in nodeLevels[lenNodeIndexList + k]:
                    if tempBoard[i] == 0:
                        tempBoard[i] = 1
                        
                        if lenNodeIndexList == (n - 1):                                           
                            for j in range(len(tempBoard)):
                                if tempBoard[j] != 3:
                                    finalBoard[j] = tempBoard[j] 
                            return True
                        
                        newNode = ListNode(startNode.val)
                        newNode.val = newNode.val + "-" + str(i)
                        
                        last.next = newNode
                        last = last.next
            startNode = startNode.next
        
    return False
  
def nQueensDFS_Iterative(n, board, s):
    
    nodeLevels = calNodeLevels(board, s)
    level = len(nodeLevels)
    
    if n > level: 
        return False
    
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
                   
    return False  

def nQueensSA(n, board, s):
    
    nodeLevels = calNodeLevels(board, s)
    level = len(nodeLevels)
            
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
#     print("currentEnergy: ",currentEnergy)
    
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
        
#         currentTemp = float(1) / (math.log(x))
        x += 0.0002
            
#     print("NewEnergy: ",currentEnergy)
#     print("currentTemp: ",currentTemp)
    
    if currentEnergy == 0:
        for j in range(len(tempBoard)):
            if tempBoard[j] != 3:
                finalBoard[j] = tempBoard[j]
        return True
    
#     if n <= 10:
#         if nQueensDFS(n, board, s, -1) == True:
#             print(" || ")
#             return True
    
    return False

def nQueensDFS(n, board, s, k):
    
    tempBoard = list(board)
    
    if n == 0:
        for i in range(len(board)):
            if tempBoard[i] != 3:
                finalBoard[i] = tempBoard[i] 
        return True 
        
    if k > -1: 
        blockBoard(k, tempBoard, s)
        
    for i in range( k + 1, len(tempBoard) - (n - 1)*2):
        
        if tempBoard[i] == 0:
            
            tempBoard[i] = 1
            if nQueensDFS(n - 1, tempBoard, s, i) == False:  
                tempBoard[i] = 0
                continue             
            else:
                return True
    return False  

boardSize = 8
numQueen = 9
numTrees = 2

numIter = 300
success = 0

finalBoard = [0]*(boardSize*boardSize)
solutions = 0
avgTime = 0.0

for i in range(numIter):
    
    finalBoard = [0]*(boardSize*boardSize)
    
    board = [0]*(boardSize*boardSize)
    nt = numTrees
#     while nt != 0:    
#         pos = choice(range(boardSize*boardSize))
#         if board[pos] == 0:
#             board[pos] = 2
#             nt -= 1
    board[6] = 2
    board[32] = 2
#     printBoard(board, boardSize)
    t1 = time()
    result = nQueensSA(numQueen, board, boardSize)
    t2 = time() 
    
    if result:
        success += 1
        solutions += 1
        
        posLiz = []
        for j in range(boardSize*boardSize):
            if finalBoard[j] == 1:
                posLiz.append(j)
        energy = energyLevel(posLiz, boardSize, board)
        if energy > 0:
            printBoard(finalBoard, boardSize)
            print("Fail")
            break
        print("Success: ",float(success)/float(i+1)*100," | ",i+1," | ",t2-t1," | ")
        
    else:        
        
        dfsRes = nQueensDFS_Iterative(numQueen, board, boardSize)
        if dfsRes == False:
            success += 1
            print("Success: ",float(success)/float(i+1)*100," | ",i+1," | ",t2-t1)
#             avgTime += (t2-t1)
        else: 
#             printBoard(board, boardSize)
            print("Fail: ",float(success)/float(i+1)*100," | ",i+1," | ",t2-t1)
#             time += (t2-t1)
#         print("Fail: ",float(success)/float(i+1)*100," | ",i+1," | ",t2-t1)
    avgTime += (t2-t1)
#         print("")
         
#     if (t2-t1) > 0.5:
#         printBoard(board, boardSize)
#         print("")
#         print(t2-t1) 
#         break
#     print(t2-t1) 
    

print("Number of test cases passed : ",success)
print("Number of solutions possible: ",solutions)
print("Average Running Time: ", avgTime/numIter)

