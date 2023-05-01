# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 20:35:15 2023

@author: yniak
"""
import pygame
from abc import ABC, abstractmethod
from GUI.utils import Utils
from AI.AI_Player import Strategy
import time

class Player(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def play(self):
        pass


class Bot(Player):
    def __init__(self,color,board,turn_nb):
        super().__init__(color)
        self.turn_nb = turn_nb
        self.board = board
        self.strategy= Strategy(color,5,0.5,0.2,0.3)

    def play(self, moves):
        if self.turn_nb >= 12 and self.turn_nb < 30:
            self.strategy.set_weighting_nb_pawns(0.2)
            self.strategy.set_weighting_nb_stroke(0.1)
            self.strategy.set_weighting_position(0.7)
        elif self.turn_nb >= 30:
            self.strategy.set_weighting_nb_pawns(0.8)
            self.strategy.set_weighting_nb_stroke(0.1)
            self.strategy.set_weighting_position(0.1)
            
        move = self.strategy.get_best_move(self.board,1.0)
        print("AI =>", move)
        return move


class Real(Player):
    def __init__(self, color):
        super().__init__(color)
    
    def play(self, moves):
        # Calcul de la position de l'échiquier pour le centrer sur l'écran
        board_x = (Utils.WINDOW_SIZE[0] - Utils.square_size * 8) // 2
        board_y = (Utils.WINDOW_SIZE[1] - Utils.square_size * 8) // 2
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return event.key
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                coord = ((mouse_pos[1] - board_y) // 50, (mouse_pos[0] - board_x) // 50)
                if coord in moves:
                    return coord
