# Combo Layers

Combo Layers is when you hold down 2 or more KC.MO() or KC.LM() keys at a time, and it goes to a defined layer.

By default combo layers is not activated. You can activate combo layers by adding this to your `main.py` file.
The combolayers NEEDS to be above the `keyboard.modules.append(Layers(combolayers))`

```python
combo_layers = {
  (1, 2): 3,
   }
keyboard.modules.append(Layers(combo_layers))
```

In the above code, when layer 1 and 2 are held, layer 3 will activate. If you release 1 or 2 it will go to whatever key is still being held, if both are released it goes to the default (0) layer.  
You should also notice that if you already have the layers Module activated, you can just add combolayers into `(Layers())`

You can add more, and even add more than 2 layers at a time.

```python
combo_layers = {
  (1, 2): 3,
  (1, 2, 3): 4,
  }
```

## Limitations

There can only be one combo layer active at a time and for overlapping matches
the first matching combo in `combo_layers` takes precedence.
Example:
```python
layers = Layers()
layers.combo_layers = {
  (1, 2, 3): 8,
  (1, 2): 9,
  }
keyboard.modules.append(Layers(combo_layers))
```
* If you activate layers 1 then 2, your active layer will be layer number 9.
* If you activate layers 1 then 2, then 3, your active layer will be layer
  number 3 (because the layer combo `(1,2)` has been activated, but layer 3
  stacks on top).
  * deactivate 1: you're on layer 3
  * deactivate 2: you're on layer 3
  * deactivate 3: you're on layer 8
* If you activate layers 3 then 1, then 2, your active layer will be layer
  number 8. Deativate layer
  * deactivate any of 1/2/3: you're on layer 0


## Example Code

```python
import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC

combo_layers = {
  (1, 2): 3,
  }
keyboard.modules.append(Layers(combo_layers))


keyboard = KMKKeyboard()


keyboard.keymap = [
    [ #Default
    KC.A,     KC.B  KC.C  KC.D,
    KC.E,     KC.F  KC.G  KC.H,
    KC.MO(1), KC.J, KC.K, KC.MO(2),
    ],
    [ #Layer 1
    KC.N1,    KC.N2, KC.N3, KC.N4,
    KC.N5,    KC.N6, KC.N7, KC.8,
    KC.MO(1), KC.N9, KC.N0, KC.MO(2),
    ],
        [ #Layer 2
    KC.EXLM,  KC.AT,   KC.HASH, KC.DLR,
    KC.PERC,  KC.CIRC, KC.AMPR, KC.ASTR,
    KC.MO(1), KC.LPRN, KC.RPRN, KC.MO(2),
    ],
        [ #Layer 3
    KC.F1,   KC.F2, KC.F3,  KC.F4,
    KC.F5,   KC.F6, KC.F7,  KC.F8,
    KC.MO(1) KC.F9, KC.F10, KC.MO(2)
    ]
    
]

if __name__ == '__main__':
    keyboard.go()
```
