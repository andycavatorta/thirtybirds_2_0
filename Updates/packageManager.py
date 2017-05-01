import commands
import json
import os
import pickle
import sys

BASE_PATH = False
DATA_PATH = False
BASHLOG_PATH = False
COMMON_PATH = False
ERRORLOGGER = False


def bashLogger(version,msg):
    path = "%s%s"%(BASHLOG_PATH,"bash.log")
    line = "echo %s, %s >> %s" % (version,msg.replace('"','\\"'),path)
    commands.getstatusoutput(line)
    print repr(path)

def runBashScripts(versionFromPickle):
    import upgradeScripts
    v_l =  upgradeScripts.scripts.keys()
    v_l.sort(key=float)
    for version in v_l:
        if float(version) >= versionFromPickle:
            for script in upgradeScripts.scripts[version]:
                runBashCommand(version, script)
                #bashLogger(version, script)
                #bashLogger(version, commands.getstatusoutput(script))
    return float(version)

def versionPickle(version=None):
    picklePath = "%s%s" % (DATA_PATH, "version.pickle")
    # create file if it doesn't exist
    if os.path.isfile(picklePath):
        if version:
            pickle.dump(float(version),open(picklePath, "wb"))
        else:
            return pickle.load(open(picklePath, "r"))
    else:
        pfile = open(picklePath, "wb")
        version = 0.01
        pickle.dump(version, pfile)
        return version

def githubSync():
    cmd = "cd %s && git pull -q --all -p" % (BASE_PATH)
    runBashCommand(0,cmd)

def runBashCommand(v,cmd):
    status, output = commands.getstatusoutput(cmd)
    bashLogger(v, cmd)
    bashLogger(v, output)

def update(basePath, dataPath, bashLogPath, commonPath, errorlogger):
    global BASE_PATH
    BASE_PATH = basePath
    global DATA_PATH
    DATA_PATH = dataPath
    global BASHLOG_PATH
    BASHLOG_PATH = bashLogPath
    global COMMON_PATH
    COMMON_PATH = commonPath

    global ERRORLOGGER
    ERRORLOGGER = errorlogger
    sys.path.append(COMMON_PATH)
    # fetch latest code from GitHub
    githubSync()
    version = versionPickle()
    latestVersion = runBashScripts(version)
    versionPickle(latestVersion)
    #reset()

def reset(version=0.01):
    versionPickle(version) # reset to the beginning
