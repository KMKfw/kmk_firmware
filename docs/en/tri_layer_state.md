

# TRI_LAYER_STATE

```python
from kmk.modules.trilayerstate import Layers
keyboard.modules.append(Layers())
```
****Please Note: This completely replaces below code, do not forget to remove it***
```python
from kmk.modules.layers import Layers
```
***
#Keycodes

|Key         |Description                                                                    |
|-----------------|--------------------------------------------------------------------------|
|`KC.RAISE`      |Switches the default layer until the next time the keyboard powers off |
|`KC.LOWER`      |Momentarily activates layer, switches off when you let go              |

#Behavior
Tri-state layers is a feature that allows you to access a third layer by activating two other layers.

**Base layer is layer 0
LOWER is layer 1 
RAISE is 2 
ADJUST is 3**
****The only way to change this is to go into the module and adjust accordingly ***

#Without Tri Layer State
For most usecases, the way you would create a "Tri_Layer_State would be to have KC.MO(x) KC.MO(y) and KC.MO(z) on opposing layer keys. This works out fine in a lot of use cases. The issue you run into is if you press X, Then Y, to get to Z; then you release X, and continue holding Y, it stays in Z. To release from this layer you have to release Y.

#With Tri Layer State
With Tri_Layer_state you can set opposing LOWER and RAISE keys. With the example above, when you release X it will switch back to the state of Y. Each key acting independently.
With the way this is implimented in KMK (unlike in QMK) you can still access layer 3 indipendently.



#Example code
```python
import board


from kb import KMKKeyboard

from kmk.keys import KC, make_key, maybe_make_key
from kmk.modules.modtap import ModTap
from kmk.scanners import DiodeOrientation
from kmk.modules.tapdance import TapDance
from kmk.modules.combos import Combos, Chord, Sequence
from kmk.modules.trilayerstate import Layers

keyboard = KMKKeyboard()

keyboard.modules.append(Layers())

combos = Combos()
keyboard.modules.append(combos)

modtap = ModTap()
keyboard.modules.append(modtap)

tapdance = TapDance()
keyboard.modules.append(tapdance)

NONE = KC.NO
CAE = KC.LCTL(KC.LALT(KC.END))
CAD = KC.LCTL(KC.LALT(KC.DEL))
SNIP = KC.LGUI(KC.LSFT(KC.S))

LWR = KC.LOWER
RSE = KC.RAISE



ZSFT = KC.MT(KC.Z, KC.LSFT, prefer_hold=True, tap_interrupted=False, tap_time=130)
SLSHSFT = KC.MT(KC.SLSH, KC.LSFT, prefer_hold=True, tap_interrupted=False, tap_time=130)
ALCTL = KC.MT(KC.A, KC.LCTRL, prefer_hold=False, tap_interrupted=False, tap_time=120)




keyboard.keymap = [
    [ # QWERTY
     KC.Q,  KC.W,  KC.E,     KC.R,    KC.T,     KC.Y,    KC.U,     KC.I,    KC.O,   KC.P,
     ALCTL, KC.S,  KC.D,     KC.F,    KC.G,     KC.H,    KC.J,     KC.K,    KC.L,   KC.QUOT,
     ZSFT,  KC.X,  KC.C,     KC.V,    KC.B,     KC.N,    KC.M,     KC.COMM, KC.DOT, SLSHSFT,
     NONE, NONE,   KC.LCTL,  KC.LOWER,   KC.SPACE, KC.BSPC, KC.RAISE, KC.RALT,    NONE,  NONE,

     ],
    [ # LOWER
     KC.N1,  KC.N2,  KC.N3,     KC.N4,    KC.N5,     KC.N6,    KC.N7,     KC.N8,    KC.N9,   KC.N0,
     KC.TAB,  KC.LEFT,  KC.DOWN,     KC.UP,    KC.RIGHT,     KC.TRNS,    KC.MINUS,     KC.EQUAL,    KC.LBRC,   KC.RBRC,
     KC.LCTL,  KC.GRAVE,  KC.LGUI,     KC.LALT,    KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS, 	KC.BSLS, KC.SCLN,
     KC.NO, KC.NO, KC.TRNS,     KC.LOWER,    KC.TRNS, KC.ENTER, KC.RAISE,     KC.TRNS,    KC.NO,  KC.NO,

     ],
    [ # RAISE
     KC.EXLM,  KC.AT,  KC.HASH,     KC.DLR,    KC.PERC,     KC.CIRC,    KC.AMPR,     KC.ASTR,    KC.LPRN,   KC.RPRN,
     KC.ESC,  KC.TRNS,  KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS,    KC.UNDS,     KC.PLUS,    KC.LCBR,   KC.RCBR,
     KC.CAPS,  KC.TILDE,  KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS, KC.PIPE, KC.COLN,
     KC.NO, KC.NO, KC.TRNS,     KC.LOWER,    KC.TRNS, KC.ENTER, KC.RAISE,     KC.DEL,    KC.NO,  KC.NO,

     ],
     [ # ADJUST
     KC.F1,  KC.F2,  KC.F3,     KC.F4,    KC.F5,     KC.F6,    KC.F7,     KC.F8,    KC.F9,   KC.F10,
     KC.F11,  KC.F12,  KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS,    KC.TRNS,     CAE,    CAD,   SNIP,
     KC.TRNS,  KC.TRNS,  KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS,    KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS,
     KC.NO, KC.NO, KC.TRNS,     KC.TRNS,    KC.TRNS, KC.ENTER, KC.TRNS,     KC.TRNS,    KC.NO,  KC.NO,

     ]
]
```
