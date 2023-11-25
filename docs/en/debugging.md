# Debugging
KMK's debug output is written to CircuitPython's serial console -- the one that's
used for the REPL -- and is automatically enabled if it detects a connection to
that console.
It can also be enabled manually, though that shouldn't be necessary in
general:
```python
keyboard.debug_enabled = True
```

Follow for example Adafruit's beginners guide on [how to connect to the serial console](https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console).
For Linux users, we recommend [picocom](https://github.com/npat-efault/picocom)
or [screen](https://www.gnu.org/software/screen/manual/screen.html)
