from kmk.keys import KC
from kmk.handlers.sequences import send_string
from kmk.modules.tapdance import TapDance

EXAMPLE_TD = KC.TD(
    # Tap once for "a"
    KC.A,
    # Tap twice for "b", or tap and hold for "left control"
    KC.HT(KC.B, KC.LCTL),
    # Tap three times to send a raw string via macro
  
)

# make the default tap time really short for this tap dance:
EXAMPLE_TD2 = KC.TD(KC.A, KC.B)