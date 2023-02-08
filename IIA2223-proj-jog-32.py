from copy import *
from random import *
from jogos import *
from jogar import *

estadoBT32 = namedtuple('EstadoBT_32', 'to_move, board, pieceValues, wPieces, bPieces, isLastMove')

class EstadoBT_32(estadoBT32):

    colLetter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5:'f', 6:'g', 7:'h'}
    letterCol = {'a': 0, 'b': 1, 'c': 2 , 'd': 3 , 'e': 4 , 'f': 5, 'g': 6, 'h': 7}
    
    def ve_se_terminou(self):
        
        if self.wPieces == 0:
            return -1   
        elif self.bPieces == 0:
            return 1
        
        return self.isLastMove
    
    def other(self):
        return '1' if self.to_move == '2' else '2'
    
    def moves(self):
        
        if self.ve_se_terminou():
            return []
        
        out = []
        direction = 1 if self.to_move == '1' else -1
        
        for (i,j) in self.board.keys():
            
            if self.to_move == '1' and self.board.get((i,j)) == '2':
                continue
            
            elif self.to_move == '2' and self.board.get((i,j)) == '1':
                continue
            
            movs1 = self.colLetter.get(j) + str(i+1) + "-"
            movs2 = self.colLetter.get(j) + str(i+1) + "-"
            movs3 = self.colLetter.get(j) + str(i+1) + "-"

            if 0 <= j - 1 < 8 and self.board.get((i + direction, j - 1)) != self.to_move:
                movs1 += self.colLetter.get(j - 1) + str(i + 1 + direction)
                out.append(movs1)
            if  self.board.get((i + direction, j)) == None:
                movs2 += self.colLetter.get(j) + str(i + 1 + direction)
                out.append(movs2)
            if  0 <= j + 1 < 8 and self.board.get((i + direction, j + 1)) != self.to_move:
                movs3 += self.colLetter.get(j + 1) + str(i + 1 + direction)
                out.append(movs3)
            
        out.sort()   
        return out
    
    def __str__(self):
        display = "-----------------\n"
        
        for i in range (0,8):
            display+= str(8-i)
            display+="|"
            for j in range (0,8):
                if self.board.get((7-i,j)) == '1':
                    display+='W '
                elif self.board.get((7-i,j)) == '2':
                    display+='B '
                else:
                    display+='. '
            display+="\n"
                    
        display+="-+---------------\n"
        display+=" |a b c d e f g h"
        player = "W" if self.to_move == '1' else "B"
        if not self.ve_se_terminou():
            display+="\n--NEXT PLAYER: "
            display+=str(player)
        return display

class JogoBT_32(Game):
    
    def __init__(self):
        grid = dict()
        pValues = dict()
        
        for i in range(0,8):
            for j in range(0,8):
                if i == 0 or i == 1:
                    grid[(i,j)] = '1'
                elif i == 6 or i == 7:
                    grid[(i,j)] = '2'
        
        for (i,j) in grid.keys():
            pValues[(i,j)] = self.__getPieceValue(i, j, grid, '1')
                    
        self.initial = EstadoBT_32(to_move = '1', board = grid, pieceValues = pValues, wPieces = 16, bPieces = 16, isLastMove = 0)
 
    def terminal_test(self, state):
        "A state is terminal if the whites reached line 8 or some black reached line 1."
        return bool(state.ve_se_terminou())
    
    def actions(self, state):
        "Legal moves for B and W"
        return state.moves()

    def result(self, state, move):
        player = state.to_move
        board2 = state.board.copy()
        pValues = state.pieceValues.copy()
        eatWhite = False
        eatBlack = False
        lastMove = 0
        
        initI = int(move[1]) - 1 
        initJ = state.letterCol[move[0]]
        endI = int(move[4]) - 1 
        endJ = state.letterCol[move[3]]
                
        del board2[(initI, initJ)]
        del pValues[(initI, initJ)]
        if board2.get((endI, endJ)) == '1':
            pValues[(endI, endJ)] = self.__getPieceValue(endI, endJ, board2, state.to_move)
            eatWhite = True
        elif board2.get((endI, endJ)) == '2':
            pValues[(endI, endJ)] = self.__getPieceValue(endI, endJ, board2, state.to_move)
            eatBlack = True
        
        if endI == 0 and player == '2':
            lastMove = -1
        elif endI == 7 and player == '1':
            lastMove = 1
        
        board2[(endI, endJ)] = '1' if player == '1' else '2'
        
        for i in [-1,0,1]:
            
            if 0 <= endI + i < 8 and 0 <= endJ + 1 < 8 and board2.get((endI+i, endJ+1)) != None:
                pValues[(endI+i, endJ + 1)] = self.__getPieceValue(endI+i, endJ+1, board2, state.to_move)
                
            if 0 <= endI + i < 8 and 0 <= endJ < 8 and board2.get((endI+i, endJ)) != None:
                pValues[(endI+i, endJ)] = self.__getPieceValue(endI+i, endJ, board2, state.to_move)
                
            if 0 <= endI + i < 8 and 0 <= endJ - 1 < 8 and board2.get((endI+i, endJ-1)) != None:
                pValues[(endI+i, endJ - 1)] = self.__getPieceValue(endI+i, endJ-1, board2, state.to_move)
                
        return EstadoBT_32(to_move = state.other(), board = board2, pieceValues = pValues, wPieces = state.wPieces - 1 if eatWhite else
                          state.wPieces, bPieces = state.bPieces - 1 if eatBlack else state.bPieces, isLastMove = lastMove)
    
    def utility(self, state, player):
        return state.ve_se_terminou()
             
    def executa(self, estado, listaJogadas):
        "executa varias jogadas sobre um estado dado"
        "devolve o estado final "
        s = estado
        for j in listaJogadas:
            s = self.result(s, j)
        return s
    
    def __getPieceValue(self, x, y, board, player):

        pieceAlmostWinValue = 500
        verticalConnectionValue = 5
        horizontalConnectionValue = 10
        pieceCanMove = 5
        firstRowValuePos = {0: 100,1: 50,2: 75,3: 60,4: 60,5: 75,6: 50,7: 100}
        secondRowValuePos = {0: 50,1: 0,2: 0,3: 0,4: 0,5: 0,6: 0,7: 50}
        pieceAttackValue = 15
        pieceDefendValue = 10
        pieceEdgeValue = -2
        rowValues = {0: 25,1: 5,2: 5,3: 8,4: 10,5: 15,6: 25,7: 50}   
        #Pieces have a value just by existing
        pieceValue = 40
        piecePlayer = board.get((x,y))
        notMine = 1 if player != piecePlayer else -1
        verticalConnected = False
        horizontalConnected = False

        if y == 0 or y == 7:
            pieceValue += pieceEdgeValue

        if board.get((x + 1, y)) == board.get((x, y)) or board.get((x - 1, y)) == board.get((x, y)):
            verticalConnected = True
        if board.get((x, y + 1)) == board.get((x, y)) or board.get((x, y - 1)) == board.get((x, y)):
            horizontalConnected = True

        pieceValue = pieceValue + verticalConnectionValue if verticalConnected else pieceValue
        pieceValue = pieceValue + horizontalConnectionValue if horizontalConnected else pieceValue

        if piecePlayer == '1':
            pieceValue += rowValues.get(x)
            if x == 0:
                pieceValue += firstRowValuePos.get(y)
            elif x == 1:
                pieceValue += secondRowValuePos.get(y)
            direction = 1
        else:
            pieceValue += rowValues.get(7-x)
            if x == 7:
                pieceValue += firstRowValuePos.get(y)
            elif x == 6:
                pieceValue += secondRowValuePos.get(y)
            direction = -1

        if 0 <= x + direction < 8:
            if board.get((x + direction, y + 1)) == piecePlayer or board.get((x + direction, y - 1)) == piecePlayer:
                pieceValue += pieceDefendValue

            if board.get((x + direction, y - 1)) == self.__getOppositePlayer(piecePlayer):

                pieceValue += notMine * pieceAttackValue

            if board.get((x + direction, y + 1)) == self.__getOppositePlayer(piecePlayer):

                pieceValue += notMine * pieceAttackValue

            if ((x + direction == 7 and player == '1') or (x + direction == 0 and player == '2')) and (board.get((x + direction, y - 1)) == None and board.get((x + direction, y + 1)) == None):
                pieceValue += pieceAlmostWinValue

        pieceValue += pieceCanMove * self.__getPieceMobilityValue(x, y, board, direction)

        return pieceValue

    def __getPieceMobilityValue(self, x, y, board, direction):
        value = 0

        if 0 <= x + direction < 8:
            if board.get((x, y)) != board.get((x + direction, y + 1)):
                value+= 1
            if board.get((x, y)) != board.get((x + direction, y - 1)):
                value += 1
            if board.get((x + direction, y)) == None:
                value += 1

        return value

    def __getOppositePlayer(self, player):
        return '1' if player == '2' else '2'
    
def func_aval_32(state, player):
    
    utility = state.ve_se_terminou()
    
    if utility == 1:
        return 10000 if player == '1' else -10000
    elif utility == -1:
        return 10000 if player == '2' else -10000
    
    emptyColumnValue = -40
    retValue = 0
    whiteColumns = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
    blackColumns = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
    
    if player == '1':
        for (i,j) in state.board.keys():
            if state.board.get((i,j)) == '1':
                retValue+=state.pieceValues.get((i,j))
                whiteColumns[j] = 1
            else:
                retValue-=state.pieceValues.get((i,j))
                blackColumns[j] = 1
    else:
        for (i,j) in state.board.keys():
            if state.board.get((i,j)) == '1':
                retValue-=state.pieceValues.get((i,j))
                whiteColumns[j] = 1
            else:
                retValue+=state.pieceValues.get((i,j))
                blackColumns[j] = 1

    
    sumWhiteCols = sum(whiteColumns.values())
    sumBlackCols = sum(blackColumns.values())

    if player == '1':
        retValue += (8 - sumWhiteCols) * emptyColumnValue
        retValue -= (8 - sumBlackCols) * emptyColumnValue
    else:
        retValue -= (8 - sumWhiteCols) * emptyColumnValue
        retValue += (8 - sumBlackCols) * emptyColumnValue 
    
    return retValue