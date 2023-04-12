"""
Created on Sun Apr  2 12:17:38 2023

@author: yniak
"""

import pygame
import pygame_menu

from typing import Optional

from GUI.utils import Utils
from Game.Match import Match

GM = 1
COLOR = False

is_paused = False
returning = False
restart = False

main_menu: Optional['pygame_menu.Menu'] = None
surface: Optional['pygame.Surface'] = None


def set_gm(value, gm):
    global GM
    GM = gm
    print(GM)


def set_color(value, gm):
    global COLOR
    COLOR = gm
    print(COLOR)


def play(font: 'pygame.font.Font'):
    # init
    global is_paused, returning, restart, GM, COLOR, is_done
    # Scores set init
    font = pygame.font.SysFont("Montserrat", 40)
    font_2 = pygame.font.SysFont("Raleway", 40)
    font_3 = pygame.font.SysFont("Comic Sans MS", 20)
    txt = font.render("SCORES", True, Utils.black)
    Blk_Nb = Wht_Nb = 2
    Blk_txt,Wht_txt =font_2.render(str(Blk_Nb), True, Utils.black),font_2.render(str(Wht_Nb), True, Utils.black)
    is_done = False
    
    
    match = Match(GM, COLOR)
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
            restart = False
            match = Match(GM, COLOR)
            Blk_Nb = Wht_Nb = 2
            Blk_txt,Wht_txt =font_2.render(str(Blk_Nb), True, Utils.black),font_2.render(str(Wht_Nb), True, Utils.black)
            pygame.display.flip()
            continue

        # Si le jeu n'est pas en pause, on fait les traitements de jeu normalement
        if not is_paused:
            # Scores display Part
            surface.fill(Utils.gainsboro)
            surface.blit(txt,(170,160))
            surface.blit(Utils.disk[0], (195,260))
            surface.blit(Utils.disk[4], (195,360))
            surface.blit(Blk_txt, (290,270))
            surface.blit(Wht_txt, (290,375))
            
            match.set_moves()
            Utils.DrawBoard(surface, match.board, match.moves)
            pygame.display.update()
            if not match.isfinished :
                if match.board.isfull() or not match.board.have(match.current.color) or match.turns_nb == 60:
                    match.isfinished = True
                    continue
                if len(match.moves) > 0:
                    coord = match.current.play(match.moves)
                    if isinstance(coord, int) and coord == pygame.K_ESCAPE:
                        is_paused = not is_paused
                        continue
                    match.board.change(coord[0], coord[1], match.current.color)
                    Wht_Nb,Blk_Nb = match.count_pawns()
                    Blk_txt, Wht_txt = font_2.render(str(Blk_Nb), True, Utils.black),font_2.render(str(Wht_Nb), True, Utils.black)
                    pause_menu.enable()
                    pygame.display.flip()
                else:
                    #TODO: Pour quand il peut pas jouer ?
                    print('pass')
                match.switchplayer()
            else:
                W = font.render("WHITES WIN THO !", True, Utils.white) 
                B = font.render("BLACKS WIN THO !", True, Utils.white)
                T = font.render("IT'S A TIE THO !", True, Utils.white)
                Winner= W if match.count_pawns()[0]> match.count_pawns()[1] else B if match.count_pawns()[0] < match.count_pawns()[1] else T
                surface.fill(Utils.grey)
                surface.blit(Winner, (500,160))
                surface.blit(Utils.disk[0], (540,260))
                surface.blit(Utils.disk[4], (540,360))
                surface.blit(Blk_txt, (620,273))
                surface.blit(Wht_txt, (620,375))
                surface.blit(font_3.render("Press a key for main menu...",True,Utils.white2),(10,650))
                pygame.display.flip()
                pause()
                is_done = True
                
                

        # Afficher le menu de pause ou le menu principal
        if is_done:
            main_menu.mainloop(surface)
        elif is_paused:
            pause_menu.mainloop(surface)
        if returning:
            returning = False
            return
        pygame.display.update()


def removePause(r=False):
    global is_paused
    global restart
    is_paused = False
    restart = r
    pause_menu.disable()

def returnFunc():
    global returning
    returning = True
    removePause()

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                paused = False
                break
        pygame.time.delay(100)
        

pygame.init()
surface = pygame.display.set_mode(Utils.WINDOW_SIZE)
pygame.display.set_caption('Othello')
icon = pygame.image.load('Asset/icon.png')
pygame.display.set_icon(icon)

main_menu = pygame_menu.Menu('Othello', 1280, 720,
                             theme=pygame_menu.themes.THEME_DARK)

main_menu.add.button('Play', play, pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))
main_menu.add.selector('Game mode ', [('Bot vs Bot', 1), ('P1 vs Bot', 2), ('P1 vs P2', 3)], onchange=set_gm)
main_menu.add.selector('Color (P1) ', [('Black', False), ('White', True)], onchange=set_color)
main_menu.add.button('Quit', pygame_menu.events.EXIT)
# pause menu
pause_menu = pygame_menu.Menu('Pause', 1280, 720, theme=pygame_menu.themes.THEME_DARK)
# faire restart
pause_menu.add.button('Continue', removePause)
pause_menu.add.button('Restart', removePause, True)
pause_menu.add.button('Main menu', returnFunc)
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
