import pyb

from kmk.micropython.pyb_hid import generate_pyb_hid_descriptor

# act as a serial device and a KMK device
pyb.usb_mode('VCP+HID', hid=generate_pyb_hid_descriptor())
