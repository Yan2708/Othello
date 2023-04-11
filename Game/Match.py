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
        #NEW
        self.state = None
        #TODO: incrémanter
        self.turns_nb = 0 #MAX 60

    def initplayer(self,gm,color):
        match gm:
            case 1:
                self.current = Bot(False)
                self.next = Bot(True)
            case 2:
                self.current = Bot(not color) if color else Real(color)
                self.next = Real(color) if color else Bot(not color)
            case 3:
                self.current = Real(False)
                self.next = Real(True)
            case _:
                pass

    def switchplayer(self):
        self.current, self.next = self.next,self.current
        """ 
       print(self.board.status)
       print(" Player 1 => colors: ",self.current.color," =>",self.board.status.count(self.current.color),"\n","Player 2 => colors: ",self.next.color," =>",self.board.status.count(self.next.color))
       """ 
    def set_moves(self):
        self.moves = Rules.movespossible(self.board, self.current.color)

    def set_flip(self,coord):
        self.toflip=Rules.getflippeddisk(self.board,coord[0],coord[1],self.current.color)
    
    # TODO get_winner
    #def get_winner(self):
        

