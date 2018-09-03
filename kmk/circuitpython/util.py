import time

import board
import digitalio


def feather_red_led_flash(duration=10, rate=0.5):
    '''
    Flash the red LED for $duration seconds, alternating every $rate
    '''

    rled = digitalio.DigitalInOut(board.LED1)
    rled.direction = digitalio.Direction.OUTPUT

    for cycle in range(duration / rate):
        rled.value = cycle % 2
        time.sleep(rate)
