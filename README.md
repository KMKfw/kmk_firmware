# KMK: Clackety Keyboards Powered by Python

KMK is a feature-rich and beginner-friendly firmware for computer keyboards
written and configured in
[CircuitPython](https://github.com/adafruit/circuitpython). **KMK is currently
in public beta, however should handle most workflows without major issues**.

<!--
@klardotsh 06 July 2021: commented for now because CDN builds have been broken
for ages and folks are (reasonably) getting confused.

You can always find the latest releases on our CDN, in [compiled and
optimized](https://cdn.kmkfw.io/kmk-latest.zip) and [raw, hackable text
file](https://cdn.kmkfw.io/kmk-latest.unoptimized.zip) forms. These follow the
`master` branch here on GitHub.
-->

> If you need support with KMK or just want to say hi, find us in
> [#kmkfw:klar.sh on Matrix](https://matrix.to/#/#kmkfw:klar.sh).  This channel
> is bridged to Discord
> [here](https://discordapp.com/widget?id=493256121075761173&theme=dark) for
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
- [Built-in unicode macros, including
  emojis](https://github.com/KMKfw/kmk_firmware/blob/master/docs/sequences.md)
- [RGB underglow](https://github.com/KMKfw/kmk_firmware/blob/master/docs/rgb.md)
  and [LED
  backlights](https://github.com/KMKfw/kmk_firmware/blob/master/docs/led.md)
- One key can turn into many more based on [how many times you tap
  it](https://github.com/KMKfw/kmk_firmware/blob/master/docs/tapdance.md)
- Bluetooth HID and split keyboards. No more wires.

## Getting Started

Our getting started guide can be found
[here](https://github.com/KMKfw/kmk_firmware/blob/master/docs/Getting_Started.md)

## The KMK Team

KMK is primarily written and maintained by @klardotsh and @kdb424, but
contributions are welcome from all, whether it's in the form of code,
documentation, hardware designs, feature ideas, or anything else that comes to
mind. A list of KMK's contributors can be found [on
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

## License, Copyright, and Legal

All software in this repository is licensed under the [GNU Public License,
verison 3](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)).
All documentation and hardware designs are licensed under the [Creative Commons
Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
license. Contributions to this repository must use these licenses unless
otherwise agreed to by the Core team.
