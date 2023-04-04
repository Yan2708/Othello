# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 12:17:38 2023

@author: yniak
"""

import pygame
import pygame_menu
from utils import Utils
from typing import Optional
from Match import Match
import time

GM=1
COLOR=False

is_paused=False
returning=False
restart=False

main_menu: Optional['pygame_menu.Menu'] = None
surface: Optional['pygame.Surface'] = None



def set_gm(value, gm):
    global GM
    GM=gm


def set_color(value, gm):
    global COLOR
    COLOR=gm

def play(gm, font: 'pygame.font.Font',color):
    #init
    global is_paused
    global returning
    global restart
    
    match = Match(gm,color)
    # Boucle de jeu
    surface.fill(Utils.black)
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_paused = not is_paused
                    if is_paused:
                        pause_menu.enable()
                    else:
                        pause_menu.disable()

        if restart:
            restart=False
            match=Match(gm,color)
            pygame.display.update()
            continue
        
        # Si le jeu n'est pas en pause, on fait les traitements de jeu normalement
        if not is_paused:
            surface.fill(Utils.black)
            match.set_moves()
            Utils.DrawBoard(surface,match.board,match.moves)
            pygame.display.update()
            if not match.isfinished:
                match.next_play()

    
        # Afficher le menu de pause ou le menu principal
        if is_paused:
            pause_menu.mainloop(surface)
    
        if returning:
            returning=False
            return
        pygame.display.update()

def removePause(r=False):
    global is_paused
    global restart
    is_paused=False
    restart=r
    pause_menu.disable()

def returnFunc():
    global returning
    returning=True
    removePause()
    

pygame.init()
surface = pygame.display.set_mode(Utils.WINDOW_SIZE)
pygame.display.set_caption('Othello')  
icon = pygame.image.load('./Asset/icon.png')
pygame.display.set_icon(icon)

main_menu = pygame_menu.Menu('Othello', 1280, 720,
                       theme=pygame_menu.themes.THEME_DARK)

main_menu.add.button('Play', play,GM, pygame.font.Font(pygame_menu.font.FONT_FRANCHISE,30),COLOR)
main_menu.add.selector('Game mode ', [('Bot vs Bot', 1), ('P1 vs Bot', 2),('P1 vs P2',3)], onchange=set_gm)
main_menu.add.selector('Color (P1) ', [('Black', False), ('White', True)], onchange=set_color)
main_menu.add.button('Quit', pygame_menu.events.EXIT)
#pause menu 
pause_menu= pygame_menu.Menu('Pause', 1280, 720,theme=pygame_menu.themes.THEME_DARK)
# faire restart
pause_menu.add.button('Continue', removePause)
pause_menu.add.button('Restart', removePause,True)
pause_menu.add.button('Main menu', returnFunc )
pause_menu.add.button('Quit', pygame_menu.events.EXIT)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    surface.fill(Utils.white)
    
    if main_menu.is_enabled:
        main_menu.mainloop(surface)


    pygame.display.update()

pygame.quit()
