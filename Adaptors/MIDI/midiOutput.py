import mido
import numbers

class Midi_Output():
    def __init__(self):
        #self.error_logger = error_logger
        oNames = mido.get_output_names()
        
        self.midi_out = mido.open_output(oNames[0])


    def send_midi(self, params, status, channel, data1=None, data2=None):
        if status == "note_on": # channel, pitch, velocity
            # data1 is None, int, or {use_variable, scaling_factor, offset_factor}
            pitch = None
            pitchbend = None
            velocity = None
            if data1 is None: # get pitch data from params
                pitch = params["pitch"]["midi"]
                if params["pitch"]["cents"] != 0.0:
                    pitchbend = (data1 * 127 / 200) + 64
            elif isinstance(data1, numbers.Real):
                pitch = data1
            elif isinstance(data1, dict):
                if data1["use_variable"] == "octave":
                    pitch = params["pitch"]["octave"]
                elif data1["use_variable"] == "cents":
                    pitch = params["pitch"]["cents"]
                elif data1["use_variable"] == "freq":
                    pitch = params["pitch"]["freq"]
                elif data1["use_variable"] == "midi":
                    pitch = params["pitch"]["midi"]
                elif data1["use_variable"] == "amplitude":
                    pitch = params["dynamics"]["amplitude"]
                elif data1["use_variable"] == "pressure":
                    pitch = params["dynamics"]["pressure"]
                elif data1["use_variable"] == "data1":
                    pitch = data1
                elif data1["use_variable"] == "data2":
                    pitch = data2
                else:
                    return
                if offset_factor is not None:
                    pitch = velocity + offset_factor
                if scaling_factor is not None:
                    pitch = velocity * scaling_factor
            else:
                return
            if data2 is None: # get amplitude data from params
                velocity = params["dynamics"]["amplitude"]*127
                print 'VELOCITY ', velocity
            elif isinstance(data1, numbers.Real):
                velocity = data2
            elif isinstance(data2, dict):
                if data2["use_variable"] == "octave":
                    velocity = params["pitch"]["octave"]
                elif data2["use_variable"] == "cents":
                    velocity = params["pitch"]["cents"]
                elif data2["use_variable"] == "freq":
                    velocity = params["pitch"]["freq"]
                elif data2["use_variable"] == "midi":
                    velocity = params["pitch"]["midi"]
                elif data2["use_variable"] == "amplitude":
                    velocity = params["dynamics"]["amplitude"]
                elif data2["use_variable"] == "pressure":
                    velocity = params["dynamics"]["pressure"]
                elif data2["use_variable"] == "data1":
                    velocity = data1
                elif data2["use_variable"] == "data2":
                    velocity = data2
                else:
                    return
                if offset_factor is not None:
                    velocity = velocity + offset_factor
                if scaling_factor is not None:
                    velocity = velocity * scaling_factor
            else:
                return
            if pitch is not None and velocity is not None:
                self.midi_out.send(mido.Message('note_on', channel=int(channel), note=int(pitch), velocity=int(velocity)))
            if pitchbend is not None:
                self.midi_out.send(mido.Message('pitchwheel', channel=channel, pitch=pitchbend))

        if status == "note_off": # channel, pitch, velocity
            # data1 is None, int, or {use_variable, scaling_factor, offset_factor}
            pitch = None
            pitchbend = None
            velocity = None
            if data1 is None: # get pitch data from params
                velocity = params["pitch"]["midi"]
                if params["pitch"]["cents"] != 0:
                    pitchbend = (data1 * 127 / 200) + 64
            elif isinstance(data1, numbers.Real):
                pitch = data1
            elif isinstance(data1, dict):
                if data1["use_variable"] == "octave":
                    pitch = params["pitch"]["octave"]
                elif data1["use_variable"] == "cents":
                    pitch = params["pitch"]["cents"]
                elif data1["use_variable"] == "freq":
                    pitch = params["pitch"]["freq"]
                elif data1["use_variable"] == "midi":
                    pitch = params["pitch"]["midi"]
                elif data1["use_variable"] == "amplitude":
                    pitch = params["dynamics"]["amplitude"]
                elif data1["use_variable"] == "pressure":
                    pitch = params["dynamics"]["pressure"]
                elif data1["use_variable"] == "data1":
                    pitch = data1
                elif data1["use_variable"] == "data2":
                    pitch = data2
                else:
                    return
                if offset_factor is not None:
                    pitch = velocity + offset_factor
                if scaling_factor is not None:
                    pitch = velocity * scaling_factor
            else:
                return
            if pitch is not None:
                self.midi_out.send(mido.Message('note_off', channel=channel, note=pitch, velocity=0))

        if status == "polyphonic_aftertouch": # channel, pitch, pressure
            self.midi_out.send(mido.Message('polytouch', channel=channel, note=data1, value=data2))

        if status == "control_change": # channel
            print channel
            self.midi_out.send(mido.Message('control_change', channel=int(channel), control=int(data1), value=int(data2)))

        if status == "program_change": # channel, program
            self.midi_out.send(mido.Message('program_change', channel=channel, program=data1))

        if status == "channel_aftertouch": # channel, pressure
            self.midi_out.send(mido.Message('aftertouch', channel=channel, value=data1))

        if status == "pitch_wheel": # channel, 
            self.midi_out.send(mido.Message('pitchwheel', channel=channel, pitch=data1))

        if status == "sysex": # channel, 
            self.midi_out.send(mido.Message('sysex', data=data1))

        if status == "song_position_pointer": # channel, 
            self.midi_out.send(mido.Message('songpos', pos=data1))

        if status == "song_select": # channel, 
            self.midi_out.send(mido.Message('song_select', pos=data1))

        if status in ["tune_request"]: # channel
            self.midi_out.send(mido.Message('tune_request'))

        if status in ["timing_clock"]: # channel
            self.midi_out.send(mido.Message('clock'))

        if status in ["start"]: # channel
            self.midi_out.send(mido.Message('start'))

        if status in ["continue"]: # channel
            self.midi_out.send(mido.Message('continue'))

        if status in ["stop"]: # channel
            self.midi_out.send(mido.Message('stop'))

        if status in ["active_sensing"]: # channel
            self.midi_out.send(mido.Message('active_sensing'))

        if status in ["sys_reset"]: # channel
            self.midi_out.send(mido.Message('reset'))
