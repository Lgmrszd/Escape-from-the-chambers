#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pyganim
import level_classes as lvlobj

need_unstopable_control = False

ANIMATION_DELAY = 0.25
ANIMATION_DOWN = ['sprites/player_mov_down_1.png',
                  'sprites/player_mov_down_2.png']
ANIMATION_UP = ['sprites/player_mov_up_1.png',
                'sprites/player_mov_up_2.png']
ANIMATION_LEFT = ['sprites/player_mov_left_1.png',
                  'sprites/player_mov_left_2.png']
ANIMATION_RIGHT = ['sprites/player_mov_right_1.png',
                   'sprites/player_mov_right_2.png']

SPRITE_STAND_DOWN = 'sprites/player_stand_down.png'
SPRITE_STAND_UP = 'sprites/player_stand_up.png'
SPRITE_STAND_LEFT = 'sprites/player_stand_left.png'
SPRITE_STAND_RIGHT = 'sprites/player_stand_right.png'
WIDTH = 64
HEIGHT = 64
PLATFORM_WIDTH = 64
PLATFORM_HEIGHT = 64
COLOR = '#888888'
DELAY = 50 # Time for step
FPS = 5 # Frames Per STEP

class Player(sprite.Sprite):
    def __init__(self, x, y, sproom):
        super().__init__()
        self.boltAnimDown = pyganim.PygAnimation([(i, ANIMATION_DELAY) for i in ANIMATION_DOWN])
        self.boltAnimDown.play()
        self.boltAnimUp = pyganim.PygAnimation([(i, ANIMATION_DELAY) for i in ANIMATION_UP])
        self.boltAnimUp.play()
        self.boltAnimLeft = pyganim.PygAnimation([(i, ANIMATION_DELAY) for i in ANIMATION_LEFT])
        self.boltAnimLeft.play()
        self.boltAnimRight = pyganim.PygAnimation([(i, ANIMATION_DELAY) for i in ANIMATION_RIGHT])
        self.boltAnimRight.play()
        self.stage = 0
        self.direct = ''
        self.lasttime = time.get_ticks()
        self.startXmap = x
        self.startYmap = y
        self.xmap = x
        self.ymap = y
        self.__need_coords_x = 0
        self.__need_coords_y = 0
        self.__need_change_coords = False
        self.__old_room = sproom
        self.startX = x * PLATFORM_WIDTH + (PLATFORM_WIDTH // 2) - (WIDTH // 2) # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y * PLATFORM_HEIGHT + (PLATFORM_HEIGHT // 2) - (HEIGHT // 2)
        self.image = image.load(SPRITE_STAND_DOWN)
        self.rect = Rect(x * PLATFORM_WIDTH + (PLATFORM_WIDTH // 2) - (WIDTH // 2), y * PLATFORM_HEIGHT + (PLATFORM_HEIGHT // 2) - (HEIGHT // 2), WIDTH, HEIGHT) # прямоугольный объект

    def setCoordsold(self, x, y):
        self.__need_coords_x = x
        self.__need_coords_y = y
        self.__need_change_coords = True

    def setCoords(self, x, y):
        self.xmap = x
        self.ymap = y
        self.startX = x * PLATFORM_WIDTH + (PLATFORM_WIDTH // 2) - (WIDTH // 2) # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y * PLATFORM_HEIGHT + (PLATFORM_HEIGHT // 2) - (HEIGHT // 2)
        self.rect = Rect(x * PLATFORM_WIDTH + (PLATFORM_WIDTH // 2) - (WIDTH // 2), y * PLATFORM_HEIGHT + (PLATFORM_HEIGHT // 2) - (HEIGHT // 2), WIDTH, HEIGHT) # прямоугольный объект
        
    def checkRoom(self, lvlmap):
        roomscoords = lvlmap.getRoomsCoords()
        #print('my coords: ', self.xmap, self.ymap)
        for roomname in roomscoords.keys():
            roomcoords = roomscoords[roomname]
            rmx, rmy = roomcoords
            rmw, rmh = lvlmap.getLevel().getRoomByName(roomname).getWidth(), lvlmap.getLevel().getRoomByName(roomname).getHeight()
            if (self.xmap >= rmx) and (self.xmap <= (rmx +  rmw - 1)) and (self.ymap >= rmy) and (self.ymap <= (rmy +  rmh - 1)):
                return roomname

    def getGate(self, lvlmap):
        cgatename = None
        croom = self.checkRoom(lvlmap)
        #print('CROOM: ', croom)
        gates = lvlmap.getLevel().getGatesInRoom(croom)
        roomscoords = lvlmap.getRoomsCoords()
        rmx, rmy = roomscoords[croom]
        for gatename in gates:
            gx, gy = lvlmap.getLevel().getGateByName(gatename).getCoords()
            gx += rmx
            gy += rmy
            print(gatename, gx, gy)
            if (gx, gy) == (self.xmap, self.ymap):
                cgatename = gatename
        return cgatename

    def canGoUp(self, lvlmap):
        return ((self.ymap > 1) and (lvlmap.getTile(self.xmap, self.ymap - 1).getType() != 'w'))
    
    def canGoLeft(self, lvlmap):
        return ((self.xmap > 1) and (lvlmap.getTile(self.xmap - 1, self.ymap).getType() != 'w'))
    
    def canGoDown(self, lvlmap):
        return ((self.ymap < lvlmap.getHeight() - 1) and lvlmap.getTile(self.xmap, self.ymap + 1).getType() != 'w')
    
    def canGoRight(self, lvlmap):
        
        return ((self.xmap < lvlmap.getWidth() - 1) and lvlmap.getTile(self.xmap + 1, self.ymap).getType() != 'w')
    
    def goLeft(self):
        self.stage = 1
        self.direct = 'l'
        self.xmap -= 1
        self.rect.x = self.stage0x - self.stage * PLATFORM_WIDTH / FPS
        self.image = image.load('sprites/player_empty.png')
        self.boltAnimLeft.blit(self.image, (0, 0))
        
    def goRight(self):
        self.stage = 1
        self.direct = 'r'
        self.xmap += 1
        self.rect.x = self.stage0x + self.stage * PLATFORM_WIDTH / FPS
        self.image = image.load('sprites/player_empty.png')
        self.boltAnimRight.blit(self.image, (0, 0))
    
    def goUp(self):
        self.stage = 1
        self.direct = 'u'
        self.ymap -= 1
        self.rect.y = self.stage0y - self.stage * PLATFORM_HEIGHT/FPS
        self.image = image.load('sprites/player_empty.png')
        self.boltAnimUp.blit(self.image, (0, 0))
    
    def goDown(self):
        self.stage = 1
        self.direct = 'd'
        self.ymap += 1
        self.rect.y = self.stage0y + self.stage * PLATFORM_HEIGHT/FPS
        self.image = image.load('sprites/player_empty.png')
        self.boltAnimDown.blit(self.image, (0, 0))

    def update(self,  left, right, up, down, lvlmap):
        whatsnew = {}
        hasnewlvl = False
        newlvl = 0
        nowtime = time.get_ticks()
        if (nowtime - self.lasttime) > DELAY/FPS:
            if self.stage == 0:
                self.olddirect = self.direct
                self.stage0x = self.rect.x
                self.stage0y = self.rect.y

                if (not need_unstopable_control) or (not(self.canGoLeft(lvlmap)) and self.direct == 'l') or (not(self.canGoRight(lvlmap)) and self.direct == 'r') or (not(self.canGoUp(lvlmap)) and self.direct == 'u') or (not(self.canGoDown(lvlmap)) and self.direct == 'd'):
                    self.direct = ''
            
                if ((left or ((self.direct == 'l') and need_unstopable_control)) and not (up or down or right)):
                    self.lasttime = nowtime
                    self.direct = ''
                    if self.canGoLeft(lvlmap):
                        self.goLeft()
                    else:
                        self.image = image.load(SPRITE_STAND_LEFT)

                if ((right or ((self.direct == 'r') and need_unstopable_control)) and not (up or down or left)):
                    self.lasttime = nowtime
                    self.direct = ''
                    if self.canGoRight(lvlmap):
                        self.goRight()
                    else:
                        self.image = image.load(SPRITE_STAND_RIGHT)

                if ((up or ((self.direct == 'u') and need_unstopable_control))  and not (left or right or down)):
                    self.lasttime = nowtime
                    self.direct = ''               
                    if self.canGoUp(lvlmap):
                        self.goUp()
                    else:
                        self.image = image.load(SPRITE_STAND_UP)

                if ((down or ((self.direct == 'd') and need_unstopable_control)) and not (left or right or up)):
                    self.lasttime = nowtime
                    self.direct = ''
                    if self.canGoDown(lvlmap):
                        self.goDown()
                    else:
                        self.image = image.load(SPRITE_STAND_DOWN)

                if self.direct == '':
                    if self.olddirect == 'd':
                        self.image = image.load(SPRITE_STAND_DOWN)
                    elif self.olddirect == 'u':
                        self.image = image.load(SPRITE_STAND_UP)
                    elif self.olddirect == 'r':
                        self.image = image.load(SPRITE_STAND_RIGHT)
                    elif self.olddirect == 'l':
                        self.image = image.load(SPRITE_STAND_LEFT)




            else:
                if (nowtime - self.lasttime) > DELAY/FPS:
                    if self.stage == FPS:
                        self.rect.x = self.xmap * PLATFORM_WIDTH + (PLATFORM_WIDTH // 2) - (WIDTH // 2)
                        self.rect.y = self.ymap * PLATFORM_HEIGHT + (PLATFORM_HEIGHT // 2) - (HEIGHT // 2)
                        self.stage = 0

                        croom = self.checkRoom(lvlmap)
                        roomscoords = lvlmap.getRoomsCoords()
                        rmx, rmy = roomscoords[croom]
                        #print('lvldata:', lvlmap.getLevel().getOtherData())
                        #print(lvlmap.getEndCoords())
                        if lvlmap.getTile(self.xmap, self.ymap).getType() == 'm':
                            msgs = lvlmap.getLevel().getMessages()
                            for msgname in msgs.keys():
                                print (msgname, msgs[msgname].getRoomName())
                                if msgs[msgname].getRoomName() == croom:
                                    msgcrds = msgs[msgname].getCoords()
                                    if (msgcrds[0] + rmx, msgcrds[1] + rmy) == (self.xmap, self.ymap):
                                        whatsnew['msg'] = msgs[msgname].getInfo()
                        
                        ex, ey = lvlmap.getEndCoords()
                        #print((ex, ey))
                        #print((self.xmap, self.ymap))
                        if (self.xmap, self.ymap) == (ex, ey):
                            whatsnew['end'] = True
                        if croom != self.__old_room:
                            #print(self.__old_room, croom)
                            gatename = self.getGate(lvlmap)
                            #print('IN GATE: ', gatename)
                            hasnewlvl, newlvl = lvlmap.getLevel().getGateByName(gatename).executeScript(lvlmap.getLevel())
                            if hasnewlvl:
                                print(hasnewlvl, newlvl, 'newlvl size: ', lvlobj.levelmap(newlvl).getWidth())
                                whatsnew.update({'newlvl': newlvl})
                        self.__old_room = croom

                    else:
                        self.lasttime = nowtime
                        self.stage += 1
                        self.image = image.load('sprites/player_empty.png')
                        if self.direct == 'l':
                            self.rect.x = self.stage0x - self.stage * PLATFORM_WIDTH/FPS
                            self.boltAnimLeft.blit(self.image, (0, 0))
                        elif self.direct == 'r':
                            self.rect.x = self.stage0x + self.stage * PLATFORM_WIDTH / FPS
                            self.boltAnimRight.blit(self.image, (0, 0))
                        elif self.direct == 'u':
                            self.rect.y = self.stage0y - self.stage * PLATFORM_HEIGHT/FPS
                            self.boltAnimUp.blit(self.image, (0, 0))
                        else:
                            self.rect.y = self.stage0y + self.stage * PLATFORM_HEIGHT/FPS
                            self.boltAnimDown.blit(self.image, (0, 0))
        return whatsnew
