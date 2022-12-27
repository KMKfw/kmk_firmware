

# TRI_LAYER_STATE

```python
from kmk.modules.layers import Layers, Trilayer
keyboard.modules.append(Layers())
keyboard.modules.append(Trilayer())
```

#Keycodes

|Key         |Description                                                                    |
|-----------------|--------------------------------------------------------------------------|
|`KC.RAISE`      |Switches to the default or defined Raise Layer. |
|`KC.LOWER`      |Switches to the default or defined Lower Layer. |

# Behavior

Tri-state layers is a feature that allows you to access a third layer by activating two other layers.

# Changing Layers
By default, the default layer is 0, lower is 1, raise is 2, adjust is 3.
To change which layers are affected by the "lower raise adjust" add this just above your keymap. 
```python
Trilayer.place = [
    0, #default 'or the layer it goes to when you release all keys. for most it is 0'
    1, #lower 'or the 'KC.LOWER' key'
    2, #raise 'or the 'KC.LOWER' key'
    3, #adjust 'or the layer that is activated when lower or raise are pressed simultaneously'
    ]
```

# Without Tri Layer State
For most usecases, the way you would create a "Tri_Layer_State would be to have KC.MO(x) KC.MO(y) and KC.MO(z) on opposing layer keys. This works out fine for most people. The issue you run into is if you press KC.MO(X), Then KC.MO(Y), to get to KC.MO(Z); then you release KC.MO(X), and continue holding KC.MO(Y), it stays in KC.MO(Z). To get back into KC.MO(Y) you need to release KC.MO(Y) and press it again.

# With Tri Layer State
With Tri_Layer_state you can set opposing LOWER and RAISE keys. With the example above where you are not using tri layer state, when you release KC.MO(X) it will switch back to the state of KC.MO(Y). Each key acting independently.
With the way this is implimented in KMK (unlike in QMK) you can still access layer 3 independently.

Here is a Real world usecase: 
You type a symbol on the raise layer, you have set enter to be on the lower layer. You quickly want to let go of raise and go to lower to press enter. You can do this as quickly as your finger releases raise with tri layer state. Without it, you could potentially hit lower before you let go of raise, causing you to be stuck on the adjust layer instead of lower.


# Example code
```python
import board

from kb import KMKKeyboard

from kmk.keys import KC, make_key
from kmk.modules.layers import Layers, Trilayer

keyboard = KMKKeyboard()

keyboard.modules.append(Layers())
keyboard.modules.append(Trilayer())

keyboard.keymap = [
    [ # QWERTY
KC.A,     KC.B,     KC.C,
KC.LOWER, KC.SPACE, KC.RAISE,

     ],
    [ # LOWER
KC.N1,    KC.N2,    KC.N3,
KC.LOWER, KC.SPACE, KC.RAISE,

     ],
    [ # RAISE
KC.EXLM,  KC.AT,    KC.HASH,
KC.LOWER, KC.SPACE, KC.RAISE,

     ],
     [ # ADJUST
KC.F1,    KC.F2,    KC.F3,
KC.LOWER, KC.SPACE, KC.RAISE

     ]
]
```
