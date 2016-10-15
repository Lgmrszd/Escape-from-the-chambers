def script(lvl, room, gx, gy):
    rslt = False
    if 'stage' not in lvl.getOtherData().keys():
        lvl.updateOtherData({'stage': 0})
    if 'circles' not in lvl.getOtherData().keys():
        lvl.updateOtherData({'circles': 0})
    
    if lvl.getOtherData()['stage'] == 2:
        rslt = True
        lvl.updateOtherData({'stage': 3})
        lvl.setStartRoom(room)
        lvl.setSpawnCoords(gx, gy)

    return rslt, lvl
