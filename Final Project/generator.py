# Algorithms that control the game logic are written in this file. 

from random import shuffle, randint


def check(i, j, board):
    for a in range(9):
        if board[i][a] == board[i][j] and a != j:
            return False
    
    for a in range(9):
        if board[a][j] == board[i][j] and a != i:
            return False
    
    for a in range(i-i%3, i-i%3+3):
        for b in range(j-j%3, j-j%3+3):
            if board[a][b] == board[i][j] and a != i and b != j:
                return False
    
    return True    

board = []
status = [False]


def dfs(col, row):
    for i in range(1, 10):
        board[col][row] = i
        if check(col, row, board):
            if row == 8 and col == 8:
                status[0] = True
            
            elif row == 8:
                dfs(col+1, 0)
            
            else:
                dfs(col, row+1)
            
            if status[0]:
                break

        board[col][row] = 0


def player_board(board, diff):
    rand = 0
    zeroes = 0
    for i in range(9):
        for j in range(9):
            match diff:
                case 1:
                    rand = randint(1,12)
                case 2: 
                    rand = randint(1,2)
            
            if rand == 1 and diff == 2 or rand in range(1,6) and diff == 1:
                board[i][j] = 0
                zeroes += 1
    
    if diff == 1 and zeroes > 33 or diff == 2 and zeroes > 64:
        return
    
    return board


def main():
    srow = [i for i in range(1, 10)]
    shuffle(srow)
    board.append(srow)

    for i in range(8):
        board.append([0 for i in range(9)])
    
    dfs(1, 0)
    return board




