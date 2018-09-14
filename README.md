# KMK

Mechanical keyboard firmware for humans (and ARM microcontrollers)

KMK is a work-in-progress and proof-of-concept firmware for (usually mechanical)
keyboards, written in
[CircuitPython](https://github.com/adafruit/circuitpython), a fork of
[MicroPython](https://micropython.org/). This allows for high-level and
expressive keyboard programming and creature comforts that C simply doesn't
make easy. KMK was heavily inspired by QMK - in fact, KMK was only created
because QMK didn't correctly support some hardware I bought, and hacking support
in was going to be a heavy uphill battle.

This project is currently written and maintained by [Josh
Klar](https://github.com/klardotsh) and [Kyle Brown](https://github.com/kdb424).


## Supported Devices

| Board | Chipset | Python Platform | Notes |
| ----- | ------- | --------------- | ----- |
| [Seeed nRF52840 Micro Dev Kit](https://www.seeedstudio.com/nRF52840-Micro-Development-Kit-p-3079.html) | nRF52840 | TBD, likely CircuitPython | This is basically as bleeding edge as it gets, will likely require upstream patches to uPy/CPY, but it supports everything we need at a hardware level, unlike the nRF52832. |
| [Adafruit HUZZAH32](https://www.adafruit.com/product/3405) | ESP32 | CircuitPython | This is the HUZZAH you actually want to build a keeb with. More lanes, more better. |
| [pyboard v1.1](https://www.adafruit.com/product/2390) | STM32F405RG (Cortex M4F) | MicroPython | |

### Support Planned/WIP
- [Planck rev6 Keyboard](https://olkb.com/planck)
- [Proton C
  Controller?](https://www.reddit.com/r/MechanicalKeyboards/comments/87cw36/render_of_the_qmk_proton_c_qmkpowered_pro_micro/)
    * Does not exist yet, the controller from a Planck rev6 in a Pro Micro pin-compat controller chip


## Unsupported Devices

If you don't see it in "Supported Devices", it won't work out of the box, it's
basically that simple. Pull requests are welcome and encouraged to add support
for new keyboards. The base requirements for device support are a port of
CircuitPython or MicroPython, at least 256KB of flash storage, and USB and/or 
Bluetooth LE interfaces.

Here's a list of boards that seem like they should otherwise be supported, but
are currently not, due to some deficiency uncovered in development/testing:

| Board | Chipset | Python Platform | Reason Unsupported |
| ----- | ------- | --------------- | ------------------ |
| [Adafruit Feather nRF52 BLE Controller](https://www.adafruit.com/product/3406) | nRF52832 | CircuitPython | Lack of USB HID (HW) |
| [Adafruit Feather Huzzah](https://www.adafruit.com/product/2821) | ESP8266 | CircuitPython | Suuuuuper limited on GPIO lanes, Lack of USB HID (HW) |
| [Teensy 3.2 Controller](https://www.adafruit.com/product/2756) | | MicroPython | Lack of USB HID (SW - MP) |


## The Great Hackaround

While it is required that at least the device talking over USB/BLE HID (the
"primary brain") be from the Supported Devices list and running the primary
component of KMK, it will soon be possible to build split keyboards with other,
otherwise unsupported devices (currently this means a Pro Micro), either to
reduce costs or to convert existing QMK boards to KMK. You'll need to flash
"dummy" firmware to each Pro Micro which simply scans a matrix and passes the
values over I2C to the "brain" device, which does the heavy lifting from there
(including actually sending HID events).

The obvious downsides of this method are increased number of moving parts,
increased number of things to flash (though the Pro Micros only need flashed
when matricies change, which should almost never happen once a board is built),
and all downsides that go with those points (increased power usage, etc.) The
upside is that it can be a _ton_ cheaper to build a split keyboard this way -
cheapo Pro Micro clones can be had for as little as $4 CAD at time of writing,
whereas a HUZZAH32, for example, is closer to $26 CAD, and to build the
"traditional" way, you'd need N of them (where N is the number of split sections
of your keyboard).

It is also possible to convert many QMK boards through this fashion - while
untested for now, just about anything with a TRRS jack should work (Ergodoxen,
just about anything from keeb.io, etc.) 

This hackaround is almost certainly pointless for non-split boards.


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
https://cla-assistant.io/klardotsh/kmk_firmware). If you forget, the bots will
remind you when you open the pull request, no worries!
