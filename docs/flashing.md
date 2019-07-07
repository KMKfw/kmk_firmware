# Flashing Instructions

KMK sits on top of an existing CircuitPython install, flash that for your board
as appropriate (see [Adafruit's
documentation](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython),
though it doesn't cover all CircuitPython boards - you may need to glance around
the CircuitPython source or ask on Discord). We primarily target CircuitPython
4.0-alpha1 and above, though many features should work on 3.x. You'll only need
to flash CircuitPython once (unless we update our baseline supported version).

After CircuitPython has been flashed, a `CIRCUITPY` drive should show up on your
computer (some Linux/BSD users without drive automounting will want to poke
around `dmesg` to find the drive identifier and mount this drive manually
somewhere - ex. `mkdir -p ~/mnt && sudo mount -o uid=1000,gid=1000 /dev/sdf1
~/mnt`, where `uid` and `gid` are your user ID and primary group ID, as found in
`id -u` and `id -g`). Take note of the path that this is mounted to (for MacOS
users, this will probably look something like `/Volumes/CIRCUITPY`).

To "flash" all of KMK, your keymap, and a basic `main.py` that will start
everything up, run `make MOUNTPOINT=/path/to/wherever
USER_KEYMAP=path/to/keymap.py`. For example, if my `CIRCUITPY` volume is mounted
to `~/mnt`, I might flash my development breadboard with the following:

```sh
make MOUNTPOINT=~/mnt USER_KEYMAP=user_keymaps/klardotsh/itsybitsy_m4_express/threethree.py
```
