"""
Created on Sun Apr  2 15:59:11 2023

@author: yniak
"""
import numpy as np


class Board:
    BOARD_SIZE = 8
    DIRECTIONS = np.array([(i, j) for j in range(-1, 2) for i in range(-1, 2) if not (i == 0 == j)])

    def __init__(self):
        self.status = None
        self.initboard()
    
    def initboard(self):
        b = np.full((Board.BOARD_SIZE, Board.BOARD_SIZE), None)
        b[3][3], b[4][4], b[3][4], b[4][3] = True, True, False, False
        self.status = b

    # Place un pion + flip
    def change(self, x, y, p):
        self.status[x][y] = p
        for i, j in Board.DIRECTIONS:
            vsize = Board.vectorsize(self, [i, j], x, y, p)
            if vsize and vsize > 0:
                self.flip((i, j), vsize, x, y, p)

    def flip(self, vector, vsize, x, y, p):
        x += vector[0]
        y += vector[1]
        while vsize > 0:
            self.status[x][y] = p
            x += vector[0]
            y += vector[1]
            vsize -= 1

    @staticmethod
    def flips(board, x, y, p):
        for i, j in Board.DIRECTIONS:
            size = Board.vectorsize(board, [i, j], x, y, p)
            if size and size > 0:
                return True
        return False

    @staticmethod
    def vectorsize(board, vector, x, y, p):
        d = 0
        x += vector[0]
        y += vector[1]
        while 0 <= x < Board.BOARD_SIZE and 0 <= y < Board.BOARD_SIZE and board.status[x][y] is not None:
            if board.status[x][y] == p:
                return d
            d += 1
            x += vector[0]
            y += vector[1]
        return None

    def isfull(self):
        return None not in self.status

    def have(self, color):
        for i in range(Board.BOARD_SIZE):
            for j in range(Board.BOARD_SIZE):
                if self.status[i][j] == color:
                    return True
        return False
    
    def simulate_stroke(self,move,player):
         self.status[move[0]][move[1]] = player
    
    def undo_move(self,move):
        self.status[move[0]][move[1]] = None

    def get_black_pawns_nb(self):
        return sum(line.count(False) for line in self.status)
    
    def get_white_pawns_nb(self):
        return sum(line.count(True) for line in self.status)

    def get_pawns_nb(self,color):
        return np.count_nonzero(self.status == color)
    
    def __str__(self):
        return '\n'.join([str(i) for i in self.status])


