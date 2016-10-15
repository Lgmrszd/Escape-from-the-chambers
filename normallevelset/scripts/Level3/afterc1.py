def script(lvl, room, gx, gy):
    rslt = False
    if 'stage' not in lvl.getOtherData().keys():
        lvl.updateOtherData({'stage': 1})
        
        ggg = lvl.getGateByName('c1top')
        ggg.setTarget('rm1down')
        lvl.replaceGate(ggg)
        
        ggg = lvl.getGateByName('c4right')
        ggg.setTarget('rm1left')
        lvl.replaceGate(ggg)
        
        print('THIS GATE IN ROOM ', room)
        lvl.setStartRoom(room)
        lvl.setSpawnCoords(gx, gy)
        print(lvl.getStartRoom())
        rslt = True
        
    if 'circles' not in lvl.getOtherData().keys():
        lvl.updateOtherData({'circles': 0})
    
    if (lvl.getOtherData()['stage'] == 0) and (lvl.getOtherData()['circles'] == 0):
        lvl.updateOtherData({'stage': 1})
        rslt = True
        lvl.setStartRoom(room)
        lvl.setSpawnCoords(gx, gy)
        
        ggg = lvl.getGateByName('c1top')
        ggg.setTarget('rm1down')
        lvl.replaceGate(ggg)
        
        ggg = lvl.getGateByName('c4right')
        ggg.setTarget('rm1left')
        lvl.replaceGate(ggg)
    
    if lvl.getOtherData()['stage'] == 4:
        rslt = True
        lvl.updateOtherData({'stage': 1})
        lvl.updateOtherData({'circles': lvl.getOtherData()['circles'] + 1})
        lvl.setStartRoom(room)
        lvl.setSpawnCoords(gx, gy)

    return rslt, lvl
