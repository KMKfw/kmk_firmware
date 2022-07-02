# KMK: Clackety Keyboards Powered by Python
![GitHub](https://img.shields.io/github/license/KMKfw/kmk_firmware)
![GitHub contributors](https://img.shields.io/github/contributors/KMKfw/kmk_firmware)
![Discord](https://img.shields.io/discord/493256121075761173?logo=Discord)
![Lines of code](https://img.shields.io/tokei/lines/github/KMKfw/kmk_firmware)
![GitHub issues](https://img.shields.io/github/issues-raw/KMKfw/kmk_firmware)
![GitHub closed issues](https://img.shields.io/github/issues-closed/KMKfw/kmk_firmware)

Documentation available at [📖 kmkfw.io](http://kmkfw.io/).

KMK is a feature-rich and beginner-friendly firmware for computer keyboards
written and configured in
[CircuitPython](https://github.com/adafruit/circuitpython).

**KMK is currently looking for maintainers.** If you like keyboards and/or
Python, and ideally have contributed to KMK in the past, and are interested in
(co-)maintaining KMK, comment on [the relevant GitHub
issue](https://github.com/KMKfw/kmk_firmware/issues/196) or drop by the Matrix
channel below.

> If you need support with KMK or just want to say hi, find us in
> [#kmkfw:klar.sh on Matrix](https://matrix.to/#/#kmkfw:klar.sh).  This channel
> is bridged to Discord
> [here](https://discord.gg/QBHUUpeGUd) for
> convenience.

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
- [Built-in Unicode macros, including
  emojis](https://github.com/KMKfw/kmk_firmware/blob/master/docs/sequences.md)
- [RGB underglow](https://github.com/KMKfw/kmk_firmware/blob/master/docs/rgb.md)
  and [LED
  backlights](https://github.com/KMKfw/kmk_firmware/blob/master/docs/led.md)
- One key can turn into many more based on [how many times you tap
  it](https://github.com/KMKfw/kmk_firmware/blob/master/docs/tapdance.md)
- Bluetooth HID and split keyboards. No more wires.

## Getting Started
KMK requires [CircuitPython](https://circuitpython.org/) version 7.0 or higher.
Our getting started guide can be found
[here](https://github.com/KMKfw/kmk_firmware/blob/master/docs/Getting_Started.md).

## The KMK Team

KMK was originally authored by @klardotsh and @kdb424 over the winter of
2018-19, and has been contributed to by numerous others since. Contributions
are welcome from all, whether it's in the form of code, documentation, hardware
designs, feature ideas, or anything else that comes to mind. A list of KMK's
contributors can be found [on
GitHub](https://github.com/KMKfw/kmk_firmware/graphs/contributors).

> While Adafruit employees and affiliates are occasionally found in the commit
> log and their help has been crucial to KMK's success, KMK is not an official
> Adafruit project, and the Core team is not compensated by Adafruit for its
> development.

## Code Style

KMK uses [Black](https://github.com/psf/black) with a Python 3.6 target and,
[(controversially?)](https://github.com/psf/black/issues/594) single quotes.
Further code styling is enforced with isort and flake8 with several plugins.
`make fix-isort fix-formatting` before a commit is a good idea, and CI will fail
if inbound code does not adhere to these formatting rules. Some exceptions are
found in `setup.cfg` loosening the rules in isolated cases, notably
`user_keymaps` (which is *also* not subject to Black formatting for reasons
documented in `pyproject.toml`).

## Tests

Unit tests within the `tests` folder mock various CircuitPython modules to allow
them to be executed in a desktop development environment.

Execute tests using the command `python -m unittest`.

## License, Copyright, and Legal

All software in this repository is licensed under the [GNU Public License,
version 3](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)).
All documentation and hardware designs are licensed under the [Creative Commons
Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
license. Contributions to this repository must use these licenses unless
otherwise agreed to by the Core team.

**Due to ethical and legal concerns, any works derived from GitHub Copilot or
similar artificial intelligence tooling are unacceptable for inclusion in any
first-party KMK repository or other code collection. We further recommend not
using GitHub Copilot while developing anything KMK-related, regardless of
intent to submit upstream.**
