import sys
import time

import board
import digitalio


def feather_signal_error_with_led_flash(rate=0.5):
    '''
    Flash the red LED for 10 seconds, alternating every $rate
    Could be useful as an uncaught exception handler later on,
    but is for now unused
    '''

    rled = digitalio.DigitalInOut(board.LED1)
    rled.direction = digitalio.Direction.OUTPUT

    # blink for 5 seconds and exit
    for cycle in range(10):
        rled.value = cycle % 2
        time.sleep(rate)

    sys.exit(1)
