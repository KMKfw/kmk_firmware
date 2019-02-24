# Flashing Instructions

KMK sits on top of an existing CircuitPython install, flash that for your board
as appropriate (see [Adafruit's
documentation](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython),
though it doesn't cover all CircuitPython boards - you may need to glance around
the CircuitPython source or ask on Discord). We primarily target CircuitPython
4.0-alpha1 to 4.0-alpha3. You'll only need
to flash CircuitPython once (unless we update our baseline supported version).

After CircuitPython has been flashed, a `CIRCUITPY` drive should show up on your
computer most likely.  If not, check out the troubleshooting section below.

# Windows
Currently, we do not have an official "flasher" for windows. You can manually install it fairly easily and we recommend coming to the KMK discord/Matrix server if you have any questions. An actual tool is in development. Alternatively, you can flash from any linux like tool set (Cygwin, WSL, ect) using the Linux guide below.

# Mac
Until an interactive installer is created, please follow the linux instructions replacing /mnt with /Volumes

# Linux

While in the directory for kmk, simply run this, changing the mount point and keymap name to whatever is appropriate.

```sh
make MOUNTPOINT=/mnt/CIRCUITPY USER_KEYMAP=user_keymaps/nameofyourkeymap.py
```

# Troubleshooting
## Windows
Please join us on the Discord/Matrix server and we can help you out

## Mac
Please join us on the Discord/Matrix server and we can help you out
    
## Linux/BSD
Check to see if your drive may have mounted elsewhere with a gui tool. Most will give you the directory in the GUI.
If it's not mounted, you can read up on how to mount a drive manually here. https://wiki.archlinux.org/index.php/File_systems#Mount_a_file_system

It would look something like this

`sudo mount -o uid=1000,gid=1000 /dev/sdf1 ~/mnt`

If you still are having issues, come say hi in the Discord/Matrix servers and we'll help you out.
