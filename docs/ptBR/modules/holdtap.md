# Keycodes HoldTap

Habilitar o HoldTap (adicionando-o à lista de módulos) te dará acesso aos
keycodes abaixo:

```python
from kmk.modules.holdtap import HoldTap
keyboard.modules.append(HoldTap())
```

## Keycodes

| Novo Keycode                                           | Descrição                                                       |
|--------------------------------------------------------|-----------------------------------------------------------------|
| LCTL = KC.HT(KC.SOMETHING, KC.LCTRL)                   | `LCTRL` se segurado `kc` se tocado                              |
| LSFT = KC.HT(KC.SOMETHING, KC.LSFT)                    | `LSHIFT` se segurado `kc` se tocado                             |
| LALT = KC.HT(KC.SOMETHING, KC.LALT)                    | `LALT` se segurado `kc` se tocado                               |
| LGUI = KC.HT(KC.SOMETHING, KC.LGUI)                    | `LGUI` se segurado `kc` se tocado                               |
| RCTL = KC.HT(KC.SOMETHING, KC.RCTRL)                   | `RCTRL` se segurado `kc` se tocado                              |
| RSFT = KC.HT(KC.SOMETHING, KC.RSFT)                    | `RSHIFT` se segurado `kc` se tocado                             |
| RALT = KC.HT(KC.SOMETHING, KC.RALT)                    | `RALT` se segurado `kc` se tocado                               |
| RGUI = KC.HT(KC.SOMETHING, KC.RGUI)                    | `RGUI` se segurado `kc` se tocado                               |
| SGUI = KC.HT(KC.SOMETHING, KC.LSHFT(KC.LGUI))          | `LSHIFT` e `LGUI` se segurado `kc` se tocado                    |
| LCA = KC.HT(KC.SOMETHING, KC.LCTRL(KC.LALT))           | `LCTRL` e `LALT` se segurado `kc` se tocado                     |
| LCAG = KC.HT(KC.SOMETHING, KC.LCTRL(KC.LALT(KC.LGUI))) | `LCTRL` e `LALT` e `LGUI` se segurado `kc` se tocado            |
| MEH = KC.HT(KC.SOMETHING, KC.LCTRL(KC.LSFT(KC.LALT)))  | `CTRL` e `LSHIFT` e `LALT` se segurado `kc` se tocado           |
| HYPR = KC.HT(KC.SOMETHING, KC.HYPR)                    | `LCTRL` e `LSHIFT` e `LALT` e `LGUI` se segurado `kc` if tapped |
