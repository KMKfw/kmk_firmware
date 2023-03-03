# Kyria Keyboard

A split keyboard with a 3x6 columnar stagger and 7 thumb keys. One button on each side is usually replaced by an
encoder.

Official retailer of Kyria PCB: [splitkb.com](https://splitkb.com/collections/keyboard-kits/products/kyria-pcb-kit). PCB
was designed with QMK in mind and KMK implementation is not officially supported by PCB designer and seller.

Keyboard works with controllers having Pro Micro layout. Existing configurations:

| PCB version | Board                               | Config file               |
|:-----------:|-------------------------------------|---------------------------|
|     1.*     | Any quickpin pro micro based board. | kb_v1_                    |
|     2.*     | Any quickpin pro micro based board. | _waiting for pinout docs_ |

## Compatibility issues

- **TRRS connection** - KMK has no protocol for one-pin communication between two splits. So, if you are using TRRS wire
  connection, only right side send matrix events to the left side. No issue when using BLE.
- **Right side encoder** - right encoder currently doesn't send updates to left half and can even freeze right half
- **OLED screens** - OLED screens are not required, but often element of Kyria keyboards. KMK have no official OLED
  implementation, but as it's based on Circuit Python, adding one is very simple and there are many examples, also on
  KMK forks

## `main.py` example config

Current layout is based on default [QMK Kyria layout](https://config.qmk.fm/#/splitkb/kyria/rev1/LAYOUT)

It has the following modules/extensions enabled:

- [Split](/docs/en/split_keyboards.md) Connects halves using a wire
- [Layers](/docs/en/layers.md) Do you need more keys than switches? Use
  layers.
- [HoldTap](/docs/en/holdtap.md) Enable press/hold double binding of keys
- [MediaKeys](/docs/en/media_keys.md) Common media controls

Also uncomment right section to enable samples of following:

- [RGB](/docs/en/rgb.md) Turn on the backlight (**requires neopixel.py
  library to work**)
- [Encoder](docs/encoder.md) Make the knobs do something

## More steps required during install

In order to mitigate lack of one-wire protocol, KMK use its UART implementation but with special low-level PIO
subprogram available only on RP2040. It allows using other pins for UART than on-board RX and TX.

Because of the above, besides of normal installation steps, you have to also:

- install Circuit Python in 7.2+ version
- add `adafruit_pioasm.mpy` library to lib or root folder of a board

## Microcontroller support

Update this line in `kb.py` to any supported microcontroller in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
