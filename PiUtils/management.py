# -*- coding: utf-8 -*-

import subprocess
import commands
import os

from thirtybirds_2_0.Updates.manager import init as updates_init
from thirtybirds_2_0.Network.info import init as network_info_init


class Management(object):
    def __init__(self, hostname):
        self.hostname = hostname

    def system_reboot(self):
        try:
            os.system("sudo reboot now")
            return True
        except Exception:
            return False

    def system_shutdown(self):
        try:
            os.system("sudo shutdown -h now")
            return True
        except Exception:
            return False

    def get_system_temp(self):
        try:
            return float(commands.getstatusoutput("/opt/vc/bin/vcgencmd measure_temp")[1][5:-2])
        except Exception:
            return False
        
    def get_system_cpu(self):
        try:
            bash_output = commands.getstatusoutput("uptime")[1]
            split_output = bash_output.split(" ")
            return split_output[12]
        except Exception:
            return False

    def get_system_uptime(self):
        try:
            bash_output = commands.getstatusoutput("uptime")[1]
            split_output = bash_output.split(" ")
            return split_output[4]
        except Exception:
            return False

    def get_system_disk(self): 
        #disk_free = commands.getstatusoutput("df -h | awk '$NF=="/"{printf "%d", $3}'")[1]
        return 0

    def get_git_timestamp(self, repo_name):
        try:
            repo_path = '/home/pi/{}'.format(repo_name)
            return commands.getstatusoutput("cd {}; git log -1 --format=%cd".format(repo_path))[1]   
        except Exception:
            return False

    def git_pull(self, repo_name):
        try:
            repo_path = '/home/pi/{}'.format(repo_name)
            return commands.getstatusoutput("cd={}; git pull".format(repo_path))[1]
        except Exception:
            return False

    def scripts_update(self, repo_name):
        try:
            repo_path = '/home/pi/{}'.format(repo_name)
            updates_init(repo_path, False, True)
            return True
        except Exception:
            return False

    def get_scripts_version(self, repo_name):
        try:
            repo_path = '/home/pi/{}'.format(repo_name)
            (updates, ghStatus, bsStatus) = updates_init(repo_path, False, False)
            return updates.read_version_pickle()
        except Exception:
            return False

    def get_system_status(self, repo_name):
        return (
            self.hostname, 
            self.get_scripts_version(repo_name), 
            self.get_git_timestamp(repo_name), 
            self.get_system_temp(), 
            self.get_system_cpu(), 
            self.get_system_uptime(), 
            self.get_system_disk()
        )

def init():
    network_info = network_info_init()
    hostname = network_info.getHostName()
    management = Management(hostname)
    return management
