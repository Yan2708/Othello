"""
Created on Sun Apr  2 15:59:11 2023

@author: yniak
"""
import numpy as np


class Board:
    # taille de l'echiquier
    BOARD_SIZE = 8
    # les 8 vecteurs de direction possibles
    DIRECTIONS = np.array([(i, j) for j in range(-1, 2) for i in range(-1, 2) if not (i == 0 == j)])

    def __init__(self):
        self.status = None
        self.initboard()
    
    def initboard(self):
        """
        initialise l'echiquier pour un debut de partie normale
        """
        b = np.full((Board.BOARD_SIZE, Board.BOARD_SIZE), None)
        b[3][3], b[4][4], b[3][4], b[4][3] = True, True, False, False
        self.status = b

    def change(self, x, y, p):
        """
        pose une piece sur l'echiquier et retourne celles qui doivent l'etre
        :param x: coord x
        :param y: coord y
        :param p: le joueur
        """
        self.status[x][y] = p
        flipped_positions = []
        for i, j in Board.DIRECTIONS:
            vsize = Board.vectorsize(self, [i, j], x, y, p)
            if vsize and vsize > 0:
                flipped_positions.extend(self.flip((i, j), vsize, x, y, p))
        return flipped_positions
    
    def undo_change(self,x,y,flip_p):
        self.status[x][y] = None
        for xbis, ybis in flip_p:
            self.status[xbis][ybis] = not self.status[xbis][ybis]

    def flip(self, vector, vsize, x, y, p):
        """
        retourne toute les pieces selon le vecteur donne et la position de depart
        :param vector: la direction des pions a retourner
        :param vsize: le nombre de pions a retourner
        :param x: coord x
        :param y: coord y
        :param p: le joueur
        """
        x += vector[0]
        y += vector[1]
        flipped_positions = []
        while vsize > 0:
            self.status[x][y] = p
            x += vector[0]
            y += vector[1]
            vsize -= 1
            flipped_positions.append((x,y))
        return flipped_positions

    @staticmethod
    def flips(board, x, y, p):
        """
        determine si une piece (x,y) retourne des pieces sur l'echiquier
        :param board: l'echiquier
        :param x: coord x
        :param y: coord y
        :param p: le joueur
        :return:
        """
        for i, j in Board.DIRECTIONS:
            size = Board.vectorsize(board, [i, j], x, y, p)
            if size and size > 0:
                return True
        return False

    @staticmethod
    def vectorsize(board, vector, x, y, p):
        """
        determine le nombre de pieces a retourner
        :param board: la partie
        :param vector: lea direction
        :param x: coord x
        :param y: coord y
        :param p: le joueur
        :return:
        """
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
        """
        :return: si l'echiquier est plein ou non
        """
        return None not in self.status

    def have(self, color):
        """
        :param color: couleur a verifier
        :return: si la couleur est presente sur l'echiquier
        """
        for i in range(Board.BOARD_SIZE):
            for j in range(Board.BOARD_SIZE):
                if self.status[i][j] == color:
                    return True
        return False
    
    def get_pawns_nb(self,color):
        """
        :param color: la couleur des pions recherches
        :return: le nombre de pions de cette couleur
        """
        return np.count_nonzero(self.status == color)
    
    def __str__(self):
        return '\n'.join([str(i) for i in self.status])


