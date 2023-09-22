# Serial ACE (Arbitrary Code Execution over serial interface)

**Caution: This module allows unrestricted, arbitrary code execution on your KMK
device. That includes potential exploits, such as keyloggers, and unvetted
user code that may result in undesired behavior and/or crashes.
This feature is purely experimental in the sense that you probably neither
want nor should use it in production.
Advanced knowledge of python and the serial console is required, and we will
not provide help or support in any way.**

This module provides an API to run any valid python code on your keyboard and
return the result of that code via an additional serial console (not the one you
use for the CircuitPython debugger).


## Prerequisite

Enable the data serial in `boot.py`, for example by using KMK's builtin boot
configurator:
```python
from kmk.bootcfg import bootcfg

bootcfg(
    # ...excerpt
    cdc_data=True,
    # ...
)

```
Consult the [bootcfg documentation](boot.md) for more details.


## Example

Enable the module, just as any other module else:
```
from kmk.modules.serialace import SerialACE
keyboard.modules.append(SerialACE())
```

Assume the data serial is on `/dev/ttyACM1`.
Depending on your OS settings, it may be necessary to explicitly set the serial
device to raw transmission, no echo:
```bash
stty -F /dev/ttyACM1 raw -echo
```

### Get the List of Active Layers
```bash
$ echo "keyboard.active_layers" > /dev/ttyACM1
$ cat /dev/ttyACM1
[0]
```

### "Tap" a Key
```bash
$ echo "exec('from kmk.keys import KC; keyboard.tap_key(KC.Y)')" > /dev/ttyACM1
$ y
```
