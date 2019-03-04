# ModTap
One key if you tap it, one or more modifiers if you hold it!
 
 
## Helpful examples
Just copy the example from New Keycode above your keymap and change KC.SOMETHING to the key that you want when tapped.
After that, just use the new keycode anywhere in your keymap.

|New Keycode                                                       | Description                                                     |
|------------------------------------------------------------------|-----------------------------------------------------------------|
|LCTL = KC.MT(KC.LCTRL, kc=KC.SOMETHING)                           |`LCTRL` if held `kc` if tapped                                   |
|LSFT = KC.MT(KC.LSFT, kc=KC.SOMETHING)                            |`LSHIFT` if held `kc` if tapped                                  |
|LALT = KC.MT(KC.LALT, kc=KC.SOMETHING)                            |`LALT` if held `kc` if tapped                                    |
|LGUI = KC.MT(KC.LGUI, kc=KC.SOMETHING)                            |`LGUI` if held `kc` if tapped                                    |
|RCTL = KC.MT(KC.RCTRL, kc=KC.SOMETHING)                           |`RCTRL` if held `kc` if tapped                                   |
|RSFT = KC.MT(KC.RSFT, kc=KC.SOMETHING)                            |`RSHIFT` if held `kc` if tapped                                  |
|RALT = KC.MT(KC.RALT, kc=KC.SOMETHING)                            |`RALT` if held `kc` if tapped                                    |
|RGUI = KC.MT(KC.RGUI, kc=KC.SOMETHING)                            |`RGUI` if held `kc` if tapped                                    |
|SGUI = KC.MT(KC.LSHFT, KC.LGUI, kc=KC.SOMETHING)                  |`LSHIFT` and `LGUI` if held `kc` if tapped                       |
|LCA = KC.MT(KC.LCTRL, KC.LALT, kc=KC.SOMETHING)                   |`LCTRL` and `LALT` if held `kc` if tapped                        |
|LCAG = KC.MT(KC.LCTRL, KC.LALT, KC.LGUI, kc=KC.SOMETHING)         |`LCTRL` and `LALT` and `LGUI` if held `kc` if tapped             |
|MEH = KC.MT(KC.LCTRL, KC.LSFT, KC.LALT, kc=KC.SOMETHING)          |`CTRL` and `LSHIFT` and `LALT` if held `kc` if tapped            |
|HYPR = KC.MT(KC.LCTRL, KC.LSFT, KC.LALT, KC.LGUI, kc=KC.SOMETHING)|`LCTRL` and `LSHIFT` and `LALT` and `LGUI` if held `kc` if tapped|

