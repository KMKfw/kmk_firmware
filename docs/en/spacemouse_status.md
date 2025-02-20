# Spacemouse Status
This extension exposes host-side LED status of the spacemouse.

## Enabling the extension
```python
from kmk.extensions.spacemouse_status import SpacemouseStatus

sm_led = SpacemouseStatus()
keyboard.extensions.append(sm_led)

```

## Read LED Status
Similar to the LockStatus extension, the spacemouse LED state can 
be retrieved with `sm_led.get_led()` and return `True`
when the LED is enabled and `False` otherwise.
