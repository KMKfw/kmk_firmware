# Mouse keys

To enable mouse cursor and/or mouse buttons control from the keyboard add this
module to list:

```python
from kmk.modules.mouse_keys import MouseKeys
keyboard.modules.append(MouseKeys())
```

# Keycodes

| Keycode                   | Description                          |
|---------------------------|--------------------------------------|
| `KC.MB_LMB`               | Left mouse button                    |
| `KC.MB_RMB`               | Right mouse button                   |
| `KC.MB_MMB`               | Middle mouse button                  |
| `KC.MW_UP`                | Mouse wheel up                       |
| `KC.MW_DOWN`, `KC.MW_DN`  | Mouse wheel down                     |
| `KC.MS_UP`                | Move mouse cursor up                 |
| `KC.MS_DOWN`, `KC.MS_DN`  | Move mouse cursor down               |
| `KC.MS_LEFT`, `KC.MS_LT`  | Move mouse cursor left               |
| `KC.MS_RIGHT`, `KC.MS_RT` | Move mouse cursor right              |
