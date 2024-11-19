import adafruit_midi
import usb_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.program_change import ProgramChange
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop

from kmk.keys import Key, make_argumented_key
from kmk.modules import Module
from kmk.utils import Debug

debug = Debug(__name__)


class MidiKey(Key):
    def __init__(self, *args, command, channel=None, **kwargs):
        super().__init__(**kwargs)
        self.on_press_msg = command(*args, channel=channel)
        self.on_release_msg = None


def midi_note_key(note=69, velocity=127, channel=None, **kwargs):
    key = MidiKey(note, velocity, command=NoteOn, channel=channel, **kwargs)
    key.on_release_msg = NoteOff(note, velocity, channel=channel)
    return key


class MidiKeys(Module):
    def __init__(self):
        make_argumented_key(
            names=('MIDI_CC',),
            constructor=MidiKey,
            command=ControlChange,
            on_press=self.on_press,
        )

        make_argumented_key(
            names=('MIDI_NOTE',),
            constructor=midi_note_key,
            on_press=self.on_press,
            on_release=self.on_release,
        )

        make_argumented_key(
            names=('MIDI_PB',),
            constructor=MidiKey,
            command=PitchBend,
            on_press=self.on_press,
        )

        make_argumented_key(
            names=('MIDI_PC',),
            constructor=MidiKey,
            command=ProgramChange,
            on_press=self.on_press,
        )

        make_argumented_key(
            names=('MIDI_START',),
            constructor=MidiKey,
            command=Start,
            on_press=self.on_press,
        )

        make_argumented_key(
            names=('MIDI_STOP',),
            constructor=MidiKey,
            command=Stop,
            on_press=self.on_press,
        )

        try:
            self.midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
        except IndexError:
            self.midi = None
            if debug.enabled:
                debug('No midi device found.')

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
        self.send(key.on_press_msg)

    def on_release(self, key, keyboard, *args, **kwargs):
        self.send(key.on_release_msg)
