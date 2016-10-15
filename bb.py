#!/usr/bin/python

import pygame
from pygame.locals import *

def separate(txt):
    lenofstr = 32
    tmpt = txt.split()
    tt=[]
    wt = tmpt[0]
    for i in tmpt[1:]:
        print(i)
        if len(wt) + len (i) + 1 <= lenofstr:
            wt += ' ' + i
        else:
            tt.append(wt)
            wt = i
    tt.append(wt)
    return tt

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((400, 200))
    pygame.display.set_caption('Basic Pygame program')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Display some text
    font = pygame.font.Font(None, 36)
    t = '1234567890123456789012345 424 646546 5645645645'
    tt = separate(t)
    print(tt)
    text = font.render("Hello There ...", 1, (10, 70, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        screen.blit(background, (0, 0))
        pygame.display.flip()


if __name__ == '__main__': main()
