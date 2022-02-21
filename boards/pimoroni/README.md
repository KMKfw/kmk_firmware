# Pimoroni Keybow family

A family of macro pads based on raspberry pi hardware:
![Keybow](image url for keybow)
(Original) Keybow - Raspberry Pi hat. 4x3 hotswap keys, with an APA102 LED per key.

![Keybow 2040](image url for keybow 2040)
Keybow 2040 - custom RP2040 board. 4x4 hotswap keys, with an RGB LED per key driven by a shared IS31FL3731 controller.

These boards share the 'feature' of using a single GPIO per key rather than a row and column matrix, so these both
use CircuitPython's `keypad.Keys` module instead of the regular KMK matrix scanner.


## Retailers
### UK
- Pimoroni
  - [Keybow](https://shop.pimoroni.com/products/keybow)
  - [Keybow 2040](https://shop.pimoroni.com/products/keybow-2040)

### AU
- Core Electronics
  - [Keybow](https://core-electronics.com.au/pimoroni-keybow-mini-mechanical-keyboard-kit-clicky-keys.html)
  - [Keybow 2040](https://core-electronics.com.au/pimoroni-keybow-2040-tactile-keys.html)

Extensions enabled by default  
- [Layers](https://github.com/KMKfw/kmk_firmware/tree/master/docs/layers.md) Need more keys than switches? Use layers.
- [RGB](https://github.com/KMKfw/kmk_firmware/tree/master/docs/rgb.md) Light it up (Keybow only so far)
- [MediaKeys](https://github.com/KMKfw/kmk_firmware/tree/master/docs/media_keys.md) Control volume and other media functions
