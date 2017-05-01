"""
This module is the VIrtual MIdi Network Adapter.
It 
1) creates virtual midi devices in the host OS
2) discovers and connects to a Nervebox server
3) catpures midi events and converts them to OSC
4) sends osc messages to Nervebox server (if connected)
"""

#############################################
##### MODULES, EVENIRONMENT AND GLOBALS #####
#############################################

import json
import math
import os
import rtmidi  #https://github.com/SpotlightKid/python-rtmidi
import socket
import sys
import datetime
import imp

BASE_PATH = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
CLIENT_PATH = "%s/client/" % (BASE_PATH )
DEVICES_PATH = "%s/client/devices/" % (BASE_PATH )
print "vimina ok"

import midiToOsc
import dps
###############################
##### VITUAL MIDI DEVICES #####
###############################

deviceNames = filter(lambda x: os.path.isdir(os.path.join(DEVICES_PATH, x)), os.listdir(DEVICES_PATH))
instrumentNames = []

statusMap = {
    128:"note_off",
    144:"note_on",
    160:"polyphonic_aftertouch",
    176:"control_change",
    192:"program_change",
    208:"channel_aftertouch",
    224:"pitch_wheel",
    240:"system_exclusive",
    241:"system_common",
    242:"song_position_pointer",
    243:"song_select",
    244:"system_common",
    245:"system_common",
    246:"tune_request",
    247:"end_of_sysex",
    248:"timing_clock",
    249:"undefined",
    250:"start",
    251:"continue",
    252:"stop",
    253:"undefined",
    254:"active_sensing",
    255:"sys_reset",
}


def midiEventCallback(devicename, msgAndTime_t, data=None):
    print "vimina/main midiEventCallback", devicename, msgAndTime_t, data
    event, deltatime = msgAndTime_t

    if event[0] < 0xF0:
        channel = (event[0] & 0xF) + 1
        status_int = event[0] & 0xF0
    else:
        status_int = event[0]
        channel = None
    status = statusMap[int(status_int)]
    data1 = data2 = None
    num_bytes = len(event)
    if num_bytes >= 2:
        data1 = event[1]
    if num_bytes >= 3:
        data2 = event[2]

    osc_msg = midiToOsc.convert(devicename, status, channel, data1, data2) # convert MIDI so OSC
    print osc_msg
    dps.pubsub_api["publish"](devicename, osc_msg)

# following MIDI functions should be moved into common module
def createVirtualPort(devicename):
    print devicename
    midiin = rtmidi.MidiIn()
    vp = midiin.open_virtual_port(devicename)
    midiin.set_callback((lambda event, data: midiEventCallback(devicename, event, data)))
    return vp

for device in deviceNames:
    SPECIFIC_PATH =  "%s/client/devices/%s" % (BASE_PATH,device)
    instruments = imp.load_source('mapping', '%s/mapping.py'%(SPECIFIC_PATH))
    for subinstrument in instruments.instruments:
        instrumentname = "%s%s" % (device, subinstrument)
        instrumentNames.append(instrumentname)


virtualPorts = map(createVirtualPort, instrumentNames)
print virtualPorts
