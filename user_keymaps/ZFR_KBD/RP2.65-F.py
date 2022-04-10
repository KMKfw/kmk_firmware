import board


from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.consumer_control import ConsumerControl
import usb_hid

from kb import KMKKeyboard

from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.modules.potentiometer import PotentiometerHandler
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()
keyboard.modules.append(Layers())

# 
rgb_ext = RGB(
    val_default=10, val_limit=100, # out of 255
    pixel_pin=keyboard.rgb_pixel_pin, num_pixels=keyboard.rgb_num_pixels,
    refresh_rate=30, animation_speed=3,
    animation_mode=AnimationModes.STATIC)
keyboard.extensions.append(rgb_ext)

_______ = KC.TRNS
XXXXXXX = KC.NO

FN1 = KC.MO(1)
FN2 = KC.MO(2)
FN3 = KC.MO(3)
MIDI = KC.TG(4)

RGB_TOG = KC.RGB_TOG
RAINBOW = KC.RGB_MODE_RAINBOW

cc = ConsumerControl(usb_hid.devices)
# keyboard.level_lock = 0
keyboard.last_level = 0

level_steps = 17

# System volume
def slider_1_handler(state):
    # print(f"slider 1 state: {state}")
    
    # if keyboard.level_lock == 1:
    #     return

    # convert to 0-100
    level = int((state['position'] / 127) * level_steps)
    last_level = keyboard.last_level
    # print(f"new vol level: {level}")
    # print(f"last: {keyboard.last_level}")

    level_diff = abs(last_level - level)
    
    if level_diff > 1:
        # keyboard.level_lock = 1
        
        # print(f"Volume change: {level_diff}")

        # set volume to new level
        vol_direction = "unknown"
        if state['direction'] == 1:
            vol_direction = "up"
            cmd = ConsumerControlCode.VOLUME_INCREMENT
        else:
            vol_direction = "down"
            cmd = ConsumerControlCode.VOLUME_DECREMENT
        
        # print(f"Setting system volume {vol_direction} by {level_diff}")
        for i in range(level_diff):
            cc.send(cmd)

        keyboard.last_level = level
        # keyboard.level_lock = 0

    return

# LEDs Color or animation speed
def slider_2_handler(state):
    rgb = None
    for ext in keyboard.extensions:
        if type(ext) is RGB:
            rgb = ext
            break
    if rgb is None:
        return
    if rgb.animation_mode == AnimationModes.STATIC:
        rgb.hue = int((state['position'] / 127) * 359)
    else:
        rgb.animation_speed = int((state['position'] / 127) * 5)
    rgb._do_update()
    return

# Keyboard Brightness
def slider_3_handler(state):
    rgb = None
    for ext in keyboard.extensions:
        if type(ext) is RGB:
            rgb = ext
            break
    if rgb is None:
        return

    rgb.val = int((state['position'] / 127) * rgb.val_limit)
    rgb._do_update()
    return

faders = PotentiometerHandler()
faders.pins = (
    (board.RV1, slider_1_handler, False),
    (board.RV2, slider_2_handler),
    (board.RV3, slider_3_handler),
)
keyboard.modules.append(faders)


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
             XXXXXXX,      _______,  _______,            _______,            _______,            _______,  _______,  FN2,          _______,  _______,  _______,
    ],
    
    [   # FN2 Layer
        _______, _______,  KC.F1  ,  KC.F2  ,  KC.F3  ,  KC.F4  ,  KC.F5  ,  KC.F6  ,  KC.F7  ,  KC.F8  ,  KC.F9  ,  KC.F10 ,  KC.F11 ,  KC.F12 ,    _______, _______,
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
          MIDI,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,    _______, _______,
             _______,      _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,              _______, _______,
             _______,      _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,    _______, _______,
             _______,      _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,      _______,         _______,
             XXXXXXX,      _______,  _______,            _______,            _______,            _______,  _______,  XXXXXXX,      _______,  _______,  _______,
    ],
]

# keyboard.debug_enabled = True

if __name__ == '__main__':
    keyboard.go()
