from kb import KMKKeyboard

from kmk.keys import KC

# add active_encoders=[0, 2] to constructor if first and third encoders installed
keyboard = KMKKeyboard()

XXXXX = KC.NO

# fmt:off
keyboard.keymap = [
    [
        XXXXX,  KC.PSLS, KC.PAST, KC.PMNS,
        KC.P7,  KC.P8,   KC.P9,   KC.PPLS,
        KC.P4,  KC.P5,   KC.P6,   KC.PPLS,
        KC.P1,  KC.P2,   KC.P3,   KC.PENT,
        KC.P0,  KC.P0,   KC.PDOT, KC.PENT,
    ]
]
# fmt:on

if __name__ == '__main__':
    keyboard.go()
