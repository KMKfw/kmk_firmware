# Debugging
Debug will output most of the useful state to the console. This can be enable in your firmware
by setting this in your keymap. NOTE that it will be slower, so only enable this when you
need debugging.
```python
DEBUG_ENABLE = True
```

The output can be viewed by connecting to the serial port of the keybord. Please refer to [THIS](https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console) for
more information when connecting to serial console. For Linux users, we recommend [picocom](https://github.com/npat-efault/picocom) or
[screen](https://www.gnu.org/software/screen/manual/screen.html)
