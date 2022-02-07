# Encoder module
Add twist control to your keyboard! Volume, zoom, anything you want

This module was mostly built to support basoc functionality of the Adafruit I2C QT Rotary Encoder with NeoPixel

## Enabling the extension
The constructor(`i2cEncoderHandler` class) takes a list of encoders, each one defined as a `busio.I2C`, address and optionally a flag set to True if you want it to be reversed.
The encoder_map is modeled after the keymap and works the same way. It should have as many layers (key pressed on "turned left", key pressed on "turned right", key pressed on "knob pressed") as your keymap, and use KC.NO keys for layers that you don't require any action.
The encoder supports a velocity mode if you desire to make something for video or sound editing. **only dented encoder tested**

## How to use
How to use this module in your main / code file

you would need to install `adafruit_seesaw` package

1. load the module
```python
from kmk.modules.i2c_encoder import i2cEncoderHandler
encoder_handler = i2cEncoderHandler()
keyboard.modules = [layers, modtap, encoder_handler]
```

2. Define the pins for each encoder (pin_a, pin_b, pin_button, True for an inversed encoder)
```python
encoder_handler.pins = ((board.GP17, board.GP15, board.GP14, False), (encoder 2 definition), etc. )
```

3. Define the mapping of keys to be called (1 / layer)
```python
# You can optionally predefine combo keys as for your layout
Zoom_in = KC.LCTRL(KC.EQUAL)
Zoom_out = KC.LCTRL(KC.MINUS)


encoder_handler.map = [(( KC.VOLD, KC.VOLU, KC.MUTE),(encoder 2 definition), etc. ), # Layer 1
                      ((KC.Zoom_out, KC.Zoom_in, KC.NO),(encoder 2 definition), etc. ), # Layer 2
                      ((KC.A, KC.Z, KC.N1),(encoder 2 definition), etc. ), # Layer 3
                      ((KC.NO, KC.NO, KC.NO),(encoder 2 definition), etc. ), # Layer 4
                      ]
```



4. Encoder methods on_move_do and on_button_do can be overwritten for complex use cases

## Full example (with 1 encoder)

```python
from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.i2c_encoder import i2cEncoderHandler
from kmk.extensions.media_keys import MediaKeys

import board
import busio


# Addons -------------------------------------------

# Setup i2c
SDA = board.GP0
SCL = board.GP1
i2c = busio.I2C(SCL, SDA)

#if i2c.try_lock():
#    print("i2c.scan(): " + str(i2c.scan()))
#i2c.unlock()

# Keyboard

# Setup Keyboard
keyboard = KMKKeyboard()
layers = Layers()
encoder_handler = i2cEncoderHandler()
keyboard.modules = [
    layers,
    encoder_handler
]
keyboard.extensions = [
    MediaKeys()
]

# keyboard.unicode_mode = UnicodeMode.LINUX
keyboard.tap_time = 250
keyboard.debug_enabled = False

# Encoder
# Setup Encoder @ address 0x36
encoder_handler.i2c = ((i2c, 0x36, False),)

# Rotary Encoder (1 encoder / 1 definition per layer)
encoder_handler.map = [
    ((KC.VOLD, KC.VOLU, KC.MPLY),), # Default
    ((KC.PGDN, KC.PGDN, KC.END),), # Function
]

# Trackball
# Setup trackball @ address 0xA


# Keymap
_______ = KC.TRNS
XXXXXXX = KC.NO

keyboard.keymap = [
[  # Default
        KC.ESC,    KC.N1,     KC.N2,     KC.N3,     KC.N4,     KC.N5,     KC.N6,     KC.N7,     KC.N8,     KC.N9,     KC.N0,     KC.MINS,   KC.EQL,    KC.BSPC,   XXXXXXX,
        KC.TAB,    KC.Q,      KC.W,      KC.E,      KC.R,      KC.T,      KC.Y,      KC.U,      KC.I,      KC.O,      KC.P,      KC.LBRC,   KC.RBRC,   XXXXXXX,  KC.PGUP,
        KC.CAPS,   KC.A,      KC.S,      KC.D,      KC.F,      KC.G,      KC.H,      KC.J,      KC.K,      KC.L,      KC.SCLN,   KC.QUOT,   KC.NUHS,   KC.ENTER,   KC.PGDN,
        KC.LSFT,   KC.NUBS,   KC.Z,      KC.X,      KC.C,      KC.V,      KC.B,      KC.N,      KC.M,      KC.COMM,   KC.DOT,    KC.SLSH,   KC.RSFT,   XXXXXXX,   KC.DEL,
        KC.LCTL,   KC.LGUI,   KC.LALT,   XXXXXXX,   KC.MO(1),  XXXXXXX,   KC.SPC,    XXXXXXX,   KC.MO(1),  KC.RALT,   KC.RCTL,   KC.LEFT,   KC.DOWN,   KC.UP,     KC.RIGHT,
    ],
    [  # Function
        KC.GRV,    KC.F1,     KC.F2,     KC.F3,     KC.F4,     KC.F5,     KC.F6,     KC.F7,     KC.F8,     KC.F9,     KC.F10,    KC.F11,    KC.F12,    _______,   _______,
        _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   KC.PSCR,
        _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   KC.PAUSE,
        _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   _______,   KC.INSERT,
        _______,   _______,   _______,   XXXXXXX,   _______,   XXXXXXX,   _______,   XXXXXXX,   _______,   _______,   _______,   KC.HOME,   KC.PGDN,   KC.PGUP,   KC.END,
    ]
]

# ------------------------------------------------------------- Main logic -------------------------------------------

if __name__ == "__main__":
    keyboard.go()
