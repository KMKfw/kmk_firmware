import adafruit_midi
import usb_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.program_change import ProgramChange
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop

from kmk.handlers.stock import passthrough as handler_passthrough
from kmk.keys import KC, make_argumented_key
from kmk.modules import Module


class midiNoteValidator:
    def __init__(self, note=69, velocity=64, channel=None):
        self.note = note
        self.velocity = velocity
        self.channel = channel


class MidiKeys(Module):
    def __init__(self):

        try:
            self.midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
        except IndexError:
            self.midi = None
            # if debug_enabled:
            print('No midi device found.')

            KC._generators.append(self.maybe_make_midi_key())

    def maybe_make_midi_key(self):
        keys = (
            (('MIDI_CC',), ControlChange),
            (('MIDI_PB',), PitchBend),
            (('MIDI_PC',), ProgramChange),
            (('MIDI_START',), Start),
            (('MIDI_STOP',), Stop),
        )
        note = ('MIDI_NOTE',)

        def closure(candidate):
            if candidate in note:
                return make_argumented_key(
                    names=('MIDI_NOTE',),
                    validator=midiNoteValidator,
                    on_press=self.note_on,
                    on_release=self.note_off,
                )
            for names, validator in keys:
                if candidate in names:
                    return make_argumented_key(
                        names=names,
                        validator=validator,
                        on_press=self.on_press,
                        on_release=handler_passthrough,
                    )

        return closure

    def during_bootup(self, keyboard):
        return None

    def before_matrix_scan(self, keyboard):
        return None

    def after_matrix_scan(self, keyboard):
        return None

    def process_key(self, keyboard, key, is_pressed, int_coord):
        return key

    def before_hid_send(self, keyboard):
        return None

    def after_hid_send(self, keyboard):
        return None

    def on_powersave_enable(self, keyboard):
        return None

    def on_powersave_disable(self, keyboard):
        return None

    def send(self, message):
        if self.midi:
            self.midi.send(message)

    def on_press(self, key, keyboard, *args, **kwargs):
        self.send(key.meta)

    def note_on(self, key, keyboard, *args, **kwargs):
        self.send(NoteOn(key.meta.note, key.meta.velocity, channel=key.meta.channel))

    def note_off(self, key, keyboard, *args, **kwargs):
        self.send(NoteOff(key.meta.note, key.meta.velocity, channel=key.meta.channel))
