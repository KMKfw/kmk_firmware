# Dactyl Tracer

![Top View](https://i.imgur.com/ReCBppEh.jpeg)

A split body, concave shaped keywell, columnar keyboard, with case halves designed similarly to the [Dactyl CC](/boards/dactyl/README.md#dactyl-cc--ergo-s-1).  
The "Q" key is vertically offset, from "A" key, to allow more comfortable actuation using ring finger.  
Key arrangement bears slight resemblance to the [Dactyl ManuForm](/boards/dactyl_manuform/) in that:
1. Row spacing and placement of two outward most thumb keys are identical and
2. bottom finger keywell row has two keys.

Hardware Availability: [Case files](https://github.com/mjohns/tracer)

KMK's rendition of the Dactyl Tracer requires two micro controllers, rather than the original implementation of a micro controller and I/O expander. 

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
