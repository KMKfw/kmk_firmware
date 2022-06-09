# Faux Fox Keyboard (ffkb)

![ffkb](https://fingerpunch.xyz/product/faux-fox-keyboard)

A 36 or 42 key keyboard with support for per key LEDs, 2 rotary encoders (EC11 or evqwgd001), and a feature in the center (EC11, OLED (128x64), or pimoroni trackball). KMK support is available for the BYO MCU option only.

`kb-kb2040.py` is designed to work with a KB2040.

`kb-nn.py` is designed to work with a Nice!Nano.

- [Layers](https://github.com/KMKfw/kmk_firmware/tree/master/docs/layers.md) Need more keys than switches? Use layers.
- [RGB](https://github.com/KMKfw/kmk_firmware/tree/master/docs/rgb.md) Light it up

Instructions:
* Copy the kmk directory as a whole into the root directory of your KB2040.
* Copy <gitroot>/lib/neopixel* to <usbroot>/lib/.
* Copy kb.py and main.py in this folder to <usbroot>/.

> Note: The Nice!Nano doesn't have a lot of ROM, so there are a couple of extra steps. See guidance [over here](../../docs/Officially_Supported_Microcontrollers.md#nicenano).
