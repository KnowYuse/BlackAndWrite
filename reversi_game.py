import time
import os

direction = ((-1, -1), (-1, 0), (-1, 1), # NW, N, NE
            (0, -1), (0, 1), # W, E
            (1, -1), (1, 0), (1, 1)) # SW, S, SE

def init_board(n):
    """
    :param n: 棋盘的维度, n * n
    :return: 初始化好的棋盘矩阵，以列表的列表的形式
    """
    board = []
    tmp = [chr(0)]
    for i in range(n):
        tmp.append(chr(97+i))
    board.append(tmp)
    for i in range(n):
        tmp = [chr(97+i)]
        for j in range(n):
            tmp.append('.')
        board.append(tmp)
    board[n//2][n//2] = board[n//2+1][n//2+1] = 'O'
    board[n//2][n//2+1] = board[n//2+1][n//2] = 'X'
    return board


def print_board(board):
    """
    :param board: 棋盘矩阵
    :return: None
    打印棋盘，包括第一行和第一列
    """
    n = len(board)
    for i in range(n):
        for j in range(n):
            print(board[i][j], end=" ")
        print()


def computer_move(board, color):
    """
    :param board  当前棋盘
    :param color: 计算机方的颜色
    计算机选择合适的位置下棋，更新board
    """
    row = col = score = 0
    n = len(board)
    for i in range(1, n):
        for j in range(1, n):
            if board[i][j] == '.':
                s = len(position_score(board, i, j, color))
                if s > score:
                    score = s
                    row = i
                    col = j
    if row == 0:
        print(color + " player has no valid move.")
        return
    print("Computer places "+color+" at "+chr(row+96)+chr(col+96)+".")
    flip(board, row, col, color)
    print_board(board)


def human_move(board, color):
    """
    :param board  当前棋盘
    :param color: 用户方的颜色
    :return True/False
    询问用户下棋的位置，翻转棋盘，更新board
    """
    n = len(board)
    for i in range(1,n):
        for j in range(1,n):
            if check_legal_move(board, i, j, color):
                break
        else:
            continue
        break
    else:
        print(color + " player has no valid move.")
        return
    pos = input("Enter move for "+color+"(RowCol):")
    row = int(ord(pos[0]) - 96)
    col = int(ord(pos[1]) - 96)
    if check_legal_move(board, row, col, color):
        flip(board, row, col, color)
        print_board(board)
        return True
    else:
        print("Invalid move.")
        return False


def gameover(isInvalidInput, color, res):
    """
    :param isInvalidInput 是否为无效输入
    :param color 用户方颜色
    :param res  游戏结果
    游戏结束，将游戏的结果附加到指定的文件
    """
    print("Game over.")
    if isInvalidInput:
        winner = color
    else:
        X_num = res[0]
        O_num = res[1]
        print("X : O = "+str(X_num)+" : "+str(O_num))
        if X_num > O_num:
            winner = 'X'
        elif X_num < O_num:
            winner = 'O'
        else:
            print("Draw!")
            return
    print(winner+" player wins.")


def saveinfo(startTime, endTime, color, dimension, res, isinValidInput):
    """
    :param startTime 游戏开始时间
    :param endTime 游戏结束时间
    :param color 用户方颜色
    :param dimension 棋盘大小
    :param res 游戏结果
    :ininValidInput 是否为合法输入
    保存游戏结果，包括：游戏开始的时间、单次游戏使用的时间、棋盘大小、黑棋玩家、白棋玩家、游戏比分
    """
    file = open("reversi.csv", 'a')
    dimension = str(dimension)
    content = str(time.strftime("%Y%m%d %H:%M:%S", time.localtime(startTime))) \
              + ',' + str(int(endTime - startTime)) \
              + ',' + dimension + '*' + dimension + ','
    if color == 'X':
        content += 'computer,'
        content += 'human,'
    else:
        content += 'human,'
        content += 'computer,'
    if isinValidInput:
        content += "Human gave up."
    else:
        content += str(res[0]) + " to " + str(res[1])
    content += '\n'
    file.write(content)
    file.close()


def check_board(board):
    """
    :param board  当前棋盘
    :return: 已经分出结果时，返回游戏的比分(白色棋子和黑色棋子)，否则返回None
    检查游戏是否结束
    """
    n = len(board)-1
    legal_X = num_X = legal_O = num_O = 0
    for i in range(1, n+1):
        for j in range(1, n+1):
            if board[i][j] == 'O':
                num_O += 1
            elif board[i][j] == 'X':
                num_X += 1
            else:
                if len(position_score(board, i, j, 'X')) != 0:
                    legal_X += 1
                if len(position_score(board, i, j, 'O')) != 0:
                    legal_O += 1
    if num_X+num_O==n*n or num_X==0 or num_O==0 or legal_O+legal_X==0:
        return [num_X, num_O]
    else:
        return None


def check_legal_move(board, row, col, color):
    """
    :param board  当前棋盘
    :param row, col:  行和列
    :Param color      哪一方在下棋
    :return True/False
    当前一方下在row,col位置是否为合法的位置
    """
    if board[row][col] != '.':
        return False
    if len(position_score(board, row, col, color)) == 0:
        return False
    return True


def flip(board, row, col, color):
    """
    :param board  当前棋盘
    :param row, col:  行和列
    :Param color      哪一方在下棋
    当前一方下在row,col位置时，翻转黑白棋
    """
    row = int(row)
    col = int(col)
    board[row][col] = color
    pos = position_score(board, row, col, color)
    for i in range(len(pos)):
        board[pos[i][0]][pos[i][1]] = color


def position_score(board, row, col, color):
    """
    :param board  当前棋盘
    :param row, col:  行和列
    :Param color      哪一方在下棋
    :return True/False
    计算机下在row,col位置时，可以翻转的黑白棋的个数
    """
    score = []
    if color == 'X':
        c = 'O'
    else:
        c = 'X'
    n = len(board)
    for i in range(8):
        j = 1
        while True:
            pos_i = row + direction[i][0]*j
            pos_j = col + direction[i][1]*j
            if 0 < pos_i < n and 0 < pos_j < n:
                if board[pos_i][pos_j] == '.':
                    break;
                elif board[pos_i][pos_j] == c:
                    j += 1
                    continue
                else:
                    for k in range(1, j):
                        score.append([row + direction[i][0]*k, col + direction[i][1]*k])
                    break
            else:
                break
    return score

def black_white_game():
    """ 初步流程
    1. 询问用户棋盘大小，保证用户输入的为[4,26]之间的整数

    2. 询问用户:计算机选择黑棋(X)还是白棋(O)，黑棋方首先下棋

    3. 初始化棋盘 init_board()

    4. loop forever:
        打印棋盘 print_board()

       if 轮到用户下棋： human_move(board, color)
           检查是否有位置可下，遍历所有的位置检查该位置是否可下(调用check_legal_move)，如果无位置，则本轮放弃
           询问用户下棋的位置
           检查用户下的位置是否合法（是否越界，是否满足下棋规则）
           翻转敌方的棋子
       else # 轮到计算机下棋 computer_move(board, color)
           确定计算机可以下棋的位置, 如果无位置，则本轮放弃
           计算这些位置的得分
           选择得分最高的位置下棋
           翻转敌方的棋子
        检查是否已经分出输赢
        如果已经分出输赢：
            保存游戏数据
            break

    """
    n = int(input("Enter the board dimension:"))
    while n>26 or n<4 or n%2:
        print("Wrong Number!")
        n = input("Enter the board dimension: ")
    c_ch = input("Computer plays(X/O): ")
    start = time.time()
    board = init_board(n)
    print_board(board)
    if c_ch == 'X':
        p_ch = 'O'
        computer_move(board, c_ch)
    else:
        p_ch = 'X'
    isInValidInput = False
    while True:
        if check_board(board) is None:
            if human_move(board, p_ch):
                pass
            else:
                isInValidInput = True
                break
        if check_board(board) is None:
            computer_move(board, c_ch)
        else:
            break
    end = time.time()
    res = check_board(board)
    if not isInValidInput:
        print("Both players have no valid move.")
    gameover(isInValidInput, c_ch, res)
    saveinfo(start, end, c_ch, n, res, isInValidInput)


def main():
    black_white_game()


if __name__ == '__main__':
    main()