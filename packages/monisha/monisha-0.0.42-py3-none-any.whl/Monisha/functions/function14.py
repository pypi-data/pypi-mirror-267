import os, time
from ..scripts.es import Folder
from ..scripts.en import Scripted
#===========================================================================

async def CDirectory(dname=Folder.DATA07, fname=Scripted.DATA01):
    name01 = str(dname)
    name02 = str(fname)
    osemse = os.getcwd()
    moonse = os.path.join(osemse, name01, name02)
    foldes = moonse if os.path.isdir(moonse) else os.makedirs(moonse)
    return foldes

#===========================================================================

async def UDirectory(dname=Folder.DATA07, fname=Scripted.DATA01):
    name01 = str(dname)
    name02 = str(fname)
    osemse = os.getcwd()
    timeso = str(round(time.time()))
    moonse = os.path.join(osemse, name01, timeso, name02)
    foldes = moonse if os.path.isdir(moonse) else os.makedirs(moonse)
    return foldes

#===========================================================================

async def BDirectory(uid, dname=Folder.DATA07, fname=Scripted.DATA01):
    usered = str(uid)
    name01 = str(dname)
    name02 = str(fname)
    osemse = os.getcwd()
    timeso = str(round(time.time()))
    moonse = os.path.join(osemse, name01, usered, timeso, name02)
    foldes = moonse if os.path.isdir(moonse) else os.makedirs(moonse)
    return foldes

#===========================================================================
