# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 23:33:44 2023

@author: yniak
"""
import pygame
import time


class Utils:
    # couleurs & taille
    white = (255, 255, 255)
    white2 = (239, 236, 239)
    black = (0, 0, 0)
    yellow = (254, 199, 45)
    beige = (245, 230, 200)
    blue = (28, 118, 206)
    grey = (46, 46, 46)
    gainsboro = (220, 220, 220)
    square_size = 50
    WINDOW_SIZE = (1280, 720)

    try:
        disk = [pygame.image.load('./Asset/disk/disk0.png'), pygame.image.load('./Asset/disk/disk1.png'),
                pygame.image.load('./Asset/disk/disk2.png'), pygame.image.load('./Asset/disk/disk3.png'),
                pygame.image.load('./Asset/disk/disk4.png')]
    except Exception:
        disk = [pygame.image.load('../Asset/disk/disk0.png'), pygame.image.load('../Asset/disk/disk1.png'),
                pygame.image.load('../Asset/disk/disk2.png'), pygame.image.load('../Asset/disk/disk3.png'),
                pygame.image.load('../Asset/disk/disk4.png')]

    def timer(func):
        def inner(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"execution of {func.__name__} *************** in {end - start:0.4f} seconds")
            return result

        return inner

    def DrawBoard(surface, board, moves):

        # Calcul de la position de l'échiquier pour le centrer sur l'écran
        board_x = (Utils.WINDOW_SIZE[0] - Utils.square_size * 8) // 2
        board_y = (Utils.WINDOW_SIZE[1] - Utils.square_size * 8) // 2

        for row in range(8):
            for col in range(8):
                x = board_x + col * Utils.square_size
                y = board_y + row * Utils.square_size

                if (row + col) % 2 == 0:
                    pygame.draw.rect(surface, Utils.beige, (x, y, Utils.square_size, Utils.square_size))
                else:
                    pygame.draw.rect(surface, Utils.blue, (x, y, Utils.square_size, Utils.square_size))

                if board.status[row][col] is not None:
                    surface.blit(Utils.disk[4] if board.status[row][col] else Utils.disk[0], (x - 1, y - 1))
        if moves:
            for y, x in moves:
                x = board_x + x * Utils.square_size
                y = board_y + y * Utils.square_size
                pygame.draw.circle(surface, Utils.grey, (x + 25, y + 25), 5)

    def DrawScore(surface, txt, Blk_txt, Wht_txt):
        surface.fill(Utils.gainsboro)
        surface.blit(txt, (170, 160))
        surface.blit(Utils.disk[0], (195, 260))
        surface.blit(Utils.disk[4], (195, 360))
        surface.blit(Blk_txt, (290, 270))
        surface.blit(Wht_txt, (290, 375))

