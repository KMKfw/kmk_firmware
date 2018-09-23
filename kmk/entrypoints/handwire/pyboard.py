import sys
from logging import DEBUG

from kmk.firmware import Firmware
from kmk.micropython.pyb_hid import HIDHelper


def main():
    from kmk_keyboard_user import cols, diode_orientation, keymap, rows

    try:
        firmware = Firmware(
            keymap=keymap,
            row_pins=rows,
            col_pins=cols,
            diode_orientation=diode_orientation,
            hid=HIDHelper,
            log_level=DEBUG,
        )

        firmware.go()
    except Exception as e:
        sys.print_exception(e)
        sys.exit(1)
