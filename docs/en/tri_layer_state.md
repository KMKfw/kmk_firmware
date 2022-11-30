

# TRI_LAYER_STATE

```python
from kmk.modules.layers import Layers, Trilayerstate
keyboard.modules.append(Layers())
keyboard.modules.append(Trilayer())
```

#Keycodes

|Key         |Description                                                                    |
|-----------------|--------------------------------------------------------------------------|
|`KC.RAISE`      |Switches the default layer until the next time the keyboard powers off |
|`KC.LOWER`      |Momentarily activates layer, switches off when you let go              |

# Behavior

Tri-state layers is a feature that allows you to access a third layer by activating two other layers.

**Base layer is layer 0
LOWER is layer 1 
RAISE is 2 
ADJUST is 3**
****The only way to change this is to go into the module and adjust accordingly ***

# Without Tri Layer State
For most usecases, the way you would create a "Tri_Layer_State would be to have KC.MO(x) KC.MO(y) and KC.MO(z) on opposing layer keys. This works out fine in a lot of use cases. The issue you run into is if you press X, Then Y, to get to Z; then you release X, and continue holding Y, it stays in Z. To release from this layer you have to release Y.

# With Tri Layer State
With Tri_Layer_state you can set opposing LOWER and RAISE keys. With the example above, when you release X it will switch back to the state of Y. Each key acting independently.
With the way this is implimented in KMK (unlike in QMK) you can still access layer 3 indipendently.

# Limitations
There are some drawbacks at the moment, this does not support the layertap function at the moment. 

# Example code
```python
import board

from kb import KMKKeyboard

from kmk.keys import KC, make_key
from kmk.modules.trilayerstate import Layers

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
