"""
Created on Sun Apr  2 15:59:11 2023

@author: yniak
"""


class Board:
    BOARD_SIZE = 8

    def __init__(self):
        self.status = None
        self.initboard()

    def initboard(self):
        b = [[None for _ in range(Board.BOARD_SIZE)] for _ in range(Board.BOARD_SIZE)]
        #WHY ?
        b[3][3], b[4][4], b[3][4], b[4][3] = True, True, False, False
        self.status = b
    
    #Place un pion + flip
    def change(self, x, y, p):
        self.status[x][y] = p
        for i in range(-1, 2):
            for j in range(-1, 2):
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
        for i in range(-1, 2):
            for j in range(-1, 2):
                size = Board.vectorsize(board, [i, j], x, y, p)
                if size and size > 0:
                    return True
        return False
    
    #TODO: Yann explained AIM 1?
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
        for i in range(Board.BOARD_SIZE):
            for j in range(Board.BOARD_SIZE):
                if self.status[i][j] is None: return False
        return True
    
    #TODO: Yann explained AIM 2?
    def have(self, color):
        for i in range(Board.BOARD_SIZE):
            for j in range(Board.BOARD_SIZE):
                if self.status[i][j] == color:
                    return True
        return False

    def __str__(self):
        return '\n'.join([str(i) for i in self.status])
