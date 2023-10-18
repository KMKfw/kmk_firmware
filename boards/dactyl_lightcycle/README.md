# Dactyl LightCycle

![Dactyl LightCycle](https://pbs.twimg.com/media/C_lE5BUU0AEufDT?format=jpg)

A handwired, split body, concave shaped keywell, columnar keyboard -- the Dactyl LightCycle is a variation of the [Dactyl](/boards/dactyl/) keyboard.  
Differences from the Dactyl are:
1. Top (number) row removed
2. Thumb cluster is 5 keys, down from 6

[Case Files](https://github.com/adereth/dactyl-keyboard/tree/master/things): Files, in linked GitHub directory, with name beginning "LightCycle" are applicable.

KMK's rendition of the Dactyl LightCycle requires two micro controllers, rather than the Dactyl's original implementation of a micro controller and I/O expander. 

## Case Files Generator

[Dactyl Generator](https://ryanis.cool/dactyl), created by [rianadon](https://github.com/rianadon), is a web based file generator that negates composing case files using a programming language, which was a requirement when using the GitHub repository for this board, by instead compiling case files based on options and parameters configured in a web front end.

## KMK Specifics

Extensions enabled by default:
- [Layers](/docs/en/layers.md)
- [Split](/docs/en/split_keyboards.md): Configured to 1-wire UART to match legacy configuration. Please see documentation for enabling 2-wire UART or, for capable controllers, Bluetooth
- [HoldTap](/docs/en/holdtap.md)

## Microcontroller support

Replace `kb2040` in the following line, of `kb.py` file, to a supported microcontroller listed in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.kb2040 import pinout as pins
```
