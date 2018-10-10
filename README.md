# KMK: Mechanical keyboard firmware for humans (and ARM microcontrollers)

[![CircleCI](https://circleci.com/gh/KMKfw/kmk_firmware/tree/master.svg?style=svg)](https://circleci.com/gh/KMKfw/kmk_firmware/tree/master)[![CLA assistant](https://cla-assistant.io/readme/badge/KMKfw/kmk_firmware)](https://cla-assistant.io/KMKfw/kmk_firmware)

KMK is a firmware for (usually mechanical) keyboards, written in
[MicroPython](https://micropython.org/) and
[CircuitPython](https://github.com/adafruit/circuitpython), heavily inspired by
QMK (and with some additions of our own). Python may not be the fastest thing on
the planet, but it's a joy to write, and bringing that ease of maintainership to
keyboard firmware (often a world of C and all the crazy error states C can
provide) opens up custom keyboards to whole new demographics. KMK currently only
supports handwired keyboards (see "Supported Devices" below), but work has begun
on both ports to existing keyboards, as well as converter devices to allow
existing keyboards with Pro Micro pinouts to use KMK-supported microcontrollers.
As always in open-source, KMK is a work in progress, and help is welcome!

This project is currently written and maintained by:

- [Josh Klar (@klardotsh)](https://github.com/klardotsh)
- [Kyle Brown (@kdb424)](https://github.com/kdb424)

This project also owes a `$BEVERAGE_OF_CHOICE` to some wonderful people in the
ecosystem:

- [Jack Humbert (@jackhumbert)](https://jackhumbert.com/), for writing QMK.
  Without QMK, I'd have never been exposed to the wonderful world of
  programmable keyboards. He's also just an awesometastic human in general, if
  you ever catch him on Discord/Reddit/etc.

- [Dan Halbert (@dhalbert)](https://danhalbert.org/), for his amazing and
  unjudgemental support of two random dudes on Github asking all sorts of
  bizzare (okay...  and occasionally dumb) questions on the MicroPython and
  CircuitPython Github projects and the Adafruit Discord. Dan, without your help
  and pointers (even when those pointers are "Remember you're working with a
  microcontroller with a few MHz of processing speed and a few KB of RAM"), this
  project would have never gotten off the ground. Thank you, and an extended
  thanks to Adafruit.


## Supported Devices

| Board | Chipset | Python Platform | Notes |
| ----- | ------- | --------------- | ----- |
| [pyboard v1.1](https://www.adafruit.com/product/2390) | STM32F405RG (Cortex M4F) | MicroPython | Our reference board for basic USB keyboards |
| [Adafruit Feather M4 Express](https://www.adafruit.com/product/3857) | Atmel SAMD51 (Cortex M4F) | CircuitPython | A more economical solution for basic USB keyboards |
| [Adafruit ItsyBitsy M4 Express](https://www.adafruit.com/product/3800) | Atmel SAMD51 (Cortex M4F) | CircuitPython | An EVEN MORE economical solution for basic USB keyboards |

### Support Planned/WIP
| Board | Chipset | Python Platform | Notes |
| ----- | ------- | --------------- | ----- |
| [Seeed nRF52840 Micro Dev Kit](https://www.seeedstudio.com/nRF52840-Micro-Development-Kit-p-3079.html) | nRF52840 | [CircuitPython](https://github.com/KMKfw/circuitpython/tree/topic-nrf52840-mdk) | This is basically as bleeding edge as it gets. Will support BLE HID to PC as well as BLE split boards |
| [Planck rev6 Keyboard](https://olkb.com/planck) | STM32 of some sort | MicroPython | Requires porting MicroPython to STM32F3, this work has begun but I'm pretty terrible at it. |
| [Proton C Controller?](https://www.reddit.com/r/MechanicalKeyboards/comments/87cw36/render_of_the_qmk_proton_c_qmkpowered_pro_micro/) | ??? | ??? | Does not exist yet, the controller from a Planck rev6 in a Pro Micro pin-compat controller chip |


## Unsupported Devices

If you don't see it in "Supported Devices", it won't work out of the box, it's
basically that simple. Pull requests are welcome and encouraged to add support
for new keyboards. The base requirements for device support are a port of
CircuitPython or MicroPython, at least 256KB of flash storage, and USB and/or 
Bluetooth LE interfaces.

Here's a list of boards that seem like they should otherwise be supported, but
are currently not, due to some deficiency uncovered in development/testing:

| Board | Chipset | Python Platform | Notes |
| ----- | ------- | --------------- | ------------------ |
| [Adafruit Feather Huzzah](https://www.adafruit.com/product/2821) | ESP8266 | CircuitPython | Suuuuuper limited on GPIO lanes, Lack of USB HID (HW) |
| [Adafruit HUZZAH32](https://www.adafruit.com/product/3405) | ESP32 | MicroPython | In theory this may work as a BLE HID device, or with a GPIO-based USB breakout. Right now, we haven't written the code for this device. Built-in USB port can't run in HID at all. |
| [Adafruit Feather nRF52 BLE Controller](https://www.adafruit.com/product/3406) | nRF52832 | CircuitPython | Lack of USB HID (HW), but could be fixed with GPIO USB breakout. BLE HID could be possible, but it's considered somewhat unstable. This chip is considered "mostly unsupported" in CircuitPython according to Adafruit Discord, so I've mostly abandoned it for now. |
| [Teensy 3.2 Controller](https://www.adafruit.com/product/2756) | | MicroPython | Lack of USB HID (SW - MP) |


## License, Copyright, and Legal

This project, and all source code within (even if the file is missing headers),
is licensed
[GPLv3](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)) -
while the tl;dr is linked, the full license text is included in `LICENSE.md` at
the top of this source tree.

When contributing for the first time, you'll need to sign a Contributor
Licensing Agreement which is based on the Free Software Foundation's CLA. The
CLA is basically a two-way promise that this code is and remains yours, but will
be distributed as part of a larger GPLv3 project. If you'd like to get it out of
the way early, you can find said CLA [here](
https://cla-assistant.io/kmkfw/kmk_firmware). If you forget, the bots will
remind you when you open the pull request, no worries!
