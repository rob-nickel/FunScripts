# To run: python3 tictactoe.py

import sys
board = [[0 for x in range(3)]for y in range(3)]
for i in range(0,3):
    for j in range(0,3):
        board[j][i] = str(i*3+j+1)

XTurn = True

def output():
    print()
    for i in range(0,3):
        for j in range(0,3):
            if str(board[j][i]) == 'X':
                print('\033[1;32m' + 'X' + '\033[0m',end=' ')
            elif str(board[j][i]) == 'O':
                print('\033[1;34m' + 'O' + '\033[0m',end=' ')
            else:
                print(str(board[j][i]),end=" ")
            if j < 2:
                print("|", end=" ")
        print("")
        if i < 2:
            print("--+---+--")
    print()

def turn(XTurn):
    output()
    choice = 0
    if XTurn == True:
        print("X", end=" ")
    else:
        print("O", end=" ")
    print("Enter your selection")
    choice = input("")
    choiceOK = False
    while not(choice == "1" or choice == "2" or choice == "3" or choice == "4" or choice == "5" or choice == "6" or choice == "7" or choice == "8" or choice == "9"):
        choice = input("Enter a valid selection: ")
    while choiceOK == False:
        for i in range(0,3):
            for j in range(0,3):
                if choice == board[j][i]:
                    choiceOK = True
                    if XTurn == True:
                        board[j][i] = "X"
                        XTurn ^= True
                    else:
                        board[j][i] = "O"
                        XTurn ^= True
        if choiceOK == False:
            choice = input("Enter a valid selection: ")
    return(XTurn)
def XWin():
    print()
    output()
    print()
    print("X Team Wins!!!")
    sys.exit()
    
def OWin():
    print()
    output()
    print()
    print("O Team Wins!!!")
    sys.exit()

def Tie():
    print()
    output()
    print()
    print("Tie")
    sys.exit()

def checkEnd():
    if board[0][0] == "X":
        if board[1][0] == "X":
            if board[2][0] == "X":
                XWin()
        if board[1][1] == "X":
            if board[2][2] == "X":
                XWin()
        if board[0][1] == "X":
            if board[0][2] == "X":
                XWin()
    if board[1][0] =="X":
        if board[1][1] == "X":
            if board[1][2] == "X":
                XWin()
    if board[2][0] == "X":
        if board[1][1] == "X":
            if board[0][2] == "X":
                XWin()
    if board[0][1] == "X":
        if board[1][1] == "X":
            if board[2][1] == "X":
                XWin()
    if board[0][2] == "X":
        if board[1][2] == "X":
            if board[2][2] == "X":
                XWin()
    if board[1][1] == "O":
        if board[0][0] == "O":
            if board[2][2] == "O":
                OWin()
        if board[0][1] == "O":
            if board[2][1] == "O":
                OWin()
        if board[0][2] == "O":
            if board[2][0] == "O":
                OWin()
        if board[1][0] == "O":
            if board[1][2] == "O":
                OWin()
    if board[0][0] == "O":
        if board[0][1] == "O":
            if board[0][2] == "O":
                OWin()
        if board[1][0] == "O":
            if board[2][0] == "O":
                OWin()
    if board[2][2] == "O":
        if board[2][1] == "O":
            if board[2][0] == "O":
                OWin()
        if board[1][2] == "O":
            if board[0][2] == "O":
                OWin()
    
for x in range(0,9):
    XTurn = turn(XTurn)
    if x > 4:
        checkEnd()
Tie()