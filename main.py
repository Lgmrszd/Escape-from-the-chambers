# -*- coding: utf-8 -*-
__author__= 'Lgmrszd'
import pygame
from engine import *
import level_classes as lvlobj
from level_manager import *
from pygame import *
from player import Player
from blocks import Platform
from camera import *

WIN_WIDTH = 800
WIN_HEIGHT = 640
MSG_HEIGHT = 205
BORDER_SIZE = 20
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = '#000000'
PATTERN_COLOR = '#FF00FF'

def convert_image(sf, tcolor):
    strsf = image.tostring(sf, 'RGBA')
    arrsf = []
    for i in range(len(strsf)//4):
        arrsf.append(strsf[4 * i:4 + 4 * i])
    nasf = []
    for i in arrsf:
        if i == bytes(list(Color(PATTERN_COLOR))):
            nasf.append(bytes(list(Color(tcolor))))
        else:
            nasf.append(i)
    return image.frombuffer(b''.join(nasf), (64, 64), 'RGBA')

def generate_blocks():
    blocks={}
    for t in PLATFORM_BLOCKS.keys():
        tblocks = {}
        pf = image.load(PLATFORM_BLOCKS[t])
        for c in PLATFORM_COLORS.keys():
            tblocks[c] = convert_image(pf, PLATFORM_COLORS[c])
        blocks[t] = tblocks
    return blocks

def separate(txt):
    lenofstr = 32
    tmpt = txt.split()
    tt=[]
    wt = tmpt[0]
    for i in tmpt[1:]:
        if len(wt) + len (i) + 1 <= lenofstr:
            wt += ' ' + i
        else:
            tt.append(wt)
            wt = i
    tt.append(wt)
    return tt



def run_level(levelname):
    level = import_level(levelname)
    print(level)
    lvlmap = lvlobj.levelmap(level)
    sproom = lvlmap.getLevel().getStartRoom()
    hero_x, hero_y = lvlmap.getSpawnCoords()
    hero = Player(hero_x, hero_y, sproom)
    left = right = False
    up = down = False

    pygame.init()  # Инициация PyGame, обязательная строчка
    timer = pygame.time.Clock()
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Mygame")  # Пишем в заголовок
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом
    print(lvlmap)

    total_level_width = lvlmap.getWidth() * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = lvlmap.getHeight() * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)
    blocks = generate_blocks()
    lvlwork = True
    whatsnew = {}
    realdirect = 0
    prsd = True
    while lvlwork:  # Основной цикл программы
        timer.tick(300)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                lvlwork = False

            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
                prsd = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
                prsd = True

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
                prsd = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
                prsd = False

            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True

            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_UP:
                up = False

        screen.blit(bg, (0, 0))
        x = y = 0
        msginfo = whatsnew.get('msg')
        while msginfo:
            for e in pygame.event.get():
                if e.type == QUIT:
                    lvlwork = False
                    msginfo = None
                if e.type == KEYDOWN and e.key == K_SPACE:
                    msginfo = None
                    left = False
                    right = False
                    up = False
                    down = False
            timer.tick(300)

        if left and (not right) and prsd:
            prsd = False
            realdirect = (realdirect - 1) % 4
        if right and (not left) and prsd:
            prsd = False
            realdirect = (realdirect + 1) % 4
        rleft, rright, rup, rdown = not bool(3 - realdirect), not bool(1 - realdirect), not bool(realdirect), not bool(2 - realdirect)
        #print(rleft, rright, rup, rdown)
        #print(realdirect)
        #whatsnew = hero.update(rleft, rright, rup, rdown, lvlmap)  # передвижение
        whatsnew = hero.update(left, right, up, down, lvlmap)  # передвижение
        for news in whatsnew:
            if news == 'newlvl':
                lvlmap = lvlobj.levelmap(whatsnew['newlvl'])
                hero_x, hero_y = lvlmap.getSpawnCoords()
                hero.setCoords(hero_x, hero_y)
                total_level_width = lvlmap.getWidth() * PLATFORM_WIDTH
                total_level_height = lvlmap.getHeight() * PLATFORM_HEIGHT
                print('sizes: ', lvlmap.getWidth(), lvlmap.getHeight())
                camera = Camera(camera_configure, total_level_width, total_level_height)
            if news == 'end':
                lvlwork = False

        camera.update(hero)
        for my_y in range(lvlmap.getHeight()):
            for my_x in range(lvlmap.getWidth()):
                col = lvlmap.getTile(my_x, my_y)
                pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                pf.fill(Color(PLATFORM_COLORS[col.getBackground()]))
                tmprect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
                screen.blit(pf, camera.apply_rect(tmprect))
                if col.getType() in ['w', 'd', 'm']:
                    pf = blocks[col.getSymbol()][col.getForeground()]
                    screen.blit(pf, camera.apply_rect(tmprect))

                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля
        screen.blit(hero.image, camera.apply(hero))
        msginfo = whatsnew.get('msg')
        if msginfo:
            msg = message(msginfo[0], msginfo[1])
            screen.blit(msg, (0, WIN_HEIGHT - MSG_HEIGHT))
        pygame.display.update()  # обновление и вывод всех изменений на экран

    pygame.quit()

def main():
    run_level('normallevelset/3.lvl')

if __name__ == "__main__":
    main()
