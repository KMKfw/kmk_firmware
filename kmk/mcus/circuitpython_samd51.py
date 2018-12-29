from kmk.firmware import Firmware as _Firmware
from kmk.hid import CircuitPythonUSB_HID

import kmk.keycodes


class Firmware(_Firmware):
    hid_helper = CircuitPythonUSB_HID
