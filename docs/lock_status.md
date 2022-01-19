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
|`locks.get_caps_lock() `  |Num Lock    |
|`locks.get_caps_lock() `  |Caps Lock   |
|`locks.get_scroll_lock() `|Scroll Lock |
|`locks.get_compose() `    |Compose     |
|`locks.get_kana() `       |Kana        |
