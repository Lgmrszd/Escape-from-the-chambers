def script(lvl, room, gx, gy):
    rslt = False
    if 'stage' not in lvl.getOtherData().keys():
        lvl.updateOtherData({'stage': 0})
        lvl.setStartRoom(room)
        lvl.setSpawnCoords(gx, gy)
    if 'circles' not in lvl.getOtherData().keys():
        lvl.updateOtherData({'circles': 0})
        lvl.setStartRoom(room)
        lvl.setSpawnCoords(gx, gy)
    
    if lvl.getOtherData()['stage'] == 1:
        rslt = True
        lvl.updateOtherData({'stage': 2})
        lvl.setStartRoom(room)
        lvl.setSpawnCoords(gx, gy)

    if (lvl.getOtherData()['circles'] == 3):
        lvl.updateOtherData({'stage': 1})
        rslt = True
        lvl.setStartRoom(room)
        lvl.setSpawnCoords(gx, gy)
        
        ggg = lvl.getGateByName('c1top')
        ggg.setTarget('arm1down')
        lvl.replaceGate(ggg)
        
        ggg = lvl.getGateByName('c4right')
        ggg.setTarget('arm1left')
        lvl.replaceGate(ggg)

    return rslt, lvl
