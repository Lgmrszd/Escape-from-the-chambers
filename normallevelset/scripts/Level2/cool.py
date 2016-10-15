
def script(lvl, room, gx, gy):
    if 'cool' not in lvl.getOtherData().keys():
        lvl.updateOtherData({'cool': 0})
    lvl.updateOtherData({'cool': lvl.getOtherData()['cool'] + 1})
    if lvl.getOtherData()['cool'] > 3:
        pass
        
    else:
        ggg = lvl.getGateByName('room2gate1')
        ggg.setTarget('hroom1gate')
        lvl.replaceGate(ggg)
        print('THIS GATE IN ROOM ', room)
        lvl.setStartRoom(room)
        lvl.setSpawnCoords(gx, gy)
        print(lvl.getStartRoom())
        rslt = True
    return rslt, lvl
