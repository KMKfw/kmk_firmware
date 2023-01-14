## Combo Layers

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

Because of the way this feature works, you have to do the combo's in numerical order on the left side of the colon.

Example `(1, 2): 3` works. `(2, 1): 3` would not work. You can on the other hand do `(3, 4): 2` because the smaller number is to the right of the colon.  
You can't go to layer 0. so something like `(1, 2): 0` doesn't work.

### Limitations with more than 2 combo layers

Although adding more than 2 layers does work, (`(1, 2, 3): 0` for example) the functionality you get where it goes to whatever layer is still being held when another key is released, doesn't work.  
If you release the 3rd one, it will usually go to the second key press's layer if you continue to hold.  
Additionally, if you do use more than one layer combo, you should put anything that has more than 2 at the bottom.  
for example the following

```python
combo_layers = {
  (1, 2): 3,
  (1, 3): 4,
  (2, 3): 6,
  (1, 2, 3): 5,
  }
```

## Fully Working Example code

Below is an example of a fully working keypad that uses combo layers.

```python
print("Starting")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC

combo_layers = {
  (1, 2): 3,
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
