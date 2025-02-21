# Spacemouse Keys

To enable spacemouse camera and/or buttons control from the keyboard, add this
module to list:

```python
from kmk.modules.spacemouse_keys import SpacemouseKeys
keyboard.modules.append(SpacemouseKeys())
```

# Keycodes

| Keycode                   | Description                          |
|---------------------------|--------------------------------------|
| `KC.SM_LB`, `KC.SM_LEFT`  | Left spacemouse button               |
| `KC.SM_RB`, `KC.SM_RIGHT` | Right spacemouse button              |
| `SM_XI`, `SM_X_INCREASE`  | Move spacemouse along its +X axis    |
| `SM_YI`, `SM_Y_INCREASE`  | Move spacemouse along its +Y axis    |
| `SM_ZI`, `SM_Z_INCREASE`  | Move spacemouse along its +Z axis    |
| `SM_AI`, `SM_A_INCREASE`  | Move spacemouse along its +A axis    |
| `SM_BI`, `SM_B_INCREASE`  | Move spacemouse along its +B axis    |
| `SM_CI`, `SM_C_INCREASE`  | Move spacemouse along its +C axis    |
| `SM_XD`, `SM_X_DECREASE`  | Move spacemouse along its -X axis    |
| `SM_YD`, `SM_Y_DECREASE`  | Move spacemouse along its -Y axis    |
| `SM_ZD`, `SM_Z_DECREASE`  | Move spacemouse along its -Z axis    |
| `SM_AD`, `SM_A_DECREASE`  | Move spacemouse along its -A axis    |
| `SM_BD`, `SM_B_DECREASE`  | Move spacemouse along its -B axis    |
| `SM_CD`, `SM_C_DECREASE`  | Move spacemouse along its -C axis    |

# Customizing Movement

To change the speed and acceleration of camera movement, use the following code:

```python
from kmk.modules.spacemouse_keys import SpacemouseKeys

spacemousekeys = SpacemouseKeys(
    max_speed = 450,
    accel = 5,
    acc_interval = 10, # Delta ms to apply acceleration
)

keyboard.modules.append(spacemousekeys)
```

**Note**:
Support for six_axis has to be explicitly
enabled in `boot.py` with the [`bootcfg` module](boot.md#six_axis).
