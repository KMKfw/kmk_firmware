# KMK: Python-based keyboard firmware for humans (and ARM microcontrollers)

[![CircleCI](https://circleci.com/gh/KMKfw/kmk_firmware/tree/master.svg?style=svg)](https://circleci.com/gh/KMKfw/kmk_firmware/tree/master)[![CLA assistant](https://cla-assistant.io/readme/badge/KMKfw/kmk_firmware)](https://cla-assistant.io/KMKfw/kmk_firmware)

#### [Join our Matrix community for chat and support!](https://matrix.to/#/+kmk:kmkfw.io)

[Or, head directly to the #support channel](https://matrix.to/#/#support:kmkfw.io)

If you can't or won't use the Matrix infrastructure, a (possibly fragile) bridge
to Discord exists
[here](https://discordapp.com/widget?id=493256121075761173&theme=dark).

<hr/>

KMK is a firmware for (usually mechanical) keyboards, running on
[CircuitPython](https://github.com/adafruit/circuitpython). It aims to provide a
means to write complex keyboard configurations quickly, without having to learn
much "real" programming, while preserving at least some of the hackability and
DIY spirit of CircuitPython. Learn more about the rationale of KMK in `Why KMK?`
below.

This project is currently written and maintained by:

- [Josh Klar (@klardotsh)](https://github.com/klardotsh)
- [Kyle Brown (@kdb424)](https://github.com/kdb424)

With community help from:

- [@siddacious](https://github.com/siddacious)
- [Scott Shawcroft (@tannewt)](https://github.com/tannewt)

> Scott is the lead developer of the CircuitPython project itself at Adafruit.
> KMK, however, is not officially sponsored by Adafruit, and is an independent
> project.

Lastly, we'd like to make a couple of shoutouts to people not directly
affiliated with the project in any way, but who have helped or inspired us along
the way:

- [Jack Humbert (@jackhumbert)](https://jackhumbert.com/), for writing QMK.
  Without QMK, I'd have never been exposed to the wonderful world of
  programmable keyboards. He's also just an awesometastic human in general, if
  you ever catch him on Discord/Reddit/etc. Jack also makes fantastic hardware -
  check out [his store](https://olkb.com)!

- [Dan Halbert (@dhalbert)](https://danhalbert.org/), for his amazing and
  unjudgemental support of two random dudes on Github asking all sorts of
  bizzare (okay...  and occasionally dumb) questions on the MicroPython and
  CircuitPython Github projects and the Adafruit Discord. Dan, without your help
  and pointers (even when those pointers are "Remember you're working with a
  microcontroller with a few MHz of processing speed and a few KB of RAM"), this
  project would have never gotten off the ground. Thank you, and an extended
  thanks to Adafruit.

## Why KMK?

A question we get from time to time is, "why bother with KMK when QMK already
exists?", so here's a short bulleted list of our thoughts on the matter (in no
particular order):

- Python is awesome
- Python is super easy to write
- Python provides fewer footguns than C
- KMK cut all the "tech debt" of supporting AVR controllers, and frankly even
  most ARM controllers with under 256KB of flash. This let us make some very
  user-friendly (in our biased opinions) design decisions that should make it
  simple for users to create even fairly complex keyboards - want a key on your
  board that sends a shruggie (`¯\_(ツ)_/¯`)? No problem - it's supported out of
  the box. Want a single key that can act as all 26 alphabet characters
  depending on the number of times it's tapped? You're insane, but our simple
  Tap Dance implementation has you covered (without a single line of matrix
  mangling or timer madness)
- KMK supports a few small features QMK doesn't - most are probably not
  deal-closers, but they exist no less. Probably the most notable addition here
  is `Leader Mode - Enter`. Check out `docs/leader.md` for details on that.
- KMK plans to support some fairly powerful hardware that would enable things
  like connecting halves (or thirds, or whatever) of a split keyboard to each
  other via Bluetooth. This stuff is still in very early R&D.

## So how do I use it?

Since KMK is still in some state between "alpha" and "beta", flashing KMK to a
board is still a process that requires a few lines of shell scripting. Check out
`docs/flashing.md` for instructions/details, though note that for now, the
instructions mostly assume Unix (Linux/MacOS/BSD) usage. You may want to check
out the Windows Subsystem for Linux if you're on Windows.

## License, Copyright, and Legal

Most files in this project are licensed
[GPLv3](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)) -
see `LICENSE.md` at the top of this source tree for exceptions and the full
license text.

When contributing for the first time, you'll need to sign a Contributor
Licensing Agreement which is based on the Free Software Foundation's CLA. The
CLA is basically a two-way promise that this code is and remains yours, but will
be distributed as part of a larger GPLv3 project. If you'd like to get it out of
the way early, you can find said CLA [here](
https://cla-assistant.io/kmkfw/kmk_firmware). If you forget, the bots will
remind you when you open the pull request, no worries!
