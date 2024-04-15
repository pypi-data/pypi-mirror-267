import os, time
from ..scripts.es import Folder
from ..scripts.en import Scripted
#===========================================================================

async def CDirectory(dname=Folder.DATA07, fname=Scripted.DATA01):
    name01 = str(dname)
    name02 = str(fname)
    osemse = os.getcwd()
    rooted = Scripted.DATA01
    moonse = os.path.join(osemse, name01, rooted) + name02
    moonse if os.path.isdir(moonse) else os.makedirs(moonse)
    return moonse

#===========================================================================

async def UDirectory(dname=Folder.DATA07, fname=Scripted.DATA01):
    name01 = str(dname)
    name02 = str(fname)
    osemse = os.getcwd()
    rooted = Scripted.DATA01
    timeso = str(round(time.time()))
    moonse = os.path.join(osemse, name01, timeso, rooted) + name02
    moonse if os.path.isdir(moonse) else os.makedirs(moonse)
    return moonse

#===========================================================================

async def BDirectory(uid, dname=Folder.DATA07, fname=Scripted.DATA01):
    usered = str(uid)
    name01 = str(dname)
    name02 = str(fname)
    osemse = os.getcwd()
    rooted = Scripted.DATA01
    timeso = str(round(time.time()))
    moonse = os.path.join(osemse, name01, usered, timeso, rooted) + name02
    moonse if os.path.isdir(moonse) else os.makedirs(moonse)
    return moonse

#===========================================================================
