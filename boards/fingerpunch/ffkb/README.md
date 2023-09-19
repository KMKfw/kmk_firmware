# Faux Fox Keyboard (ffkb)

![ffkb](https://fingerpunch.xyz/product/faux-fox-keyboard)

A 36 or 42 key keyboard with support for per key LEDs, 2 rotary encoders (EC11
or EVQWGD001), and a feature in the center (EC11, OLED (128x64), or Pimoroni
trackball). KMK support is available for the BYO MCU option only.

Use `nice_nano/kb.py` when using a Nice!Nano v2 MCU.

> Note: The Nice!Nano doesn't have a lot of ROM, so there are a couple of extra
> steps. See guidance [over
> here](../../docs/en/Officially_Supported_Microcontrollers.md#nicenano).

Use `kb2040/kb.py` when using any other pro micro footprint MCU.

An example `main.py` file is included for each MCU.

## Microcontroller support

Update this line in `kb.py` to any supported microcontroller in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
