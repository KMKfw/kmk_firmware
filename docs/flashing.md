# Flashing Instructions

## DFU-UTIL

Compatible flashers:

* [dfu-programmer](http://dfu-util.sourceforge.net/)
* [python-dfu](https://github.com/vpelletier/python-dfu) (not recommended)

Flashing sequence:

1. Press the `RESET` keycode, or tap the RESET button.
2. Wait for the OS to detect the device
3. Erase the memory (may be done automatically)
4. Flash a .hex file
5. Reset the device into application mode (may be done automatically)

or:

    make <board> USER_KEYMAP=user_keymaps/<keymap>

