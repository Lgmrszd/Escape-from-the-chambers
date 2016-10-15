# -*- coding: utf-8 -*-
import pygame
from pygame import *
from player import Player

WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000"

PLATFORM_WIDTH = 64
PLATFORM_HEIGHT = 64
PLATFORM_COLOR = "#FF6262"
level = [['┏', '━', '┓',' '],
         ['┃', ' ', '┗','━'],
         ['┃', ' ', ' ',' '],
         ['┃', ' ', '┏','━'],
         ['┗', '━', '┛',' ']]


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    timer = pygame.time.Clock()
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Mygame")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом
    hero = Player(55, 55)
    left = right = False
    while 1:  # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        x = y = 0  # координаты
        for row in level:  # вся строка
            for col in row:  # каждый символ
                pf = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
                    pf.fill(Color(PLATFORM_COLOR))
                    screen.blit(pf,(x,y))
                if col == "━":
                    pf = image.load('sprites/block_red_0.png')
                    screen.blit(pf, (x, y))
                elif col == "┃":
                    pf = image.load('sprites/block_red_1.png')
                    screen.blit(pf, (x, y))
                elif col == "┏":
                    pf = image.load('sprites/block_red_2.png')
                    screen.blit(pf, (x, y))
                elif col == "┓":
                    pf = image.load('sprites/block_red_3.png')
                    screen.blit(pf, (x, y))
                elif col == "┛":
                    pf = image.load('sprites/block_red_4.png')
                    screen.blit(pf, (x, y))
                elif col == "┗":
                    pf = image.load('sprites/block_red_5.png')
                    screen.blit(pf, (x, y))

                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля

        hero.update(left, right) # передвижение
        hero.draw(screen) # отображение
        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()
