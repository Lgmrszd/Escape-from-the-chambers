# -*- coding: utf-8 -*-
import pygame
from pygame import *

PLATFORM_WIDTH = 64
PLATFORM_HEIGHT = 64
PLATFORM_COLOR = "#FF6262"
PATTERN_COLOR = '#FF00FF'
PLATFORM_BLOCKS = {'━': 'sprites/block_0.png', '┃': 'sprites/block_1.png', '┏': 'sprites/block_2.png',
                   '┓': 'sprites/block_3.png', '┛': 'sprites/block_4.png', '┗': 'sprites/block_5.png'}


def convert_image(sf, tcolor):
    strsf = image.tostring(sf, 'RGBA')
    arrsf = []
    for i in range(len(strsf) // 4):
        arrsf.append(strsf[4 * i:4 + 4 * i])
    nasf = []
    for i in arrsf:
        if i == bytes(list(Color(PATTERN_COLOR))):
            nasf.append(bytes(list(Color(tcolor))))
        else:
            nasf.append(i)
    return image.frombuffer(b''.join(nasf), (64, 64), 'RGBA')


class Platform(sprite.Sprite):
    def __init__(self, x, y, pf):
        sprite.Sprite.__init__(self)
        self.image = pf
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
