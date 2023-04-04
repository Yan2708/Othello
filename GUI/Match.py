# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 20:35:07 2023

@author: yniak
"""
import os
import sys
from Player import Real,Bot
script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'Game' )
sys.path.append( mymodule_dir )
from Board import Board
import Rules

class Match:
    def __init__(self,gm,color=False):
        self.next = None
        self.current = None
        self.board=Board()
        self.isfinished=False
        self.initplayer(gm,color)
        self.moves=None

    def initplayer(self, gm,color):
        match gm:
            case 1:
                self.current = Bot(False)
                self.next = Real(True)
            case 2:
                self.current=Bot(not color)
                self.next=Real(color)
            case 3:
                self.current = Real(False)
                self.next = Real(True)
            case _:
                pass

    def switchplayer(self):
        tmp=self.current
        self.current=self.next
        self.next=tmp

    def set_moves(self):
        self.moves = Rules.movespossible(self.board, self.current.color)

    def next_play(self):
        if self.board.isfull() or not self.board.have(self.current.color):
            self.isfinished=True
            return
        if len(self.moves)>0:
            coord=self.current.play(self.moves)
            self.board.change(coord[0], coord[1], self.current.color)
        else:
            print('pass')
        self.switchplayer()

            
        
        