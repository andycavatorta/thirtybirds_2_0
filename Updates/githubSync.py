import commands

def main(path_str):
    cmd = "cd %s && git pull -q --all -p" % (path_str)
    print cmd
    code, msg = commands.getstatusoutput(cmd)
    return (code, msg, "common/githubSync.main")