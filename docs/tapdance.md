# Tap Dance

Tap dance is a way to allow a single physical key to work as multiple logical
keys / actions without using layers. With basic tap dance, you can trigger these
"nested" keys or macros through a series of taps of the physical key within a
given timeout.

The resulting "logical" action works just like any other key - it can be pressed
and immediately released, or it can be held. For example, let's take a key
`KC.TD(KC.A, KC.B)`. If the tap dance key is tapped and released once quickly,
the letter "a" will be sent. If it is tapped and released twice quickly, the
letter "b" will be sent. If it is tapped once and held, the letter "a" will be
held down until the tap dance key is released. If it is tapped and released once
quickly, then tapped and held (both actions within the timeout window), the
letter "b" will be held down until the tap dance key is released.

To use this, you may want to define a `tap_time` value in your keyboard
configuration. This is an integer in milliseconds, and defaults to `300`.

You'll then want to create a sequence of keys using `KC.TD(KC.SOMETHING,
KC.SOMETHING_ELSE, MAYBE_THIS_IS_A_MACRO, WHATEVER_YO)`, and place it in your
keymap somewhere. The only limits on how many keys can go in the sequence are,
theoretically, the amount of RAM your MCU/board has, and how fast you can mash
the physical key. Here's your chance to use all that button-mash video game
experience you've built up over the years.
[//]: # (The button mashing part has been 'fixed' by a timeout refresh per)
[//]: # (button press. The comedic sentiment is worth keeping though.)

**NOTE**: Currently our basic tap dance implementation has some limitations that
are planned to be worked around "eventually", but for now are noteworthy:

- The behavior of momentary layer switching within a tap dance sequence is
  currently "undefined" at best, and will probably crash your keyboard. For now,
  we strongly recommend avoiding `KC.MO` (or any other layer switch keys that
  use momentary switch behavior - `KC.LM`, `KC.LT`, and `KC.TT`)
[//]: # (This also doesn't seem to be the case anymore; as long as the layer)
[//]: # (is transparent to the tap dance key.)
[//]: # (At least KC.MO is working as intended, other momentary actions haven't)
[//]: # (been tested.)

Here's an example of all this in action:

```python
from kmk.keycodes import KC
from kmk.handlers.sequences import send_string
from kmk.modules.tapdance import TapDance

keyboard = KMKKeyboard()

tapdance = TapDance()
tapdance.tap_time = 750
keyboard.modules.append(tapdance)

EXAMPLE_TD = KC.TD(
    KC.A,  # Tap once for "a"
    KC.B,  # Tap twice for "b"
    # Tap three times to send a raw string via macro
    send_string('macros in a tap dance? I think yes'),
    # Tap four times to toggle layer index 1
    KC.TG(1),
)

keyboard.keymap = [[ ...., EXAMPLE_TD, ....], ....]
```
