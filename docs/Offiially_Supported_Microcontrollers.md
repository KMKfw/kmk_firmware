# Officially supported microcontrollers
While most Circuitpython devices are great for hand wired keyboards, most 
keyboards are designed to accept a Pro Micro. The boards listed below either 
are, or can be adapted to that pinout to use common keyboards already on the market.

## Nice!Nano
Features include
- Pro Micro pinout
- Both USB HID and Bluetooth support
- Can do bluetooth split keyboards with no wires at all
- Has battery support including charging

Downsides
- $25 USD per microcontroller at most retailers

Recommended Retailers
[Boardsource](https://boardsource.xyz/store/5f4a1733bbaa5c635b83ed67)
[NiceKeyboards](https://nicekeyboards.com/collections/group-buy/products/nice-nano-v1-0).

## ItsyBitsy M4 Express
Features include
- Affordable at $15 USD
- Can run most features of KMK including RGB

Downsides
- Needs adapted to work with Pro Micro pinout keyboards. Adapter can be found 
[HERE](https://github.com/KMKfw/kmk_firmware/tree/master/hardware)

Recommended Retailers
[Adafruit](https://www.adafruit.com/product/3800)

## Adafruit ItsyBitsy nRF52840 Express
Features include
- Both USB HID and Bluetooth support
- More affordable than the Nice!Nano at only $18

Downsides
- Needs adapted to work with Pro Micro pinout keyboards. Adapter can be found
[HERE](https://github.com/KMKfw/kmk_firmware/tree/master/hardware)
- No battery support without addon board found 
[HERE](https://www.adafruit.com/product/2124) 

## Other microcontrollers
What you'll need to have at minimum
- CircuitPython/KMKpython
- 256KB of flash storage
- HID over USB and/or Bluetooth.
