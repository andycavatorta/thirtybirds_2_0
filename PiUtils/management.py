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
        os.system("reboot now")

    def system_shutdown(self):
        os.system("shutdown -h now")

    def system_temp(self):
        return commands.getstatusoutput("/opt/vc/bin/vcgencmd measure_temp")[1]

    def system_cpu(self):
        bash_output = commands.getstatusoutput("uptime")[1]
        split_output = bash_output.split(" ")
        return split_output[12]

    def system_uptime(self):
        bash_output = commands.getstatusoutput("uptime")[1]
        split_output = bash_output.split(" ")
        return split_output[4]

    def system_disk(self): 
        #disk_free = commands.getstatusoutput("df -h | awk '$NF=="/"{printf "%d", $3}'")[1]
        return 0

    def git_get_timestamp(self, repo_name):
        repo_path = '/home/pi/{}'.format(repo_name)
        return commands.getstatusoutput("cd {}; git log -1 --format=%cd".format(repo_path))[1]   

    def git_pull(self, repo_name):
        repo_path = '/home/pi/{}'.format(repo_name)
        subprocess.call(['sudo', 'git', 'pull'], cwd=repo_path)
        return 

    def scripts_update(self, repo_name):
        repo_path = '/home/pi/{}'.format(repo_name)
        updates_init(repo_path, False, True)
        return

    def scripts_get_version(self, repo_name):
        repo_path = '/home/pi/{}'.format(repo_name)
        (updates, ghStatus, bsStatus) = updates_init(repo_path, False, False)
        return updates.read_version_pickle()

    def report_system_status(self, repo_name):
        return (self.hostname, self.scripts_get_version(repo_name), self.git_get_timestamp(repo_name), self.system_temp(), self.system_cpu(), self.system_uptime(), self.system_disk())

def init():
    network_info = network_info_init()
    hostname = network_info.getHostName()
    management = Management(hostname)
    return management
