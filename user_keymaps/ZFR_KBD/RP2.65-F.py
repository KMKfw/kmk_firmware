import board

import ulab.numpy as np
from kb import KMKKeyboard

from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.midi import MidiKeys
from kmk.modules.potentiometer import PotentiometerHandler

keyboard = KMKKeyboard()
keyboard.modules.append(Layers())
keyboard.modules.append(MidiKeys())


rgb = RGB(
    val_default=10,
    val_limit=100,  # out of 255
    pixel_pin=keyboard.rgb_pixel_pin,
    num_pixels=keyboard.rgb_num_pixels,
    refresh_rate=30,
    animation_speed=3,
    animation_mode=AnimationModes.STATIC,
)
keyboard.extensions.append(rgb)
keyboard.extensions.append(MediaKeys())

_______ = KC.TRNS
XXXXXXX = KC.NO

BASE_LAYER_IDX = 0
FN1_LAYER_IDX = 1
FN2_LAYER_IDX = 2
FN3_LAYER_IDX = 3
MIDI_LAYER_IDX = 4

FN1 = KC.MO(FN1_LAYER_IDX)
FN2 = KC.MO(FN2_LAYER_IDX)
FN3 = KC.MO(FN3_LAYER_IDX)
MIDI = KC.TG(MIDI_LAYER_IDX)

RGB_TOG = KC.RGB_TOG
RAINBOW = KC.RGB_MODE_RAINBOW


def get_kb_rgb_obj(keyboard):
    rgb = None
    for ext in keyboard.extensions:
        if type(ext) is RGB:
            rgb = ext
            break
    return rgb


keyboard.last_level = -1

# Gnome in Linux
level_steps = 17
level_inc_step = 1

# Windows 10
# level_steps = 100
# level_inc_step = 1

level_lut = [int(x) for x in np.linspace(0, level_steps, 64).tolist()]


def set_sys_vol(state):
    # convert to 0-100
    new_pos = int((state.position / 127) * 64)
    level = level_lut[new_pos]
    # print(f"new vol level: {level}")
    # print(f"last: {keyboard.last_level}")

    # check if uninitialized
    if keyboard.last_level == -1:
        keyboard.last_level = level
        return

    level_diff = abs(keyboard.last_level - level)
    if level_diff > 0:
        # set volume to new level
        # vol_direction = "unknown"
        if level > keyboard.last_level:
            # vol_direction = "up"
            cmd = KC.VOLU
        else:
            # vol_direction = "down"
            cmd = KC.VOLD
        # Send command  cmd to OS to up and down volume
        keyboard.tap_key(cmd)
        # print(f"Setting system volume {vol_direction} by {level_diff} to reach {level}")

        keyboard.last_level = level
    return


# LEDs Color or animation speed
hue_lut = [int(x) for x in np.linspace(0, 360, 127).tolist()]


def set_led_var(state):
    rgb = get_kb_rgb_obj(keyboard)
    if rgb is None:
        return

    if rgb.animation_mode == AnimationModes.STATIC:
        rgb.hue = hue_lut[state.position]
    else:
        rgb.animation_speed = int((state.position / 127) * 5)
    rgb._do_update()
    return


def set_led_brightness(state):
    rgb = get_kb_rgb_obj(keyboard)
    if rgb is None:
        return

    rgb.val = int((state.position / 127) * rgb.val_limit)
    rgb._do_update()
    return


def slider_1_handler(state):
    set_sys_vol(state)


# reserve middle four values - software detent
pb_lut = []
pb_lut[00:29] = [int(x) for x in np.linspace(0, 8192, 30).tolist()]
pb_lut[30:33] = [8192 for x in range(4)]  # midpoint - no bend
pb_lut[34:63] = [int(x) for x in np.linspace(8192, 8192 * 2, 30)]


def slider_2_handler(state):
    if keyboard.active_layers[0] == MIDI_LAYER_IDX:
        # use as MIDI Pitch wheel
        # use 64 values
        bend_idx = int((state.position / 127) * 64)
        bend = pb_lut[bend_idx]
        key = KC.MIDI_PB(bend)
        keyboard.tap_key(key)
    else:
        set_led_var(state)


keyboard.__midi_velocity = 0


def slider_3_handler(state):
    if keyboard.active_layers[0] == MIDI_LAYER_IDX:
        # use as MIDI note velocity
        keyboard.__midi_velocity = int((state.position / 127) * 127)
    else:
        set_led_brightness(state)


faders = PotentiometerHandler()
faders.pins = (
    (board.RV1, slider_1_handler, False),
    (board.RV2, slider_2_handler),
    (board.RV3, slider_3_handler),
)
keyboard.modules.append(faders)


def set_midi_vel(key, keyboard, *args):
    key.meta.velocity = keyboard.__midi_velocity
    return True


def MN(note: str):
    midi_keypress = KC.MIDI_NOTE(note, 1)
    midi_keypress.before_press_handler(set_midi_vel)
    return midi_keypress


# fmt:off
keyboard.keymap = [
    [   # Base Layer
        KC.ESC, KC.GRAVE,  KC.N1,    KC.N2,    KC.N3,    KC.N4,    KC.N5,    KC.N6,    KC.N7,    KC.N8,    KC.N9,    KC.N0,    KC.BSLS,  KC.DEL,     KC.MINS, KC.EQUAL,
             KC.TAB,       KC.Q,     KC.W,     KC.E,     KC.R,     KC.T,     KC.Y,     KC.U,     KC.I,     KC.O,     KC.P,     KC.BACKSPACE,         KC.LBRC, KC.RBRC,
             KC.LCTRL,     KC.A,     KC.S,     KC.D,     KC.F,     KC.G,     KC.H,     KC.J,     KC.K,     KC.L,     KC.SCLN,  KC.QUOT,  KC.ENTER,   KC.QUOT, KC.HOME,
             KC.LSFT,      KC.Z,     KC.X,     KC.C,     KC.V,     KC.B,     KC.N,     KC.M,     KC.COMM,  KC.DOT,   KC.SLSH,  KC.RSFT,      KC.UP,           KC.END,
                 FN1,      KC.LGUI,  KC.LALT,            KC.SPC,             KC.ENTER,           KC.RGUI,  KC.RALT,  FN2,          KC.LEFT,  KC.DOWN,  KC.RIGHT,
    ],

    [   # FN1 Layer
        _______, _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,    _______, _______,
             _______,      _______,  _______,  RGB_TOG,  RAINBOW,  _______,  _______,  _______,  _______,  _______,  _______,  _______,              _______, _______,
             _______,      _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,    _______, _______,
             _______,      _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,      _______,         _______,
             XXXXXXX,      _______,  _______,            _______,            _______,            _______,  _______,  FN3,          _______,  _______,  _______,
    ],

    [   # FN2 Layer
        _______, _______,  KC.F1,    KC.F2,    KC.F3,    KC.F4,    KC.F5,    KC.F6,    KC.F7,    KC.F8,    KC.F9,    KC.F10,   KC.F11,   KC.F12,     _______, _______,
             _______,      _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,              _______, _______,
             _______,      _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,    _______, _______,
             _______,      _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,      _______,         _______,
                 FN3,      _______,  _______,            _______,            _______,            _______,  _______,  XXXXXXX,      _______,  _______,  _______,
    ],

    [   # FN3 Layer
        _______, _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,    _______, _______,
             _______,      _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,              _______, _______,
             _______,      _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,    _______, _______,
             _______,      _______,  _______,  _______,  _______,  _______,  _______,  MIDI,     _______,  _______,  _______,  _______,      _______,         _______,
             XXXXXXX,      _______,  _______,            _______,            _______,            _______,  _______,  XXXXXXX,      _______,  _______,  _______,
    ],

    [   # MIDI Layer
          MIDI,  MN('E3'), MN('F#3'), MN('G#3'), MN('A#3'), XXXXXXX,  MN('C#4'), MN('D#4'), XXXXXXX,   MN('F#4'), MN('G#4'), MN('A#4'), MN('C5'), MN('C#5'),    _______, _______,
             _______,      MN('F3'),  MN('G3'),  MN('A3'),  MN('B3'), MN('C4'),  MN('D4'),  MN('E4'),  MN('F4'),  MN('G4'),  MN('A4'),  MN('B4'),               _______, _______,
             _______,      XXXXXXX,   MN('C#2'), MN('D#2'), XXXXXXX,  MN('F#2'), MN('G#2'), MN('A#2'), XXXXXXX,   MN('C#3'), MN('D#3'), XXXXXXX,  _______,      _______, _______,
             _______,      MN('B1'),  MN('C2'),  MN('D2'),  MN('E2'), MN('F2'),  MN('G2'),  MN('A2'),  MN('B2'),  MN('C3'),  MN('D3'),  MN('E3'),      _______,         _______,
             XXXXXXX,      _______,   _______,              _______,             _______,              _______,   _______,   XXXXXXX,        _______,  _______,  _______,
    ],
]
# fmt:on


if __name__ == '__main__':
    keyboard.go()
