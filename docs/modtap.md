# ModTap Keycodes
Enabling ModTap will give you access to the following keycodes and can simply be
added to the extentions list.

```python
from kmk.extensions.modtap import ModTap
keyboard.extensions.append(ModTap())
```

## Keycodes

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


