class tile(object):
    def __init__(self):
        self.__type = ' '
        self.__symbol = '.'
        self.__background = 'b'
        self.__foreground = 'w'

    def getBackground(self):
        return self.__background

    def getForeground(self):
        return self.__foreground

    def getSymbol(self):
        return self.__symbol

    def getType(self):
        return self.__type

    def setBackground(self, bg):
        self.__background = bg

    def setForeground(self, fg):
        self.__foreground = fg

    def setSymbol(self, s):
        self.__symbol = s

    def setType(self, t):
        self.__type = t

class message(object):
    def __init__(self, room, mx, my, color, text):
        self.__room = room
        self.__coord_x = mx
        self.__coord_y = my
        self.__color = color
        self.__text = text

    def getRoomName(self):
        return self.__room

    def getCoords(self):
        return (self.__coord_x, self.__coord_y)

    def getInfo(self):
        return [self.__color, self.__text]

class gate(object):
    def __init__(self, gatename, room, rx, ry, direction, targetgate, script):
        self.__gate_name = gatename
        self.__room = room
        self.__coord_x = rx
        self.__coord_y = ry
        self.__direction = direction
        self.__target_gate_name = targetgate
        self.__script_name = script

    def getName(self):
        return self.__gate_name

    def getRoomName(self):
        return self.__room

    def getCoords(self):
        return (self.__coord_x, self.__coord_y)

    def getDirection(self):
        return self.__direction

    def getTarget(self):
        return  self.__target_gate_name

    def setTarget(self, target):
        self.__target_gate_name = target
        
    def movLeft(self, shft):
        self.__coord_x += shft

    def executeScript(self, lvl):
        print(self.__script_name)
        rslt = False
        lvl2 = 0
        if self.__script_name != 'none':
            script = __import__('normallevelset.scripts.%s.%s'%(lvl.getName(), self.__script_name), fromlist=('script'))
            rslt, lvl2 = script.script(lvl, self.__room, self.__coord_x, self.__coord_y)
        return rslt, lvl2


class room(object):
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__roommap = [[tile() for _ in range(width)] for _ in range(height)]
        self.__room_name = ''

    def getName(self):
        return self.__room_name

    def getRoomMap(self):
        return self.__roommap

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getTile(self, x, y):
        return self.__roommap[y][x]

    def setName(self, rn):
        self.__room_name = rn

    def setTileBackground(self, x, y, bg):
        self.__roommap[y][x].setBackground(bg)

    def setTileForeground(self, x, y, fg):
        self.__roommap[y][x].setForeground(fg)

    def setTileSymbol(self, x, y, s):
        self.__roommap[y][x].setSymbol(s)

    def setTileType(self, x, y, t):
        self.__roommap[y][x].setType(t)

class level(object):
    def __init__(self, name, room, px, py, eroom, ex, ey):
        self.__name = name
        self.__spawn_x = px
        self.__spawn_y = py
        self.__defroom = room
        self.__end_x = ex
        self.__end_y = ey
        self.__endroom = eroom
        self.__rooms = {}
        self.__gates = {}
        self.__messages = {}
        self.__gatesbyroom = {}
        self.__otherdata = {}
    
    def getName(self):
        return self.__name
    
    def getOtherData(self):
        return self.__otherdata
    
    def updateOtherData(self, newdata):
        self.__otherdata.update(newdata)
    
    def printInfo(self):
        print('level info: ', self.__name, self.__spawn_x, self.__spawn_y, self.__defroom)
        print(self.__gatesbyroom)
        print('gates:')
        for k in self.__gates.keys():
            print(k, self.__gates[k].getRoomName(), self.__gates[k].getTarget())
        print('rooms:')
        for k in self.__rooms.keys():
            rm = self.__rooms[k]
            print(k)
            for y in range(rm.getHeight()):
                w = ''
                for x in range(rm.getWidth()):
                    w += rm.getTile(x, y).getSymbol()
                print(w)

    def addRooms(self, rooms):
        self.__rooms.update(rooms)

    def addGates(self, gates):
        self.__gates.update(gates)
        for gatename in self.__gates.keys():
            roomname = self.__gates[gatename].getRoomName()
            if self.__gatesbyroom.get(roomname) is None:
                self.__gatesbyroom[roomname] = set()
            self.__gatesbyroom[roomname].update([gatename])

    def addMessages(self, messages):
        self.__messages.update(messages)
    
    def replaceGate(self, gt):
        self.__gates[gt.getName()] = gt

    def getRoomsNames(self):
        return list(self.__rooms.keys())

    def getGatesNames(self):
        return list(self.__gates.keys())

    def getRoomByName(self, roomname):
        return self.__rooms[roomname]

    def getGateByName(self, gatename):
        return self.__gates[gatename]

    def getMessageByName(self, msgname):
        return self.__messages[msgname]

    def getMessages(self):
        return self.__messages

    def getStartRoom(self):
        return self.__defroom

    def getGatesInRoom(self, roomname):
        return self.__gatesbyroom[roomname]

    def getSpawnCoords(self):
        return [self.__spawn_x, self.__spawn_y]

    def getEndInfo(self):
        return [self.__endroom, self.__end_x, self.__end_y]
        print('-------- end x and y', self.__end_x, self.__end_y)

    def setSpawnCoords(self, x, y):
        self.__spawn_x, self.__spawn_y = x, y

    def setStartRoom(self, rmnm):
        self.__defroom = rmnm

class levelmap(object):
    def __init__(self, in_level):
        self.__current_room = in_level.getStartRoom()
        #print('SPAWN ROOM', self.__current_room)
        self.__spawn_coords = in_level.getSpawnCoords()
        self.__end_info = in_level.getEndInfo()
        #print('endinfo', self.__end_info)
        self.__level = in_level
        self.__width = in_level.getRoomByName(in_level.getStartRoom()).getWidth()
        self.__height = in_level.getRoomByName(in_level.getStartRoom()).getHeight()
        self.__roommap = list(in_level.getRoomByName(in_level.getStartRoom()).getRoomMap())
        self.__rooms_coords = {in_level.getStartRoom(): [0, 0]}
        self.__space_left = 0
        self.__space_top = 0
        self.__checked_rooms = set()
        self.__checked_rooms.add(in_level.getStartRoom())
        for my_y in range(self.getHeight()):
            w = ''
            for my_x in range(self.getWidth()):
                t = self.getTile(my_x, my_y)
                w += t.getSymbol()
            #print(w)
        for gatename in in_level.getGatesInRoom(in_level.getStartRoom()):
            wgate = in_level.getGateByName(gatename)
            #print('gc', wgate.getCoords(), 'direction', wgate.getDirection())
            direction = wgate.getDirection()
            gx, gy = wgate.getCoords()
            troom = in_level.getRoomByName(in_level.getGateByName(wgate.getTarget()).getRoomName())
            tgx, tgy = in_level.getGateByName(wgate.getTarget()).getCoords()
            #print('gates coords: ', tgx, tgy)
            if direction == 'right':
                srx, sry = gx + tgx + 1, gy - tgy
            elif direction == 'left':
                srx, sry = gx - tgx - 1, gy - tgy
            elif direction == 'down':
                srx, sry = gx - tgx, gy + tgy + 1
            else:
                srx, sry = gx - tgx, gy - tgy - 1
            
            srx += self.__rooms_coords[in_level.getStartRoom()][0]
            sry += self.__rooms_coords[in_level.getStartRoom()][1]

            self.__rooms_coords[troom.getName()] = [srx, sry]
            self.applyRoom(troom, srx, sry)
        for gatename in in_level.getGatesInRoom(in_level.getStartRoom()):
            #print('fucking wring gates there: ', gatename)
            rmnm = in_level.getGateByName(self.__level.getGateByName(gatename).getTarget()).getRoomName()
            self.__checked_rooms.add(rmnm)
        print('checked after 1st room: ', self.__checked_rooms)
        for gatename in in_level.getGatesInRoom(in_level.getStartRoom()):
            rmnm = in_level.getGateByName(self.__level.getGateByName(gatename).getTarget()).getRoomName()
            #print(' other rooms: ', rmnm)
            self.workRoom(rmnm)

    def workRoom(self, rmnm):
        for my_y in range(self.getHeight()):
            w = ''
            for my_x in range(self.getWidth()):
                t = self.getTile(my_x, my_y)
                w += t.getSymbol()
            #print(w)
        self.__checked_rooms.add(rmnm)
        #print(self.__checked_rooms)
        #print('WORK IN ROOOOOOOM ', rmnm)
        for gatename in self.__level.getGatesInRoom(rmnm):
            tgname = self.__level.getGateByName(gatename).getTarget()
            if self.__level.getGateByName(tgname).getRoomName() not in self.__checked_rooms:
                wgate = self.__level.getGateByName(gatename)
                #print('FINALLY BINALLY GATES NOMBERS AAA ', gatename, wgate.getTarget())
                #print('gc', wgate.getCoords(), 'direction', wgate.getDirection())
                direction = wgate.getDirection()
                gx, gy = wgate.getCoords()
                troom = self.__level.getRoomByName(self.__level.getGateByName(wgate.getTarget()).getRoomName())
                tgx, tgy = self.__level.getGateByName(wgate.getTarget()).getCoords()
                #print('gates coords: ', tgx, tgy)
                if direction == 'right':
                    srx, sry = gx + tgx + 1, gy - tgy
                elif direction == 'left':
                    srx, sry = gx - tgx - 1, gy - tgy
                elif direction == 'down':
                    srx, sry = gx - tgx, gy + tgy + 1
                else:
                    srx, sry = gx - tgx, gy - tgy - 1

                srx += self.__rooms_coords[rmnm][0]
                sry += self.__rooms_coords[rmnm][1]

                self.__rooms_coords[troom.getName()] = [srx, sry]
                self.applyRoom(troom, srx, sry)
                print(self.__checked_rooms)
        for gatename in self.__level.getGatesInRoom(rmnm):
            tgname = self.__level.getGateByName(gatename).getTarget()
            if self.__level.getGateByName(tgname).getRoomName() not in self.__checked_rooms:
                rmnm2 = self.__level.getGateByName(self.__level.getGateByName(gatename).getTarget()).getRoomName()
                print('ROOMNOOM 2 ', rmnm2)
                self.workRoom(rmnm2)

    def applyRoom(self, aroom, sx, sy):
        rmmap = aroom.getRoomMap()
        rsx, rsy = aroom.getWidth(), aroom.getHeight()
        print('x: map, room, shift: ', self.__width, rsx, sx)
        print('y: map, room, shift: ', self.__height, rsy, sy)

        if sx < 0:
            self.addTilesLeft(-sx)
            sx = 0

        if sy < 0:
            self.addTilesUp(-sy)
            sy = 0

        if sy + rsy > self.__height:
            self.addTilesDown(sy + rsy - self.__height)

        if sx + rsx > self.__width:
            self.addTilesRight(sx + rsx - self.__width)

        print(len(self.__roommap[0]), len(self.__roommap))
        for y in range(rsy):
            for x in range(rsx):
                #print (x, y, x + sx, y + sy, rmmap[y][x].getType())
                self.__roommap[y + sy][x + sx] = rmmap[y][x]

        self.__height = len(self.__roommap)
        self.__width = len(self.__roommap[0])

    def addTilesRight(self, n):
        for i in range(len(self.__roommap)):
            self.__roommap[i] += [tile() for i in range(n)]
        self.__height = len(self.__roommap)
        self.__width = len(self.__roommap[0])

    def addTilesLeft(self, n):
        for i in range(len(self.__roommap)):
            self.__roommap[i] = [tile() for j in range(n)] + self.__roommap[i]
        for rmnm in self.__rooms_coords.keys():
            self.__rooms_coords[rmnm][0] += n
        self.__spawn_coords[0] += n
        self.__height = len(self.__roommap)
        self.__width = len(self.__roommap[0])
        self.__space_left += n
        for my_y in range(self.getHeight()):
            w = ''
            for my_x in range(self.getWidth()):
                t = self.getTile(my_x, my_y)
                w += t.getSymbol()
            print(w)

    def addTilesDown(self, n):
        self.__roommap += [[tile() for i in range(len(self.__roommap[0]))] for j in range(n)]
        self.__height = len(self.__roommap)
        self.__width = len(self.__roommap[0])

    def addTilesUp(self, n):
        self.__roommap = [[tile() for i in range(len(self.__roommap[0]))] for j in range(n)] + self.__roommap
        for rmnm in self.__rooms_coords.keys():
            self.__rooms_coords[rmnm][1] += n
        self.__spawn_coords[1] += n
        self.__height = len(self.__roommap)
        self.__width = len(self.__roommap[0])
        self.__space_top += n
        for my_y in range(self.getHeight()):
            w = ''
            for my_x in range(self.getWidth()):
                t = self.getTile(my_x, my_y)
                w += t.getSymbol()
            print(w)

    def getSpawnCoords(self):
        return self.__spawn_coords

    def getEndCoords(self):
        if self.__end_info[0] in self.__rooms_coords.keys():
            print('end crds: ', self.__end_info[1], self.__end_info[2])
            print('room crds: ', self.__rooms_coords[self.__end_info[0]][0], self.__rooms_coords[self.__end_info[0]][1])
            return [self.__end_info[1] + self.__rooms_coords[self.__end_info[0]][0], self.__end_info[2] + self.__rooms_coords[self.__end_info[0]][1]]
        else:
            return [-1, -1]

    def getRoomsCoords(self):
        return self.__rooms_coords

    def getLevel(self):
        return self.__level

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getTile(self, x, y):
        return self.__roommap[y][x]
