# CapsWord
The CapsWord module functions similar to caps lock but will deactivate automatically when its encounters a key that breaks the word or after inactivity timeout.
By default it will not deactivate CapsWord on numbers, alphabets, underscore, modifiers, minus, backspace and other keys like HoldTap, Layers, etc.
Add it to your keyboard's modules list with:

```python
from kmk.modules.capsword import CapsWord
# default inactivity timeout is 8s
caps_word=CapsWord()
# change inactivity timeout
# caps_word=CapsWord(timeout=5000) 
# for no inactivity timeout
# caps_word=CapsWord(timeout=0) 
# add additional ignored keys
# caps_word.keys_ignored.append(KC.COMMA) 
keyboard.modules.append(caps_word)
keyboard.keymap = [
    [
        KC.CW,
    ],
]
```
## Keycodes

|Key                    |Aliases             |Description                                    |
|-----------------------|--------------------|-----------------------------------------------|
|`KC.CW`                |`KC.CAPSWORD`       |Enables/disables CapsWord                      |