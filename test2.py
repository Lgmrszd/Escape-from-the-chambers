# -*- coding: utf-8 -*-
from level_manager import *
import level_classes as lvlobj

def add_space_left(lvlmap):
    lvlmap2 = []
    for i in lvlmap:
        lvlmap2.append(lvlobj.tile())


def main():
    level = import_level('testlevelset/3.lvl')
    level.printInfo()
    lvlmap = lvlobj.levelmap(level)
    for my_y in range(lvlmap.getHeight()):
        w = ''
        for my_x in range(lvlmap.getWidth()):
            t = lvlmap.getTile(my_x, my_y)
            w += t.getType()
        print(w)
    for my_y in range(lvlmap.getHeight()):
        w = ''
        for my_x in range(lvlmap.getWidth()):
            t = lvlmap.getTile(my_x, my_y)
            w += t.getSymbol()
        print(w)
    print(lvlmap.getRoomsCoords())
    print('----------------------------------------')
'''
    result, lvl2 = lvlmap.getLevel().getGateByName('room4gate').executeScript(level)
    lvlmap2 = lvlobj.levelmap(lvl2)
    for my_y in range(lvlmap2.getHeight()):
        w = ''
        for my_x in range(lvlmap2.getWidth()):
            t = lvlmap2.getTile(my_x, my_y)
            w += t.getType()
        print(w)
    for my_y in range(lvlmap2.getHeight()):
        w = ''
        for my_x in range(lvlmap2.getWidth()):
            t = lvlmap2.getTile(my_x, my_y)
            w += t.getSymbol()
        print(w)
    lvl2.printInfo()
    print(lvlmap2.getRoomsCoords())

    print('----------------------------------------')
    result, lvl2 = lvlmap.getLevel().getGateByName('room4gate').executeScript(lvlmap2.getLevel())
    lvlmap2 = lvlobj.levelmap(lvl2)
    for my_y in range(lvlmap2.getHeight()):
        w = ''
        for my_x in range(lvlmap2.getWidth()):
            t = lvlmap2.getTile(my_x, my_y)
            w += t.getType()
        print(w)
    for my_y in range(lvlmap2.getHeight()):
        w = ''
        for my_x in range(lvlmap2.getWidth()):
            t = lvlmap2.getTile(my_x, my_y)
            w += t.getSymbol()
        print(w)
    lvl2.printInfo()
    print(lvlmap2.getRoomsCoords())
    print('----------------')
'''

if __name__ == "__main__":
    main()
