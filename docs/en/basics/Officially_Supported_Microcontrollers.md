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

### Pre-compiling KMK for nice!nano (or any other microcontroller with limited flash)
As the nice!nano has limited flash memory you'll need to use a [compiled KMK](Getting_Started.md#pre-compiling-kmk-for-faster-boot-times-or-microcontrollers-with-limited-flash).

## ItsyBitsy M4 Express
Features include
- Affordable at $15 USD
- Can run most features of KMK including RGB

Downsides
- Needs to be adapted to work with Pro Micro pinout keyboards. You can find a tutorial and files for such an adapter [in our GitHub repository under /hardware](https://github.com/KMKfw/kmk_firmware/tree/master/hardware)

## RP2040
Features include
- Very affordable
- Very powerful for the price

Downsides
- Little support for keyboard kits

## Adafruit ItsyBitsy nRF52840 Express
Features include
- Both USB HID and Bluetooth support
- More affordable than the nice!nano at only $18

Downsides
- Needs to be adapted to work with Pro Micro pinout keyboards. You can find a tutorial and files for such an adapter [in our GitHub repository under /hardware](https://github.com/KMKfw/kmk_firmware/tree/master/hardware)
- No battery support without addon board like [this one by adafruit](https://www.adafruit.com/product/2124) 

## Other microcontrollers
What you'll need to have at minimum
- CircuitPython
- 256KB of flash storage
- HID over USB and/or Bluetooth.

Please keep in mind that KMK relies on CircuitPython's ability to use Bluetooth Low Energy with any given controller.
