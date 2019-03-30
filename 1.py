# -*- coding: utf-8 -*-
import random

'''
*   Author: ZeroNMT
*   MSSV: 1613166
*   Version: 01:39 07/01/2018 (v2)
'''
class Node:
    def __init__(self, move = [], value = [], lstSubNode = [], board = [[]]*5, lstValue=[]):
        self.lstSubNode = lstSubNode
        self.move = move
        self.value = value
        self.lstValue = lstValue
        self.board = board

    def __str__(self):
        return self.move
    def get_lstValue(self):
        return self.lstValue  
    def set_lstSubNode(self, bonus):
        self.lstSubNode.append(bonus)
    def remove_lstSubNode(self, bonus):
        self.lstSubNode = bonus 
    def get_lstSubNode(self):
        return self.lstSubNode

    def set_move(self, move):
        self.move = move
    def get_move(self):
        return self.move

    def set_value(self, value):
        self.value = value
    def get_value(self):
        return self.value   

    def set_board(self, board):
        self.board = board
    def get_board(self):
        return self.board  


class ZeroTree:
    def __init__(self):
        self.root = Node()

    def __str__(self):
        return str(self.root)      

    def get_root(self):
        return self.root

    def set_root(self, root):
        self.root = root

    def board_copy(self,board):
        new_board = [[]]*5
        for i in range(5):
            new_board[i] = [] + board[i]
        return new_board

    def insertNode(self, nameFlag, board, highMax):
        maxValue = -1000
        for row in range(5):
            for col in range(5):    
                if board[row][col] == nameFlag:
                    moveState, isTrueMove = ZeroTree.moveState((row,col), board)  
                    for x in range(len(isTrueMove)):
                        if isTrueMove[x][1] == True:
                            move =  [(row,col),moveState[x]]
                            new_board = self.doMoveBoard(move, board)
                            value = len(self.caculationValue( moveState[x], new_board) )
                            child_board = self.board_copy(new_board)
                            lst, valueNode = self._insertNode(nameFlag, child_board, [3, highMax])
                            sumValue = value
                            for y in valueNode[0:-1]:
                                sumValue += y
                            if maxValue < sumValue:
                                maxValue = sumValue
                            self.root.set_lstSubNode(Node(move, [sumValue, value] + valueNode, lst, new_board))
        self.root.set_value(maxValue)

    def _insertNode(self, nameFlag, board, high):
        _lst = []
        _value = []                        
        if high[0]%2 != 0: #Luot di cua doi thu
            nameFlagEnymy = 'r' if nameFlag == 'b' else 'b'
            _value.append(100)
            for row in range(5):
                for col in range(5):    
                    if board[row][col] == nameFlagEnymy:
                        moveState, isTrueMove = ZeroTree.moveState((row,col), board)   
                        for x in range(len(isTrueMove)):
                            if isTrueMove[x][1] == True:
                                move = [(row,col),moveState[x]]
                                new_board = self.doMoveBoard(move, board)
                                value_ = self.caculationValue( moveState[x], new_board)
                                value = - len(value_)                                
                                if high[0] != high[1]:
                                    child_board = self.board_copy(new_board)
                                    childLst, maxValue = self._insertNode(nameFlag, child_board, [high[0] + 1, high[1]])
                                else:
                                    childLst = []
                                    maxValue = []
                                if _value[0] > value:
                                    _value = [value] + maxValue
    
                                _lst.append(Node(move, [value] + maxValue, childLst, new_board, value_))                         
            return _lst, _value                                
        else:                   #Luot di cua minh
            _value.append(-100)
            for row in range(5):
                for col in range(5):    
                    if board[row][col] == nameFlag:
                        moveState, isTrueMove = ZeroTree.moveState((row,col), board)   
                        for x in range(len(isTrueMove)):
                            if isTrueMove[x][1] == True:
                                move = [(row,col),moveState[x]]
                                new_board = self.doMoveBoard(move, board)
                                value_ = self.caculationValue( moveState[x], new_board)
                                value = len(value_)
                                if high[0] != high[1]:
                                    child_board = self.board_copy(new_board)
                                    childLst, minValue = self._insertNode(nameFlag, child_board, [high[0] + 1, high[1]])
                                else:
                                    childLst = []
                                    minValue = []                                
                                
                                if _value[0] < value:
                                    _value = [value] + minValue
                                _lst.append(Node(move, [value] + minValue, childLst, new_board, value_))                        
            return _lst, _value    


    def searchTrap(self):
        lstNode = []
        maxV = 0
        maxChild= 0
        for x in self.root.get_lstSubNode():#tang 2
            if maxChild < x.get_value()[1]:
                maxChild = x.get_value()[1]
            if x.get_value()[1] == 0:
                state = x.get_move()[1]
                for y in x.get_lstSubNode():#tang 3
                    value = y.get_value()[1] +  y.get_value()[0]
                    if y.get_value()[0] < 0 and state in y.get_lstValue() and value > 0:
                        if maxV < value:
                            maxV = value
                        lstNode.append((x, value))
        result = []
        for x in lstNode:
            if x[1] == maxV:
                result.append(x[0])
        if maxV < maxChild:
            result = []
        return result

    def searchNodeMax(self, nameFlag, isTrap, moveAgo):
        lstNode = []
        _isTrap = False

        if isTrap == True:
            minV = 100
            lst = []
            for x in self.root.get_lstSubNode():
                value = x.get_value()
                val_ = -value[2] - value[1]
                if x.get_board()[moveAgo[1][0]][moveAgo[1][1]] == nameFlag and val_ > 0 :
                    if minV > val_:
                        minV = val_
                    _isTrap = True
                    lst.append((x,val_))

            for x in lst:
                if minV == x[1]:
                    lstNode.append(x[0])

        if _isTrap == False:
            lstNode = self.searchTrap()
            if len(lstNode) == 0:
                maxValue = self.root.get_value()
                for x in self.root.get_lstSubNode():
                    if x.get_value()[0] == maxValue:
                        lstNode.append(x)

        lenLst = len(lstNode)
        if lenLst != 0:
            rand = random.randint(0,lenLst - 1)
            self.root.set_move(lstNode[rand].get_move())
            self.root.set_board(lstNode[rand].get_board())
        else:
            self.root.set_move(None)

    def doMoveBoard(self, move, board):
        new_board = [[]]*5
        for i in range(5):
            new_board[i] = [] + board[i]
      
        row_old = move[0][0]
        col_old = move[0][1]
        row_new = move[1][0]
        col_new = move[1][1]

        #change current board to new board    
        nameFlag = new_board[row_old][col_old] 
        new_board[row_old][col_old] = '.'
        new_board[row_new][col_new] = nameFlag
        return new_board

    def caculationValue(self, state, board):
        moveState, isTrueMove = ZeroTree.moveState(state, board)   

        lstTurn = ZeroTree.isTurn(moveState, isTrueMove, state, board)
        lstDE = ZeroTree.isDeadEnd(moveState, isTrueMove, state, board)
        for x in lstTurn:
            board[x[0]][x[1]] = board[state[0]][state[1]]
        for x in lstDE:
            board[x[0]][x[1]] = board[state[0]][state[1]]        
        return lstTurn + lstDE

    @staticmethod
    def moveState(state, board):
        moveSta = []
        isTrueMove = []
        row = state[0]
        col = state[1]
        Radd1 = row + 1
        Rsub1 = row - 1
        Cadd1 = col + 1
        Csub1 = col - 1       
        # 2 : (Radd1,Csub1)    (Radd1,col)      (Radd1,Cadd1)
        # 1 : (row,Csub1)       (row,col)       (row,Cadd1)
        # 0 : (Rsub1,Csub1)    (Rsub1,col)      (Rsub1,Cadd1)
        #       0                     1               2
      
        if Csub1 >= 0:
            if Radd1 <= 4:
                moveSta.append((Radd1,Csub1))
                isTrueMove.append(ZeroTree.statusLocation((Radd1, Csub1), board))
            moveSta.append((row,Csub1))
            isTrueMove.append(("yes",True) if board[row][Csub1] == "."  else ("yes",False))                
            if Rsub1 >= 0:
                moveSta.append((Rsub1,Csub1))
                isTrueMove.append(ZeroTree.statusLocation((Rsub1, Csub1), board))
        if Radd1 <= 4:
            moveSta.append((Radd1,col))
            isTrueMove.append(("yes",True) if board[Radd1][col] == "."  else ("yes",False))                
        if Rsub1 >= 0:
            moveSta.append((Rsub1,col))
            isTrueMove.append(("yes",True) if board[Rsub1][col] == "."  else ("yes",False))                
        if Cadd1 <= 4:
            if Radd1 <= 4:
                moveSta.append((Radd1,Cadd1))
                isTrueMove.append(ZeroTree.statusLocation((Radd1, Cadd1), board))
            moveSta.append((row,Cadd1))
            isTrueMove.append(("yes",True) if board[row][Cadd1] == "."  else ("yes",False))                
            if Rsub1 >= 0:
                moveSta.append((Rsub1,Cadd1))
                isTrueMove.append(ZeroTree.statusLocation((Rsub1, Cadd1), board))
        return moveSta, isTrueMove

    @staticmethod
    def statusLocation(state, board):
        noStreet = [      (0,1),      (0,3), 
                    (1,0),      (1,2),      (1,4),
                          (2,1),      (2,3),
                    (3,0),      (3,2),      (3,4),
                          (4,1),      (4,3)]          
        if (state[0], state[1]) in noStreet:
            return ("no",False)
        elif board[state[0]][state[1]] != ".":
            return ("yes",False)
        else:
            return ("yes",True)

    @staticmethod
    def isNoStreet(state, nameFlagEnymy, board):
        moveState, isTrueMove = ZeroTree.moveState(state, board) 
        lst = []
        for x in isTrueMove:
            if x[1] == True:
                return lst, False 
        for x in range(len(isTrueMove)):
            if isTrueMove[x][0]== "yes" and isTrueMove[x][1] == False and board[moveState[x][0]][moveState[x][1]] == nameFlagEnymy:
                lst.append(moveState[x])
        return lst, True

    @staticmethod
    def isDeadEnd(moveState, isTrueMove, state, board):
        nameFlagEnymy = 'r' if board[state[0]][state[1]]  == 'b' else 'b'
        lstLocation = [] # danh sách các vị trí "bị nhốt"
        lst = [] # danh sách các vị trí có khả năng bị nhốt -> cần phải kiểm tra
        for x in moveState:
            if board[x[0]][x[1]] == nameFlagEnymy :
                _lst, isDE = ZeroTree.isNoStreet(x, nameFlagEnymy, board)
                if isDE:
                    lst += _lst
                    lstLocation.append(x)
        if len(lstLocation) != 0:
            for x in lst:
                if x not in lstLocation:
                    _lst, isDE = ZeroTree.isNoStreet(x, nameFlagEnymy, board)
                    if isDE:
                        lst += _lst
                        lstLocation.append(x)
                    else:
                        return []                    
            return lstLocation
        else:
            return []

    @staticmethod
    def isTurn(moveState, isTrueMove, state, board):
        nameFlagEnymy = 'r' if board[state[0]][state[1]]  == 'b' else 'b'
        rn_add1 = state[0] + 1
        rn_sub1 = state[0] - 1
        cn_add1 = state[1] + 1
        cn_sub1 = state[1] - 1  
        lstTurn = []
        if (rn_add1, state[1]) in moveState and (rn_sub1, state[1]) in moveState:
            if board[rn_add1][state[1]] == board[rn_sub1][state[1]] == nameFlagEnymy:
                lstTurn += [(rn_add1, state[1]), (rn_sub1, state[1])]
        if (state[0], cn_add1) in moveState and (state[0], cn_sub1) in moveState:
            if board[state[0]][cn_add1] == board[state[0]][cn_sub1] == nameFlagEnymy:
                lstTurn += [(state[0], cn_add1), (state[0], cn_sub1)]
        if (rn_add1, cn_sub1) in moveState and (rn_sub1, cn_add1) in moveState:
            if board[rn_add1][cn_sub1] == board[rn_sub1][cn_add1] == nameFlagEnymy:
                lstTurn += [(rn_add1, cn_sub1), (rn_sub1, cn_add1)]
        if (rn_add1, cn_add1) in moveState and (rn_sub1, cn_sub1) in moveState:
            if board[rn_add1][cn_add1] == board[rn_sub1][cn_sub1] == nameFlagEnymy:
                lstTurn += [(rn_add1, cn_add1), (rn_sub1, cn_sub1)]
        return lstTurn        

    def remove(self):
        self.root.set_move(None)
        self.root.remove_lstSubNode([])
        self.root.set_value(None)
        self.root.set_board(None)

def board_print(board, move=[], num=0):

    if move:
        print("move = ", move)
    for i in [4, 3, 2, 1, 0]:
        print(i, ":", end=" ")
        for j in range(5):
            print(board[i][j], end=" ")
        print()
    print("   ", 0, 1, 2, 3, 4)
    print("\n")        


    
# ======================== Class Player =======================================
class Player:
    # student do not allow to change two first functions
    def __init__(self, str_name):
        self.str = str_name

    def __str__(self):
        return self.str
    board_ago = 0
    # Student MUST implement this function
    # The return value should be a move that is denoted by a list of tuples:
    # [(row1, col1), (row2, col2)] with:
        # (row1, col1): current position of selected piece
        # (row2, col2): new position of selected piece
    def next_move(self, board):
        result = [(3, 2), (2, 2)]
        minimaxTree = ZeroTree()    
        minimaxTree.remove()

        numFlagNow = 0
        numFlagAgo = 0
        nameFlagEnymy = 'r' if self.str == 'b' else 'b'
        moveAgo = []
        isTrap = False
        if self.board_ago != 0:
            for row in range(5):
                for col in range(5):    
                    if self.board_ago[row][col] == self.str:
                        numFlagAgo += 1
                    if board[row][col] == self.str:
                        numFlagNow += 1
                    if board[row][col] == self.board_ago[row][col]:
                        continue
                    if board[row][col] == '.' and self.board_ago[row][col] == nameFlagEnymy:
                        moveAgo.append((row,col))
                        moveState, isTrueMove = ZeroTree.moveState((row,col), self.board_ago)   
                        for x in range(len(isTrueMove)):
                            if isTrueMove[x][1] == True and board[moveState[x][0]][moveState[x][1]] == nameFlagEnymy:
                                moveAgo.append(moveState[x])

            if numFlagAgo == numFlagNow:
                isTrap = True

                    

        minimaxTree.insertNode(self.str, board, 4)
        minimaxTree.searchNodeMax(self.str ,isTrap, moveAgo)
        move = minimaxTree.get_root().get_move()
        self.board_ago = minimaxTree.get_root().get_board()
        return move