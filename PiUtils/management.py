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

    def get_core_temp(self):
        try:
            return float(commands.getstatusoutput("/opt/vc/bin/vcgencmd measure_temp")[1][5:-2])
        except Exception:
            return False

    def get_core_voltage(self):
        try:
            return float(commands.getstatusoutput("/opt/vc/bin/vcgencmd measure_volts core")[1])
            # ^ not formatted yet
        except Exception:
            return False


    def get_system_cpu(self):
        try:
            #top -n1 | awk '/Cpu\(s\):/ {print $2}'
            bash_output = commands.getstatusoutput("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'")[1]
            return float(bash_output)
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
        try: 
            text_block_str = commands.getstatusoutput("df -h")[1]
            text_block_l = text_block_str.split("\n")
            for line in text_block_l:
                if line.startswith("/dev/sda2") or line.startswith("/dev/root"):
                    return line.split()[3]
            return ""
        except Exception:
            return ""

    def get_wifi_strength(self):
        text_block_str = commands.getstatusoutput("iwconfig")[1]
        text_block_l = text_block_str.split("\n")
        for line in text_block_l:
            try:
                start_postion = line.index("Link Quality")
                return int(line.split("Link Quality=")[1][:2])
            except ValueError:
                pass
        return -1

    def get_memory_free(self):
        try:
            text_block_str = commands.getstatusoutput("cat /proc/meminfo")[1]
            text_block_l = text_block_str.split("\n")
            for line in text_block_l:
                if line.startswith("MemFree:"):
                    line_l = line.split()
                    kb = float(line_l[1])
                    mb = kb/1000.0
                    return mb
            return "-1.0"
        except Exception:
            return "-1.0"

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
        report = {
            "hostname":self.hostname,
            "scripts_version":self.get_scripts_version(repo_name),
            "git_timestamp":self.get_git_timestamp(repo_name),
            "system_uptime":self.get_system_uptime(),
            "system_cpu":self.get_system_cpu(),
            "memory_free":self.get_memory_free(),
            "system_disk":self.get_system_disk(),
            "core_temp":self.get_core_temp(),
            "wifi_strength":self.get_wifi_strength()
        }
        return report

def init():
    network_info = network_info_init()
    hostname = network_info.getHostName()
    management = Management(hostname)
    return management
