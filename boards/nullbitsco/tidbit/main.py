from kb import KMKKeyboard
from kmk.keys import KC

# add active_encoders=[0, 2] to constructor if first and third encoders installed
keyboard = KMKKeyboard()

XXXXX = KC.NO

keyboard.keymap = [
    [
        XXXXX,  KC.PSLS, KC_PAST, KC_PMNS,
        KC_P7,  KC_P8,   KC_P9,   KC_PPLS,
        KC_P4,  KC_P5,   KC_P6,   KC_PPLS,
        KC_P1,  KC_P2,   KC_P3,   KC_PENT,
        KC_P0,  KC_P0,   KC_PDOT, KC_PENT,
    ]
]

if __name__ == '__main__':
    keyboard.go()
