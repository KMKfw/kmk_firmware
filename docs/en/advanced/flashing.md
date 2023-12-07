# Flashing Instructions

In general, we recommend using the instructions in `README.md`, however, mostly
as a development artifact, another method of flashing KMK exists (tested and
supported only on Linux, though it should also work on macOS, the BSDs, and
other Unix-likes. It may also work on Cygwin and the Windows Subsystem for
Linux).

Given `make` and `rsync` are available on your system (in `$PATH`), the
following will copy the `kmk` tree to your CircuitPython device, and will copy
the file defined as `USER_KEYMAP` as your `main.py`. It will also copy our
`boot.py`. If any of these files exist on your CircuitPython device already, they
will be overwritten without a prompt.

If you get permissions errors here, **don't run make as root or with sudo**. See
`Troubleshooting` below.

```sh
make MOUNTPOINT=/media/CIRCUITPY USER_KEYMAP=user_keymaps/nameofyourkeymap.py BOARD=board/nameofyourboard/kb.py
```

# Troubleshooting
## Linux/BSD

Check to see if your drive may have mounted elsewhere with a GUI tool or other
automounter. Most of these tools will mount your device under `/media`, probably
as `/media/CIRCUITPY`.  If it's not mounted, you can read up on how to [mount a
drive manually](https://wiki.archlinux.org/index.php/File_systems#Mount_a_file_system).

For example,

`sudo mount -o uid=$(id -u),gid=$(id -g) /dev/disk/by-label/CIRCUITPY ~/mnt`

If you're still having issues, check out our support page to see where you can
come say hi and the community will gladly help you out.
