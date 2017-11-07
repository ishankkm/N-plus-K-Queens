'''
Created on Sep 17, 2017

@author: ishan
'''

# 0: Free
# 1: Queen
# 2: Tree
# 3: Under Attack   

from __future__ import print_function
from time import time

def printBoard(board, n):        
    for i in range(0,n):
        for j in range(0,n):
            print(board[i * n + j],end=" ")        
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

def nQueensDFS(n, board, s):
    
    nodeLevels = calNodeLevels(board, s)
    level = len(nodeLevels)
    
    freeSegAllowed = level - n
    
    nodeStack = []
#     startNodeList = []
    
    for i in range(freeSegAllowed + 1):
        for j in nodeLevels[i]:
            nodeStack.append([j])
    
    nodeStack.reverse()
#     print(nodeStack)
    
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
        
#         printBoard(tempBoard, s)
#         print("")
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