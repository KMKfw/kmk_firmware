from kmk.keys import KC
from kmk.handlers.sequences import send_string
from kmk.modules.tapdance import TapDance
from kmk.handlers.sequences import simple_key_sequence

GGL = simple_key_sequence(
    (
        KC.LGUI(KC.C),
        KC.LGUI(KC.SPC),
        KC.G,
        KC.G,
        KC.L,
        KC.ENTER,
        KC.LGUI(KC.V),
        KC.ENTER
    )
)


F9 = KC.TD(
    # Tap once for "F9"
    KC.F9,
    # Tap twice for lang change
    KC.LALT(KC.Z)
)
F10 = KC.TD(
    # Tap once for "F10"
    KC.F9,
    # Tap twice for raycast, tap and hold for google search of the selected text
    KC.HT(KC.LGUI(KC.SPC), GGL),
)
