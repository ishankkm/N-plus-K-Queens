'''
Created on Sep 15, 2017

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

result = nQueensDFS(lizards, board,boardSize,-1)

t1 = time()

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

t2 = time()
print(t1 - t0)