# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 20:35:07 2023

@author: yniak
"""
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
        self.initplayer(gm, color)
        self.moves = None
        self.state = None
        #TODO: incrémanter
        self.turns_nb = 0 #MAX 60

    def initplayer(self,gm,color):
        match gm:
            case 1:
                self.current = Bot(False,self.board)
                self.next = Bot(True,self.board)
            case 2:
                self.current = Bot(not color,self.board) if color else Real(color)
                self.next = Real(color) if color else Bot(not color,self.board)
            case 3:
                self.current = Real(False)
                self.next = Real(True)
            case _:
                pass

    def switchplayer(self):
        self.current, self.next = self.next,self.current
       
     
    def set_moves(self):
        self.moves = Rules.movespossible(self.board, self.current.color)

    def set_flip(self,coord):
        self.toflip=Rules.getflippeddisk(self.board,coord[0],coord[1],self.current.color)
        
    def count_pawns(self):
        return self.board.get_white_pawns_nb(),self.board.get_black_pawns_nb()
        

