import sys
from logging import DEBUG

from kmk.common.consts import UnicodeModes
from kmk.firmware import Firmware
from kmk.micropython.pyb_hid import HIDHelper


def main():
    from kmk_keyboard_user import cols, diode_orientation, keymap, rows

    try:
        from kmk_keyboard_user import unicode_mode
    except Exception:
        unicode_mode = UnicodeModes.NOOP

    try:
        firmware = Firmware(
            keymap=keymap,
            row_pins=rows,
            col_pins=cols,
            diode_orientation=diode_orientation,
            unicode_mode=unicode_mode,
            hid=HIDHelper,
            log_level=DEBUG,
        )

        firmware.go()
    except Exception as e:
        sys.print_exception(e)
        sys.exit(1)
