# Officially supported microcontrollers
While most Circuitpython devices are great for hand wired keyboards, most 
keyboards are designed to accept a Pro Micro. The boards listed below either 
are, or can be adapted to that pinout to use common keyboards already on the market.

## ItsyBitsy M4 Express
Features include
- Affordable at $15 USD
- Can run most features of KMK including RGB

Downsides
- Needs adapted to work with Pro Micro pinout keyboards. Adapter can be found 
[HERE](https://github.com/KMKfw/kmk_firmware/tree/master/hardware)

Common Retailers
[Adafruit](https://www.adafruit.com/product/3800)

## RP2040
Features include
- Very affordable
- Very powerful for the price

Downsides
- Little support for keyboard kits

Common Retailers
[Adafruit](https://www.adafruit.com/pico?src=raspberrypi)
[Sparkfun](https://www.sparkfun.com/products/17829?src=raspberrypi)

## Adafruit ItsyBitsy nRF52840 Express
Features include
- Both USB HID and Bluetooth support
- More affordable than the Nice!Nano at only $18

Downsides
- Needs adapted to work with Pro Micro pinout keyboards. Adapter can be found
[HERE](https://github.com/KMKfw/kmk_firmware/tree/master/hardware)
- No battery support without addon board found 
[HERE](https://www.adafruit.com/product/2124) 

Common Retailers
[Adafruit](https://www.adafruit.com/product/4481)

## Other microcontrollers
What you'll need to have at minimum
- CircuitPython
- 256KB of flash storage
- HID over USB and/or Bluetooth.
