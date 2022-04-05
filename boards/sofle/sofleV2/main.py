import board

from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitType

keyboard = KMKKeyboard()

layers_ext = Layers()

split = Split(
    split_flip=True,  # If both halves are the same, but flipped, set this True
    split_type=SplitType.UART,  # Defaults to UART
    uart_interval=20,  # Sets the uarts delay. Lower numbers draw more power
    data_pin=board.RX,  # The primary data pin to talk to the secondary device with
    data_pin2=board.TX,  # Second uart pin to allow 2 way communication
    use_pio=True, # allows for UART to be used with PIO
)

keyboard.modules = [layers_ext, split]

# Cleaner key names
XXXXXXX = KC.NO
LOWER = KC.MO(1)
RAISE = KC.MO(2)

keyboard.keymap = [
    [  #QWERTY
        #HERE-----#HERE-----#HERE-----#HERE-----#HERE-----#HERE-----#HERE-----#ENCODER--#ENCODER--#HERE-----#HERE-----#HERE-----#HERE-----#HERE-----#HERE-----#HERE-----
        KC.ESC,   KC.N1,    KC.N2,    KC.N3,    KC.N4,    KC.N5,                                            KC.N6,    KC.N7,    KC.N8,    KC.N9,    KC.N0,    KC.BSPC,
        KC.TAB,   KC.Q,     KC.W,     KC.E,     KC.R,     KC.T,                                             KC.Y,     KC.U,     KC.I,     KC.O,     KC.P,     KC.BSLS,
        KC.LCTL,  KC.A,     KC.S,     KC.D,     KC.F,     KC.G,                                             KC.H,     KC.J,     KC.K,     KC.L,     KC.SCLN,  KC.QUOT,
        KC.LSFT,  KC.Z,     KC.X,     KC.C,     KC.V,     KC.B,                                             KC.N,     KC.M,     KC.COMM,  KC.DOT,   KC.SLSH,  KC.RSFT,
                            KC.LGUI,  KC.LALT,  KC.LCTL,  LOWER,    KC.ENT,   KC.MUTE,  KC.MPLY,  KC.SPC,   RAISE,    KC.RCTL,  KC.RALT,  KC.RCMD,
    ],
    [  #LOWER
        #HERE-----#HERE-----#HERE-----#HERE-----#HERE-----#HERE-----#HERE-----#ENCODER--#ENCODER--#HERE-----#HERE-----#HERE-----#HERE-----#HERE-----#HERE-----#HERE-----
        KC.ESC,   KC.F1,    KC.F2,    KC.F3,    KC.F4,    KC.F5,                                            KC.F6,    KC.F7,    KC.F8,    KC.F9,    KC.F10,   KC.F11,
        XXXXXXX,  KC.N1,    KC.N2,    KC.N3,    KC.N4,    KC.N5,                                            KC.N6,    KC.N7,    KC.N8,    KC.N9,    KC.N0,    KC.F12,
        KC.LCTL,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,                                          KC.LEFT,  KC.DOWN,  KC.UP,    KC.RIGHT, XXXXXXX,  XXXXXXX,
        KC.LSFT,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,                                          XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,
                            KC.LGUI,  KC.LALT,  KC.LCTL,  LOWER,    KC.ENT,   XXXXXXX,  XXXXXXX,  KC.SPC,   RAISE,    KC.RCTL,  KC.RALT,  KC.RCMD,
    ],
    [  #RAISE
        #HERE-----#HERE-----#HERE-----#HERE-----#HERE-----#HERE-----#HERE-----#ENCODER--#ENCODER--#HERE-----#HERE-----#HERE-----#HERE-----#HERE-----#HERE-----#HERE-----
        KC.ESC,   KC.EXLM,  KC.AT,    KC.HASH,  KC.DLR,   KC.PERC,                                          XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  KC.BSPC,
        XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,                                          KC.CIRC,  KC.AMPR,  KC.ASTR,  KC.LPRN,  KC.RPRN,  KC.BSLS,
        XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,                                          KC.MINS,  KC.EQL,   KC.LBRC,  KC.RBRC,  KC.PIPE,  XXXXXXX,
        XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,                                          KC.UNDS,  KC.PLUS,  XXXXXXX,  XXXXXXX,  XXXXXXX,  XXXXXXX,
                            KC.LGUI,  KC.LALT,  KC.LCTL,  LOWER,    KC.ENT,   KC.MUTE,  XXXXXXX,  KC.SPC,   RAISE,    KC.RCTL,  KC.RALT,  KC.RCMD,
    ]
]

encoder_handler = EncoderHandler()
encoder_handler.pins = ((keyboard.encoder_pin_1, keyboard.encoder_pin_0, None, False),)
encoder_handler.map = (
    ((KC.VOLD, KC.VOLU),), # base layer
    ((KC.VOLD, KC.VOLU),), # Raise
    ((KC.VOLD, KC.VOLU),), # Lower
)

keyboard.modules.append(encoder_handler)

if __name__ == "__main__":
    keyboard.go()
