# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 15:58:06 2023

@author: yniak
"""
from Game.Board import Board
import numpy as np

def isplayable(board, x, y, p):
    return board.status[x][y] is None and checkadjacent(board, x, y, not p) and Board.flips(board, x, y, p)


def checkadjacent(board, x, y, p):
    positions_adjacentes = np.array([(0, 1), (0, -1), (1, 0), (-1, 0)])
    for i, j in positions_adjacentes:
        try:
            if board.status[x + i][y + j] == p:
                return True
        except:
            pass
    return False

#TODO:Mettre dans board ?
def movespossible(board, p):
    t = []
    for i in range(8):
        for j in range(8):
            if isplayable(board, i, j, p):
                t.append((i, j))
    return t

def is_in_corner(position):
    corner =  np.array([(0,0),(0,7),(7,7),(7,0)])
    if position in corner:
        return True
    return False
def is_in_border(position):
    if is_in_corner(position) == False:
        if position[0] == 0 or position[0] == 7:
            return True
        elif position[1] == 0 or position[1] == 7:
            return True
    return False

def checkadjacent_for_corner(p):
    corner = np.array([(0,0),(0,7),(7,7),(7,0)])
    is_adj = False
    for t in corner:
        if t[0] == p[0] and abs(t[1]-p[1]) == 1 or t[1] == p[1] and abs(t[0]-p[0]) == 1:
            is_adj == True
        if is_adj:
            break
    return is_adj
    

