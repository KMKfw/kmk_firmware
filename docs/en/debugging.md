# Debugging

KMK's debug output is written to CircuitPython's serial console -- the one that's
used for the REPL -- and is automatically enabled if it detects a connection to
that console.
It can also be enabled manually, though that shouldn't be necessary in
general.

## KMK's Debug Utility

KMK has a convenient debug utility that adds a timestamp in milliseconds since boot and a message origin to distinguish subsystems to debug statements.

```python
from kmk.utils import Debug

# Create a debug source with the current file as message origin
debug = Debug(__name__)

# For completeness: Force enable/disable debug output. This is handled
# automatically -- you will most likely never have to use this:
# debug.enabled = True/False

# KMK idiomatic debug with guard clause
var = 'concatenate'
if debug.enabled:
    debug('Arguments ', var, '!')
```

## Connecting to the Serial Console

Follow for example Adafruit's beginners guide on [how to connect to the serial console](https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console).
For Linux users, we recommend [picocom](https://github.com/npat-efault/picocom)
or [screen](https://www.gnu.org/software/screen/manual/screen.html)
