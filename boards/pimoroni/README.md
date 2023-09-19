# Pimoroni Keybow family

A family of macro pads based on raspberry pi hardware:
![Keybow](image URL for keybow)
(Original) Keybow - Raspberry Pi hat. 4x3 hotswap keys, with an APA102 LED per key.

![Keybow 2040](image URL for keybow 2040)
Keybow 2040 - custom RP2040 board. 4x4 hotswap keys, with an RGB LED per key driven by a shared IS31FL3731 controller.

These boards share the 'feature' of using a single GPIO per key rather than a row and column matrix, so these both
use CircuitPython's `keypad.Keys` module instead of the regular KMK matrix scanner.


Extensions enabled by default  
- [Layers](/docs/en/layers.md) Need more keys than switches? Use layers.
- [RGB](/docs/en/rgb.md) Light it up (Keybow only so far)
- [MediaKeys](/docs/en/media_keys.md) Control volume and other media functions
