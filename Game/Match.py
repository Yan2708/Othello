# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 20:35:07 2023

@author: yniak
"""
import numpy as np

from Game import Rules
from Game.Board import Board
from Game.Player import Bot, Real


class Match:
    def __init__(self, gm, color=False):
        self.toflip = None
        self.next = None
        self.current = None
        self.board = Board()
        self.isfinished = False
        self.turns_nb = 1
        self.moves = None
        self.state = None
        self.initplayer(gm, color)

    def initplayer(self, gm, color):
        match gm:
            # bot vs bot
            case 1:
                self.current = Bot(False, self.board, self.turns_nb)
                self.next = Bot(True, self.board, self.turns_nb)
            # bot vs player
            case 2:
                self.current = Bot(not color, self.board, self.turns_nb) if color else Real(color)
                self.next = Real(color) if color else Bot(not color, self.board, self.turns_nb)
            # player vs player
            case 3:
                self.current = Real(False)
                self.next = Real(True)
            case _:
                pass

    def switchplayer(self):
        """
        passe au prochain joueur
        """
        self.current, self.next = self.next, self.current

    def set_moves(self):
        """
        actualise la variable moves avec les coups possibles du joueur actuel
        """
        self.moves = Rules.movespossible(self.board, self.current.color)

    def count_pawns(self):
        """
        :return: le nombre de pions blancs moins ceux des noirs
        """
        return self.board.get_pawns_nb(True), self.board.get_pawns_nb(False)
