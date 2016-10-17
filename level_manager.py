import level_classes as lvlobj

def readblock_levelinfo(lines):
    for line in lines:
        if line[:7] == '*!name ':
            name = line[7:]
        elif line[:9] == '*!plspwn ':
            player_spawn_room, player_spawn_x, player_spawn_y = line[9:].split()
        elif line[:9] == '*!lvlend ':
            end_room, end_x, end_y = line[9:].split()
    levelinfo = {'name' : name, 'player_spawn_room' : player_spawn_room, 'player_spawn_coords_x' : int(player_spawn_x), 'player_spawn_coords_y' : int(player_spawn_y), 'end_room' : end_room, 'end_coords_x' : int(end_x), 'end_coords_y' : int(end_y)}
    return levelinfo

def readblock_gates(lines):
    gates = {}
    for line in lines:
        gatename, room, rx, ry, direction, targetgate, script = line.split()[1:]
        gate = lvlobj.gate(gatename, room, int(rx), int(ry), direction, targetgate, script)
        gates[gatename] = gate
    return gates

def readblock_messages(lines):
    messages = {}
    for line in lines:
        msgname, room, mx, my, color = line.split()[1:6]
        text = ' '.join(line.split()[6:])
        msg = lvlobj.message(room, int(mx), int(my), color, text)
        messages[msgname] = msg
    return messages


def readblock_room(lines):
    i = 0
    while i < len(lines):
        line = lines[i]
        if line[:6] == '*size ':
            room = lvlobj.room(int(line[6:].split()[0]), int(line[6:].split()[1]))
            i += 1
        elif line == '*walls':
            y = 0
            for j in range(room.getHeight()):
                i += 1
                line = lines[i]
                for x, w in enumerate(list(line)):
                    room.setTileType(x, y, w)
                y += 1
            i += 1
        elif line == '*symbols':
            y = 0
            for j in range(room.getHeight()):
                i += 1
                line = lines[i]
                for x, w in enumerate(list(line)):
                    room.setTileSymbol(x, y, w)
                y += 1
            i += 1
        elif line == '*colors_background':
            y = 0
            for j in range(room.getHeight()):
                i += 1
                line = lines[i]
                for x, w in enumerate(list(line)):
                    room.setTileBackground(x, y, w)
                y += 1
            i += 1
        elif line == '*colors_foreground':
            y = 0
            for j in range(room.getHeight()):
                i += 1
                line = lines[i]
                for x, w in enumerate(list(line)):
                    room.setTileForeground(x, y, w)
                y += 1
            i += 1
    return room

def readblock_rooms(lines):
    rooms = {}
    i = 0
    while i < len(lines)-1:
        line = lines[i]
        if line[:7] == '*!room ':
            roomname = line[7:]
            bs = i + 1
            while line[:9] != '*!roomend':
                i += 1
                line = lines[i]
            room = readblock_room(lines[bs:i])
            room.setName(roomname)
            rooms[roomname] = room
            i += 1
    return rooms
    
def import_level(levelfile):
    f = open(levelfile, 'r', encoding="utf-8")
    lines = f.readlines()
    for i in range(len(lines)):
        if lines[i][-1] == '\n':
            lines[i] = lines[i][:-1]
    i = 0
    reading = True
    messages = {}
    while reading:
        line = lines[i]
        if line[:8] == '*!start ':
            block = line[8:]
            bs = i + 1
            while line[:5] != '*!end':
                i += 1
                line = lines[i]
            if block == 'levelinfo':
                levelinfo = readblock_levelinfo(lines[bs:i])
            elif block == 'rooms':
                rooms = readblock_rooms(lines[bs:i])
            elif block == 'gates':
                gates = readblock_gates(lines[bs:i])
            elif block == 'messages':
                messages = readblock_messages(lines[bs:i])
        elif line[:9] == '*!endfile':
            reading = False
        i += 1
    level = lvlobj.level(levelinfo['name'], levelinfo['player_spawn_room'], levelinfo['player_spawn_coords_x'], levelinfo['player_spawn_coords_y'], levelinfo['end_room'], levelinfo['end_coords_x'], levelinfo['end_coords_y'])
    level.addRooms(rooms)
    level.addGates(gates)
    level.addMessages(messages)
    return level

