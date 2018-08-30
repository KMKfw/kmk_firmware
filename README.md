# kmk_firmware

Mechanical keyboard firmware for humans (and ARM microcontrollers)

KMK is a work-in-progress and proof-of-concept firmware for (usually mechanical)
keyboards, written in
[CircuitPython](https://github.com/adafruit/circuitpython), a fork of
[MicroPython](https://micropython.org/). This allows for high-level and
expressive keyboard programming and creature comforts that C simply doesn't
make easy. KMK was heavily inspired by QMK - in fact, KMK was only created
because QMK didn't correctly support some hardware I bought, and hacking support
in was going to be a heavy uphill battle.

This project is currently written and maintained by @klardotsh and @kdb424.


## Supported Devices

### Officially Supported
- [Adafruit Feather nRF52 BLE Controller](https://www.adafruit.com/product/3406)

### Support Planned/WIP
- [Planck rev6 Keyboard](https://olkb.com/planck)
- [Proton C
  Controller?](https://www.reddit.com/r/MechanicalKeyboards/comments/87cw36/render_of_the_qmk_proton_c_qmkpowered_pro_micro/)
    * Does not exist yet, basically a Planck6 in a Pro Micro pin-compat controller chip
- [Teensy 3.2 Controller](https://www.adafruit.com/product/2756)
    * Has at least MicroPython, possibly CircuitPython as well


## Unsupported Devices

If you don't see it in "Supported Devices", it won't work out of the box, it's
basically that simple. Pull requests are welcome and encouraged to add support
for new keyboards. The base requirements for device support are a port of
CircuitPython (technically base MicroPython could still work), at least
256KB of flash storage, and USB and/or Bluetooth LE interfaces. DFU
bootloaders are very strongly encouraged, but not required.

Devices require at least 256KB of flash to run KMK, and that's already pretty
tight. In general this means that no or almost no Arduinos are or will ever be
supported. This extends to Arduino-compatibles, including the Pro Micro. If you
want to run custom firmware on your Pro Micro-equipped keyboard, or for that
matter anything running the ATmega32U4 (Let's Split, Plancks before rev6,
hundreds of others), check out [QMK](https://github.com/qmk/qmk_firmware), the
biggest influence of KMK by far. They're great people.


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
