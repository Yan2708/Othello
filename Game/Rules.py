# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 15:58:06 2023

@author: yniak
"""
from Game.Board import Board
import numpy as np


def isplayable(board, x, y, p):
    """
    :param board: la partie
    :param x: coord x
    :param y: coord y
    :param p: le joueur
    :return: True si un coup est possible sinon False
    """
    return board.status[x][y] is None and checkadjacent(board, x, y, not p) and Board.flips(board, x, y, p)


def movespossible(board, p):
    """
    :param board: la partie
    :param p: le joueur
    :return: une liste des coups possibles
    """
    t = []
    for i in range(8):
        for j in range(8):
            if isplayable(board, i, j, p):
                t.append((i, j))
    return t


def checkadjacent(board, x, y, p):
    """
    :param board: la partie
    :param x: coord x
    :param y: coord y
    :param p: le joueur adverse
    :return: True si le pion est adjacent a au moins une piece enemie sinon False
    """
    for i, j in Board.DIRECTIONS:
        try:
            if board.status[x + i][y + j] == p:
                return True
        except:
            pass
    return False
