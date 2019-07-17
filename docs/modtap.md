# ModTap
One key if you tap it, one or more modifier keys if you hold it!
 
 
## Helpful examples
Just copy the example from New Keycode above your keymap and change KC.SOMETHING to the key that you want when tapped.
After that, just use the new keycode anywhere in your keymap.

|New Keycode                                            | Description                                                     |
|-------------------------------------------------------|-----------------------------------------------------------------|
|LCTL = KC.MT(KC.SOMETHING, KC.LCTRL)                   |`LCTRL` if held `kc` if tapped                                   |
|LSFT = KC.MT(KC.SOMETHING, KC.LSFT)                    |`LSHIFT` if held `kc` if tapped                                  |
|LALT = KC.MT(KC.SOMETHING, KC.LALT)                    |`LALT` if held `kc` if tapped                                    |
|LGUI = KC.MT(KC.SOMETHING, KC.LGUI)                    |`LGUI` if held `kc` if tapped                                    |
|RCTL = KC.MT(KC.SOMETHING, KC.RCTRL)                   |`RCTRL` if held `kc` if tapped                                   |
|RSFT = KC.MT(KC.SOMETHING, KC.RSFT)                    |`RSHIFT` if held `kc` if tapped                                  |
|RALT = KC.MT(KC.SOMETHING, KC.RALT)                    |`RALT` if held `kc` if tapped                                    |
|RGUI = KC.MT(KC.SOMETHING, KC.RGUI)                    |`RGUI` if held `kc` if tapped                                    |
|SGUI = KC.MT(KC.SOMETHING, KC.LSHFT(KC.LGUI))          |`LSHIFT` and `LGUI` if held `kc` if tapped                       |
|LCA = KC.MT(KC.SOMETHING, KC.LCTRL(KC.LALT))           |`LCTRL` and `LALT` if held `kc` if tapped                        |
|LCAG = KC.MT(KC.SOMETHING, KC.LCTRL(KC.LALT(KC.LGUI))) |`LCTRL` and `LALT` and `LGUI` if held `kc` if tapped             |
|MEH = KC.MT(KC.SOMETHING, KC.LCTRL(KC.LSFT(KC.LALT)))  |`CTRL` and `LSHIFT` and `LALT` if held `kc` if tapped            |
|HYPR = KC.MT(KC.SOMETHING, KC.HYPR)                    |`LCTRL` and `LSHIFT` and `LALT` and `LGUI` if held `kc` if tapped|

```python
SHFT_HOME = KC.MT(KC.HOME, KC.LSFT)

keyboard.keymap = [[ ...., SHFT_HOME, ....], ....]
```

