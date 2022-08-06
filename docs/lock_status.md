# Lock Status
This extension exposes host-side locks like caps or num lock.

## Enabling the extension
```python
from kmk.extensions.lock_status import LockStatus

locks = LockStatus()
keyboard.extensions.append(locks)

```

## Read Lock Status
Lock states can be retrieved with getter methods and are truth valued -- `True`
when the lock is enabled and `False` otherwise.

|Method                    |Description |
|--------------------------|------------|
|`locks.get_num_lock() `   |Num Lock    |
|`locks.get_caps_lock() `  |Caps Lock   |
|`locks.get_scroll_lock() `|Scroll Lock |
|`locks.get_compose() `    |Compose     |
|`locks.get_kana() `       |Kana        |


## React to Lock Status Changes
Lock Status will accept a callback function that is invoked when the status of
a lock changes. When the function is invoked, it will have a Lock Status object
passed to it.

```python
import board

from kb import KMKKeyboard
from kmk.extensions.lock_status import LockStatus
from kmk.extensions.LED import LED

keyboard = KMKKeyboard()
keyboard.extensions.append(LED(led_pin=[board.GP27, board.GP28]))

def toggle_lock_leds(self):
    if self.get_caps_lock():
        keyboard.leds.set_brightness(50, leds=[0])
    else:
        keyboard.leds.set_brightness(0, leds=[0])

    if self.get_scroll_lock():
        keyboard.leds.set_brightness(50, leds=[1])
    else:
        keyboard.leds.set_brightness(0, leds=[1])

keyboard.extensions.append(LockStatus(toggle_lock_leds))
```