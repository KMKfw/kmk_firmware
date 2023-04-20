# Dactyl

![Dacytl](https://raw.githubusercontent.com/adereth/dactyl-cave/master/resources/glamourshot.png)
![Dactyl](https://i.imgur.com/Bo11dGx.jpeg)

A split body, concave shaped key well, columnar keyboard with a 6 key thumb cluster that takes inspiration from the Kinesis Advantage keyboard range.

KMK's rendition of the [aderth/dactyl-keyboard](https://github.com/adereth/dactyl-keyboard) requires two micro controllers rather than the original implementation of a micro controller and I/O expander. 

## KMK Specifics

Extentions enabled by default  
- [Layers](/docs/en/layers.md)
- [Split](/docs/en/split_keyboards.md): Configured to 1-wire UART to match legacy configuration. Please see documentation for enabling 2-wire UART or, for capable controllers, Bluetooth

## Microcontroller support

Replace `kb2040` in the following line of `kb.py` to a supported microcontroller listed in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.kb2040 import pinout as pins
```
