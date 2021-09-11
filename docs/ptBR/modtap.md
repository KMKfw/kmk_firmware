# Keycodes ModTap

Habilitar o ModTap (adicionando-o à lista de módulos) te dará acesso aos
keycodes abaixo:

```python
from kmk.modules.modtap import ModTap
keyboard.modules.append(ModTap())
```

## Keycodes

| Novo Keycode                                           | Descrição                                                       |
|--------------------------------------------------------|-----------------------------------------------------------------|
| LCTL = KC.MT(KC.SOMETHING, KC.LCTRL)                   | `LCTRL` se segurado `kc` se tocado                              |
| LSFT = KC.MT(KC.SOMETHING, KC.LSFT)                    | `LSHIFT` se segurado `kc` se tocado                             |
| LALT = KC.MT(KC.SOMETHING, KC.LALT)                    | `LALT` se segurado `kc` se tocado                               |
| LGUI = KC.MT(KC.SOMETHING, KC.LGUI)                    | `LGUI` se segurado `kc` se tocado                               |
| RCTL = KC.MT(KC.SOMETHING, KC.RCTRL)                   | `RCTRL` se segurado `kc` se tocado                              |
| RSFT = KC.MT(KC.SOMETHING, KC.RSFT)                    | `RSHIFT` se segurado `kc` se tocado                             |
| RALT = KC.MT(KC.SOMETHING, KC.RALT)                    | `RALT` se segurado `kc` se tocado                               |
| RGUI = KC.MT(KC.SOMETHING, KC.RGUI)                    | `RGUI` se segurado `kc` se tocado                               |
| SGUI = KC.MT(KC.SOMETHING, KC.LSHFT(KC.LGUI))          | `LSHIFT` e `LGUI` se segurado `kc` se tocado                    |
| LCA = KC.MT(KC.SOMETHING, KC.LCTRL(KC.LALT))           | `LCTRL` e `LALT` se segurado `kc` se tocado                     |
| LCAG = KC.MT(KC.SOMETHING, KC.LCTRL(KC.LALT(KC.LGUI))) | `LCTRL` e `LALT` e `LGUI` se segurado `kc` se tocado            |
| MEH = KC.MT(KC.SOMETHING, KC.LCTRL(KC.LSFT(KC.LALT)))  | `CTRL` e `LSHIFT` e `LALT` se segurado `kc` se tocado           |
| HYPR = KC.MT(KC.SOMETHING, KC.HYPR)                    | `LCTRL` e `LSHIFT` e `LALT` e `LGUI` se segurado `kc` if tapped |
