# -*- coding: utf-8 -*-
import pygame
from pygame import *
import button

BACKGROUND_COLOR = '#999999'

def imageToList(img):
    strsf = image.tostring(img, 'RGBA')
    arrsf = []
    for i in range(len(strsf)//4):
        arrsf.append(strsf[4 * i : 4 + 4 * i])
    
    w, h = img.get_rect().width, img.get_rect().height
    
    image_list = []
    for i in range(len(arrsf)//w):
        image_list.append(arrsf[w * i : w + w * i])
    return image_list

def listToImage(imglist):
    imglist2 = []
    for i in imglist:
        imglist2 += i
    return image.frombuffer(b''.join(imglist2), (len(imglist[0]), len(imglist)), 'RGBA')

def cutVertical(img, sx):
    imglist = imageToList(img)
    imgl1 = []
    imgl2 = []
    for i in imglist:
        imgl1.append(i[:sx])
        imgl2.append(i[sx:])
    
    img1 = listToImage(imgl1)
    img2 = listToImage(imgl2)
    return img1, img2

class Button(object):
    def __init__(self, width, txtmsg):
        self.stat = 0
        bs = 12
        self.size = (width, 32)
        
        unactive_all = image.load('/home/mikhail/PycharmProjects/Escape-from-the-chambers/sprites/button_unactive.png')
        unactive_left, tmp = cutVertical(unactive_all, bs)
        unactive_center, unactive_right = cutVertical(tmp, unactive_all.get_rect().width - bs * 2)
        unactive_center, _ = cutVertical(unactive_center, 1)
        self.unactive = Surface((width, 32), pygame.SRCALPHA, 32)
        self.unactive = self.unactive.convert_alpha()
        self.unactive.blit(unactive_left, (0,0))
        self.unactive.blit(unactive_right, (width - bs,0))
        for i in range(width - bs * 2):
            self.unactive.blit(unactive_center, (bs + i, 0))
        
        active_all = image.load('/home/mikhail/PycharmProjects/Escape-from-the-chambers/sprites/button_active.png')
        active_left, tmp = cutVertical(active_all, bs)
        active_center, active_right = cutVertical(tmp, active_all.get_rect().width - bs * 2)
        active_center, _ = cutVertical(active_center, 1)
        self.active = Surface((width, 32), pygame.SRCALPHA, 32)
        self.active = self.active.convert_alpha()
        self.active.blit(active_left, (0,0))
        self.active.blit(active_right, (width - bs,0))
        for i in range(width - bs * 2):
            self.active.blit(active_center, (bs + i, 0))
        
        pressed_all = image.load('/home/mikhail/PycharmProjects/Escape-from-the-chambers/sprites/button_pressed.png')
        pressed_left, tmp = cutVertical(pressed_all, bs)
        pressed_center, pressed_right = cutVertical(tmp, pressed_all.get_rect().width - bs * 2)
        pressed_center, _ = cutVertical(pressed_center, 1)
        self.pressed = Surface((width, 32), pygame.SRCALPHA, 32)
        self.pressed = self.pressed.convert_alpha()
        self.pressed.blit(pressed_left, (0,0))
        self.pressed.blit(pressed_right, (width - bs,0))
        for i in range(width - bs * 2):
            self.pressed.blit(pressed_center, (bs + i, 0))
        
        font = pygame.font.SysFont('Monospace', 15, bold = True)
        text = font.render(txtmsg, 1, (0, 0, 0))
        self.unactive.blit(text, (self.unactive.get_rect().centerx - text.get_rect().centerx, self.unactive.get_rect().centery - text.get_rect().centery))
        self.active.blit(text, (self.active.get_rect().centerx - text.get_rect().centerx, self.active.get_rect().centery - text.get_rect().centery))
        self.pressed.blit(text, (1 + self.pressed.get_rect().centerx - text.get_rect().centerx, 1 + self.pressed.get_rect().centery - text.get_rect().centery))
        
    
    def getWidgetImage(self):
        return self.active


class MyMainWindow(object):
    def __init__(self, size):
        self.size = size
        self.screen = pygame.display.set_mode(size)
        self.fps = 50
        self.timer = pygame.time.Clock()
        self.bg = Surface(self.size)
        self.bg.fill(Color(BACKGROUND_COLOR))
        self.widgets = []
        self.initUI()
    
    def setCaption(self, text):
        pygame.display.set_caption(text)
    
    def workEvents(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.work = False
                self.rslt = 0
    
    def addWidget(self, widget, pos):
        self.widgets.append([widget, pos])
    
    def redraw(self):
        self.screen.blit(self.bg, (0, 0))
        for wdg in self.widgets:
            self.screen.blit(wdg[0].getWidgetImage(), wdg[1])
        pygame.display.flip()
    
    def run(self):
        self.work = True
        while self.work:
            self.workEvents()
            self.redraw()
            self.timer.tick(self.fps)
        pygame.display.quit()
        return self.rslt
    
    def initUI(self):
        self.setCaption('abcdefg')
        btn = Button(100, 'HEllo')
        self.addWidget(btn, (10, 20))

def main():
    pygame.init()
    window = MyMainWindow((200,150))
    result = window.run()
    return result

if __name__ == "__main__":
    main()
