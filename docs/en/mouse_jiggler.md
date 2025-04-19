# Mouse Jiggler

This module will periodically jiggle the mouse cursor, keeping the host
system from idling or sleeping.

To enable the mouse jiggler module, import it and append it to the
modules list:

```python
from kmk.modules.mouse_jiggler import MouseJiggler
keyboard.modules.append(MouseJiggler())
```

# Keycodes

| Keycode                   | Description                          |
|---------------------------|--------------------------------------|
| `KC.MJ_TOGGLE`            | Toggle the mouse jigger.             |
| `KC.MJ_START`             | Stop jiggling.                       |
| `KC.MJ_STOP`              | Start jiggling.                      |

# Customizing Behavior

To change the speed and acceleration of mouse movement, use the following code:

```python
from kmk.modules.mouse_jiggler import MouseJiggler

jiggler = MouseJiggler(
    period_ms = 5000, # Move the mouse cursor every 5 seconds.
    move_step = 1, # Move one unit each time period_ms elapses.
)

keyboard.modules.append(jiggler)
```

# LED Status

It can be helpful to show whether the mouse jiggler is active via a status LED,
RGB, or other means. The mouse jiggler module provides an `is_jiggling`
property which returns `True` when the jiggler is active.

# Requirements

Support for the mouse HID endpoint must be enabled in `boot.py` for the mouse
jiggler to function. This can be done using the
[`bootcfg` module](boot.md#mouse) and setting `mouse = True`.

Alternatively, if a custom `boot.py` is in place, then `usb_hid.Device.MOUSE`
can be added to the list of HID endpoints passed to `usb_hid.enable()`.
```python
usb_hid.enable((usb_hid.Device.KEYBOARD, usb_hid.Device.MOUSE))