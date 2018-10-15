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
