# Faux Fox Keyboard (ffkb)

![ffkb](https://github.com/sadekbaroudi/ffkb)

A 36 or 42 key keyboard with support for per key LEDs, 2 rotary encoders (EC11 or evqwgd001), and a feature in the center (EC11, OLED (128x64), or pimoroni trackball)

kb.py is designed to work with a Pro Micro or KB2040, while kb-nn.py is designed to work with a Nice!Nano.

- [Layers](https://github.com/KMKfw/kmk_firmware/tree/master/docs/layers.md) Need more keys than switches? Use layers.
- [RGB](https://github.com/KMKfw/kmk_firmware/tree/master/docs/rgb.md) Light it up

Instructions:
* Copy the kmk directory as a whole into the root directory of your KB2040
* Copy <gitroot>/lib/neopixel* to <usbroot>/lib/
* Copy kb.py and main.py in this folder to <usbroot>/

> Note: The Nice!Nano doesn't have a lot of ROM, see guidance [over here](../../docs/../../docs/Officially_Supported_Microcontrollers.md#nicenano).

