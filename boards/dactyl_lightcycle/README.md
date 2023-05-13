# Dactyl Lightcycle

![DacytlLightcycle](https://pbs.twimg.com/media/C_lE5BUU0AEufDT?format=jpg)

A handwired, split body, concave shaped key well, columnar keyboard -- the Dactyl Lightcycle is a variation of the [Dactyl](/boards/dactyl/) keyboard.  
Differences from the Dactyl are:
1. Top (number) row removed
2. Thumb cluster is 5 keys, down from 6

[Case Files](https://github.com/adereth/dactyl-keyboard/tree/master/things): Files, in linked GitHub directory, with name beginning "lightcycle" are applicable.

KMK's rendition of the Dactyl Lightcycle requires two micro controllers, rather than the Dactyl's original implementation of a micro controller and I/O expander. 

## KMK Specifics

Extentions enabled by default:
- [Layers](/docs/en/layers.md)
- [Split](/docs/en/split_keyboards.md): Configured to 1-wire UART to match legacy configuration. Please see documentation for enabling 2-wire UART or, for capable controllers, Bluetooth
- [HoldTap](/docs/en/holdtap.md)

## Microcontroller support

Replace `kb2040` in the following line, of `kb.py` file, to a supported microcontroller listed in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.kb2040 import pinout as pins
```
