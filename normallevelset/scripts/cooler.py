
def script(lvl, room, gx, gy):
    ggg = lvl.getGateByName('room2gate1')
    ggg.setTarget('hroom1gate')
    lvl2 = lvl
    lvl2.replaceGate(ggg)
    print('THIS GATE IN ROOM ', room)
    lvl2.setStartRoom(room)
    lvl2.setSpawnCoords(gx, gy)
    print(lvl2.getStartRoom())
    rslt = True
    return rslt, lvl2
