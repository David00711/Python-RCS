import pymem
import pymem.process
import time
import math
import keyboard
from os import _exit
import requests


offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(offsets).json()


m_iShotsFired = int(response["netvars"]["m_iShotsFired"])
m_aimPunchAngle = int(response["netvars"]["m_aimPunchAngle"])
dwClientState_ViewAngles = int(response["signatures"]["dwClientState_ViewAngles"])
dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
dwClientState_ViewAngles = int(response["signatures"]["dwClientState_ViewAngles"])


pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll


def checkangles(x, y):
    if x > 89:
        return False
    elif x < -89:
        return False
    elif y > 360:
        return False
    elif y < -360:
        return False
    else:
        return True


def nanchecker(first, second):
    if math.isnan(first) or math.isnan(second):
        return False
    else:
        return True


def main():
    print('rcs is running')
    if pm.read_uint(player + m_iShotsFired) > 2:
        rcs.x = pm.read_float(engine_pointer + dwClientState_ViewAngles)
        rcs.y = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
        punch.x = pm.read_float(player + m_aimPunchAngle)
        punch.y = pm.read_float(player + m_aimPunchAngle + 0x4)
        newrcs.x = rcs.x - (punch.x - oldpunch.x) * 2
        newrcs.y = rcs.y - (punch.y - oldpunch.y) * 2
        oldpunch.x = punch.x
        oldpunch.y = punch.y
        if nanchecker(newrcs.x, newrcs.y) and checkangles(newrcs.x, newrcs.y):
            pm.write_float(engine_pointer + dwClientState_ViewAngles, newrcs.x)
            pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, newrcs.y)
    else:
        oldpunch.x = 0.0
        oldpunch.y = 0.0
        newrcs.x = 0.0
        newrcs.y = 0.0
    if keyboard.is_pressed('delete'):
        _exit(0)


if __name__ == '__main__':
    main()

    
