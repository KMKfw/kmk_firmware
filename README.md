# KMK: Clackety Keyboards Powered by Python

KMK is a feature-rich and beginner-friendly firmware for computer keyboards
written and configured in
[CircuitPython](https://github.com/adafruit/circuitpython). **KMK is currently
in public beta, however should handle almost all workflows without major
issues**.

You can always find the latest releases on our CDN, in [compiled and
optimized](https://cdn.kmkfw.io/kmk-latest.zip) and [raw, hackable text
file](https://cdn.kmkfw.io/kmk-latest.unoptimized.zip) forms. These follow the
`master` branch here on GitHub.

> If you need support with KMK or just want to say hi, find us in
> [#kmkfw:klar.sh on Matrix](https://matrix.to/#/#kmkfw:klar.sh).  This channel
> is bridged to Discord
> [here](https://discordapp.com/widget?id=493256121075761173&theme=dark) for
> convenience.
>
> If you ask for help on chat or open a bug report, if possible please give us
> your commit SHA, found by running `from kmk.consts import KMK_RELEASE;
> print(KMK_RELEASE)` in the REPL on your controller.

## Features

- Fully configured through a single, easy to understand Python file that lives
  on a "flash-drive"-esque space on your microcontroller - edit on the go
  without DFU or other devtooling available!
- Single-piece or [two-piece split
  keyboards](https://github.com/KMKfw/kmk_firmware/blob/master/docs/split_keyboards.md)
  are supported
- [Chainable
  keys](https://github.com/KMKfw/kmk_firmware/blob/master/docs/keys.md) such as
  `KC.LWIN(KC.L)` to lock the screen on a Windows PC
- [Built-in unicode macros, including
  emojis](https://github.com/KMKfw/kmk_firmware/blob/master/docs/sequences.md)
- [Multiple vim-inspired leader key
  modes](https://github.com/KMKfw/kmk_firmware/blob/master/docs/leader.md)
- [RGB underglow](https://github.com/KMKfw/kmk_firmware/blob/master/docs/rgb.md)
  and [LED
  backlights](https://github.com/KMKfw/kmk_firmware/blob/master/docs/led.md)
- One key can turn into many more based on [how many times you tap
  it](https://github.com/KMKfw/kmk_firmware/blob/master/docs/tapdance.md)

Coming (hopefully) soon: Bluetooth support! Stay tuned.

## Getting Started

- Start by grabbing a supported microcontroller. Broadly speaking, KMK supports
  any device CircuitPython does, but KMK requires a decent bit of RAM, and in
  general requires a working USB HID stack, which leads us to recommend the
  following controllers:

  * [Adafruit ItsyBitsy M4 Express](https://www.adafruit.com/product/3800)\*
  * [Adafruit Feather M4 Express](https://www.adafruit.com/product/3857)
  * [Adafruit Feather nRF52840 Express](https://www.adafruit.com/product/4062)
  * [MakerDiary nRF52840 MDK](https://store.makerdiary.com/collections/frontpage/products/nrf52840-mdk-iot-development-kit)
  * [SparkFun Pro nRF52840 Mini](https://www.sparkfun.com/products/15025)

  > \* The ItsyBitsy M4 Express is the only controller we currently support in
  > non-handwired configurations, using our [ItsyBitsy to Pro Micro converter
  > PCB](https://github.com/KMKfw/kmk_firmware/tree/master/hardware) designed by
  > @siddacious and @kdb424. It is our most-recommended MCU until [the ItsyBitsy is
  > updated with an nRF52840
  > chip](https://blog.adafruit.com/2019/01/26/comingsoon-itsybitsy-nrf52480-runs-circuitpython-adafruit-circuitpython-adafruit-circuitpython/)

  > Some other controllers, such as the [Feather M0 Express](https://www.adafruit.com/product/3403),
  > are usable in reduced functionality modes and may require custom hackery.
  > For example, @kdb424 uses a ItsyBitsy M0 Express as a barebones matrix scanner
  > in a split keyboard configuration
  > [here](https://github.com/KMKfw/kmk_firmware/commit/1f84079dc8aadeb9627c4762d9f9fb855292c4a2).
  > Use such controllers at your own risk.

- Ensure CircuitPython 4.0.0 or newer is installed on your controller. We
  recommend the latest stable version from
  [circuitpython.org](https://circuitpython.org/downloads). Flashing
  instructions vary by device: all Adafruit boards can be flashed [using their
  instructions](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython),
  other boards generally have their instructions [in the CircuitPython
  repository](https://github.com/adafruit/circuitpython) under the
  `ports/atmel-samd/boards/<your board here>` and `ports/nrf/boards/<your board
  here>` directories. If all else fails, consult your device's official
  documentation.

- [Download the latest KMK release](https://cdn.kmkfw.io/kmk-latest.zip) and
  extract the zip to the USB drive exposed by CircuitPython, typically labeled
  `CIRCUITPY`.  Again, [we'll defer to Adafruit's
  documentation](https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries)
  on adding libraries to a CircuitPython installation. You should end up with a
  folder called `kmk` and a file called `boot.py`, both living at the top of
  this USB drive.

- Define your keyboard in a file called `main.py` on this `CIRCUITPY` drive and
  get tinkering! Examples of both handwired and ProMicro-\>ItsyBitsy converted
  boards exist under the `user_keymaps/` tree, and feel free to submit a pull
  request of your own definitions! At this point, you'll want to look through
  `docs/` in the source tree to explore the functionality at your disposal.

> Linux, BSD, and MacOS users can also make use of the `Makefile` provided in
> this source tree to flash KMK and a keymap using `rsync`. This is advanced
> functionality outside the scope of this README, but it's documented in the
> `docs/` tree.

## The KMK Team

KMK is primarily written and maintained by @klardotsh and @kdb424, but
contributions are welcome from all, whether it's in the form of code,
documentation, hardware designs, feature ideas, or anything else that comes to
mind. KMK's contributors and other helpers are listed alphabetically by username
below (we'll try to keep this up to date!):

- [Dan Halbert (@dhalbert)](https://github.com/dhalbert)
- [Elvis Pfützenreuter (@elvis-epx)](https://github.com/elvis-epx)
- [Kyle Brown (@kdb424)](https://github.com/kdb424)
- [Josh Klar (@klardotsh)](https://github.com/klardotsh)
- [Limor Fried (@ladyada)](https://github.com/ladyada)
- [Ryan Karpinski (@rk463345)](https://github.com/rk463345)
- [@siddacious](https://github.com/siddacious)
- [Scott Shawcroft (@tannewt)](https://github.com/tannewt)

> While Adafruit employees and affiliates are included in the above list and
> their help has been crucial to KMK's success, KMK is not an official Adafruit
> project, and the Core team is not compensated by Adafruit for its development.

## Code Style

KMK uses [Black](https://github.com/psf/black) with a Python 3.6 target and,
[(controversially?)](https://github.com/psf/black/issues/594) single quotes.
Further code styling is enforced with isort and flake8 with several plugins.
`make fix-isort fix-formatting` before a commit is a good idea, and CI will fail
if inbound code does not adhere to these formatting rules. Some exceptions are
found in `setup.cfg` loosening the rules in isolated cases, notably
`user_keymaps` (which is *also* not subject to Black formatting for reasons
documented in `pyproject.toml`).

## License, Copyright, and Legal

All software in this repository is licensed under the [GNU Public License,
verison 3](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)).
All documentation and hardware designs are licensed under the [Creative Commons
Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
license. Contributions to this repository must use these licenses unless
otherwise agreed to by the Core team.
