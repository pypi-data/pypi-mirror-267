import os, time
from ..scripts.eo import Smbo
from ..scripts.es import Folder
from ..scripts.en import Scripted
#========================================================================

async def CDirectory(dname=Folder.DATA07):
    direos = str(dname)
    osemse = os.getcwd()
    moonse = os.path.join(osemse, direos) + Smbo.DATA03
    moonse if os.path.isdir(moonse) else os.makedirs(moonse)
    return moonse

#========================================================================

async def UDirectory(dname=Folder.DATA07):
    direos = str(dname)
    osemse = os.getcwd()
    timeso = str(round(time.time()))
    moonse = os.path.join(osemse, direos, timeso) + Smbo.DATA03
    moonse if os.path.isdir(moonse) else os.makedirs(moonse)
    return moonse

#========================================================================

async def BDirectory(uid, dname=Folder.DATA07):
    usered = str(uid)
    direos = str(dname)
    osemse = os.getcwd()
    timeso = str(round(time.time()))
    moonse = os.path.join(osemse, direos, usered, timeso) + Smbo.DATA03
    moonse if os.path.isdir(moonse) else os.makedirs(moonse)
    return moonse

#========================================================================
