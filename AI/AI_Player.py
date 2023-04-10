# -*- coding: utf-8 -*-
import Game.Player as Player

#TODO: Set strategie
class AI_Basic(Player):
    def __init__(self, color):
        super().__init__(color)
        self.strategy=None

    def play(self, moves):
        return moves[0]