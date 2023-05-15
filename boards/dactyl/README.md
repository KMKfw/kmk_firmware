# Dactyl

![Dacytl1](https://raw.githubusercontent.com/adereth/dactyl-cave/master/resources/glamourshot.png)
![Dactyl2](https://i.imgur.com/Bo11dGx.jpeg)

A split body, concave shaped key well, columnar keyboard with a 6 key thumb cluster that takes inspiration from the Kinesis Advantage keyboard range.

Hardware Availability: [Case Files](https://github.com/adereth/dactyl-keyboard)

KMK's rendition of the Dactyl requires two micro controllers rather than the original implementation of a micro controller and I/O expander. 

## KMK Specifics

Extentions enabled by default  
- [Layers](/docs/en/layers.md)
- [Split](/docs/en/split_keyboards.md): Configured to 1-wire UART to match legacy configuration. Please see documentation for enabling 2-wire UART or, for capable controllers, Bluetooth

## Microcontroller support

Replace `kb2040` in the following line of `kb.py` to a supported microcontroller listed in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.kb2040 import pinout as pins
```

## Dactyl CC & Ergo S-1

Electronically:
1. [Dactyl CC](https://github.com/mjohns/dactyl-cc) and [Ergo S-1](https://github.com/wizarddata/Ergo-S-1) are identical to one another
2. Both these boards are identical to the Dactyl with one difference; on the finger key-well, they do not have the bottom row, outer column key (per half) of the Dactyl

To accomodate this, in files:
- **`kb.py`**  
`coord_mapping` element: Delete '`24, `' and '`60,`'
- **`main.py`**  
`keyboard.keymap` element: Delete bottom row, outer column position from each side including accompanying comma
