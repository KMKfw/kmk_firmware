import sys

from kmk.circuitpython.util import feather_red_led_flash
from kmk_keyboard_user import main

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        sys.print_exception(e)
        feather_red_led_flash(duration=10, rate=0.5)
        sys.exit(1)
