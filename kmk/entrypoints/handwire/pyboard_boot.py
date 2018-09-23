import pyb

pyb.usb_mode('VCP+HID', hid=pyb.hid_keyboard)  # act as a serial device and a mouse
