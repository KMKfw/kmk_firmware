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
| `KC.MB_BTN4`              | mouse button 4                       |
| `KC.MB_BTN5`              | mouse button 5                       |
| `KC.MW_UP`                | Mouse wheel up                       |
| `KC.MW_DOWN`, `KC.MW_DN`  | Mouse wheel down                     |
| `KC.MW_LEFT`, `KC.MW_LT`  | Mouse pan left                       |
| `KC.MW_RIGHT`, `KC.MW_RT` | Mouse pan right                      |
| `KC.MS_UP`                | Move mouse cursor up                 |
| `KC.MS_DOWN`, `KC.MS_DN`  | Move mouse cursor down               |
| `KC.MS_LEFT`, `KC.MS_LT`  | Move mouse cursor left               |
| `KC.MS_RIGHT`, `KC.MS_RT` | Move mouse cursor right              |

# Customizing Movement

To change the speed and acceleration of mouse movement use the following code:

```python
from kmk.modules.mouse_keys import MouseKeys

mousekeys = MouseKeys(
    max_speed = 10,
    acc_interval = 20, # Delta ms to apply acceleration
    move_step = 1
)

keyboard.modules.append(mousekeys)
```

**Note**:
Support for panning (mouse wheel left/right) `boot.py` has to be explicitly
enabled in `boot.py` with the [`bootcfg` module](boot.md#panning).
