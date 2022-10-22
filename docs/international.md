# Non QWERTY layout
If your computer is not configured (at the OS level) to use the QWERTY layout, you will have a hard time making your layers as `KC.Q` will for example output an `a` on an azerty layout.

To not have to deal yourself with all those translation we provide the `KeyMapConverter` class. It is intented to be subclassed for your layout, you then only have to define your mapping.

Note: There is no consensus on this (and currently not many user of that feature). Keep in mind that this might evolve, so keep an eyes on this when you update KMK.

The mapping is a relation:
 - from what you want to use in the keymap (= what you see on your keyboard key)
 - to what it should send as qwerty (= what your computer will print for this key if you set it up to use a QWERTY layout)


## Example use
For a french AZERTY layout you would have something like:

file: /kmk/extensions/keymap_extras/keymap_french.py
```python
from kmk.keys import KC
from kmk.extensions.keymap_extras.base import KeyMapConverter

class AZERTY(KeyMapConverter):
    MAPPING = {
		'A': KC.Q,
		'Z': KC.W,
		'E': KC.E,
		'R': KC.R,
		'T': KC.T,
		'Y': KC.Y,
		...
    }
```

file: /code.py
```python
from kmk.extensions.keymap_extras.keymap_french import AZERTY

FR = AZERTY()
keyboard.keymap = [[FR.A, FR.Z, FR.E, FR.R, FR.T, FR.Y, ...]]
```

## Generating a missing layout
Making such mapping is very tedious. But a script to generate it from the equivlaent files from QMK can be found [here](https://github.com/crazyiop/kmk_keymap_extras)

Warning: The generated layout **need to be tested** and might need to be refined but that should save you quite some work.
