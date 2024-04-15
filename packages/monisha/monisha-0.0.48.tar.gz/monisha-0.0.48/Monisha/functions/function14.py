import os, time
from ..scripts.eo import Smbo
from ..scripts.es import Folder
from ..scripts.en import Scripted
#========================================================================================

async def CDirectory(dname=Folder.DATA07, fname=None):
    name01 = str(dname)
    name02 = str(fname)
    osemse = os.getcwd()
    moonse = os.path.join(osemse, name01)
    moonse if os.path.isdir(moonse) else os.makedirs(moonse)
    moonue = moonse + Smbo.DATA03 if fname == None else moonse + Smbo.DATA03 + name02
    return moonue

#========================================================================================

async def UDirectory(dname=Folder.DATA07, fname=None):
    name01 = str(dname)
    name02 = str(fname)
    osemse = os.getcwd()
    timeso = str(round(time.time()))
    moonse = os.path.join(osemse, name01, timeso)
    moonse if os.path.isdir(moonse) else os.makedirs(moonse)
    moonue = moonse + Smbo.DATA03 if fname == None else moonse + Smbo.DATA03 + name02
    return moonue

#========================================================================================

async def BDirectory(uid, dname=Folder.DATA07, fname=None):
    usered = str(uid)
    name01 = str(dname)
    name02 = str(fname)
    osemse = os.getcwd()
    timeso = str(round(time.time()))
    moonse = os.path.join(osemse, name01, usered, timeso)
    moonse if os.path.isdir(moonse) else os.makedirs(moonse)
    moonue = moonse + Smbo.DATA03 if fname == None else moonse + Smbo.DATA03 + name02
    return moonue

#========================================================================================
