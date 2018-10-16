def main():
    import sys

    from kmk.circuitpython.hid import HIDHelper
    from kmk.firmware import Firmware
    from kmk.matrix import MatrixScanner

    import kmk_keyboard

    cols = getattr(kmk_keyboard, 'cols')
    diode_orientation = getattr(kmk_keyboard, 'diode_orientation')
    keymap = getattr(kmk_keyboard, 'keymap')
    rows = getattr(kmk_keyboard, 'rows')

    debug_enable = getattr(kmk_keyboard, 'debug_enable', False)

    if debug_enable:
        from logging import DEBUG as log_level
    else:
        from logging import ERROR as log_level

    try:
        firmware = Firmware(
            keymap=keymap,
            row_pins=rows,
            col_pins=cols,
            diode_orientation=diode_orientation,
            log_level=log_level,
            matrix_scanner=MatrixScanner,
            hid=HIDHelper,
        )

        firmware.go()
    except Exception as e:
        sys.print_exception(e)
        sys.exit(1)
