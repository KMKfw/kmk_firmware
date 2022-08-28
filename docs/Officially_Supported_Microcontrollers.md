# Officially supported microcontrollers
While most CircuitPython devices are great for hand wired keyboards, most
keyboards are designed to accept a Pro Micro. The boards listed below either 
are, or can be adapted to that pinout to use common keyboards already on the market.

## nice!nano
Features include
- Pro Micro pinout
- Both USB HID and Bluetooth support
- Can do Bluetooth split keyboards with no wires at all
- Has battery support including charging

Downsides
- $25 USD per microcontroller at most retailers
- Not enough space to run KMK without compiling

### Pre-compiling KMK for nice!nano
As the nice!nano has limited flash memory you'll need to compile KMK. To do that you'll need to download and install the [compatible mpy-cross](https://adafruit-circuit-python.s3.amazonaws.com/index.html?prefix=bin/mpy-cross/) for your Operating System. Don't forget to add it to your PATH, test by running `mpy-cross` from a shell (Powershell, Bash, Fish, etc). Once that's set up, run either `make compile` (if you have `make`) or `python util/compile.py`to generate the `.mpy` versions of KMK files. Then copy the whole compiled `kmk/` directory to your keyboard.


Common Retailers
- [Boardsource](https://boardsource.xyz/store/5f4a1733bbaa5c635b83ed67)
- [Nice Keyboards](https://nicekeyboards.com/nice-nano/)

## ItsyBitsy M4 Express
Features include
- Affordable at $15 USD
- Can run most features of KMK including RGB

Downsides
- Needs adapted to work with Pro Micro pinout keyboards. Adapter can be found 
[HERE](https://github.com/KMKfw/kmk_firmware/tree/master/hardware)

Common Retailers
- [Adafruit](https://www.adafruit.com/product/3800)

## RP2040
Features include
- Very affordable
- Very powerful for the price

Downsides
- Little support for keyboard kits

Common Retailers
- [Adafruit](https://www.adafruit.com/pico?src=raspberrypi)
- [SparkFun](https://www.sparkfun.com/products/17829?src=raspberrypi)

## Adafruit ItsyBitsy nRF52840 Express
Features include
- Both USB HID and Bluetooth support
- More affordable than the nice!nano at only $18

Downsides
- Needs adapted to work with Pro Micro pinout keyboards. Adapter can be found
[HERE](https://github.com/KMKfw/kmk_firmware/tree/master/hardware)
- No battery support without addon board found 
[HERE](https://www.adafruit.com/product/2124) 

Common Retailers
- [Adafruit](https://www.adafruit.com/product/4481)

## Other microcontrollers
What you'll need to have at minimum
- CircuitPython
- 256KB of flash storage
- HID over USB and/or Bluetooth.
