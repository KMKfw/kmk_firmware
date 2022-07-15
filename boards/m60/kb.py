import analogio
import microcontroller
import supervisor
from board import VOLTAGE_MONITOR, RGB_POWER
from board import R1, R2, R3, R4, R5, R6, R7, R8, C1, C2, C3, C4, C5, C6, C7, C8
from digitalio import DigitalInOut, Direction, Pull
from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation

BATTERY_LIMIT = 3100  # Cutoff voltage [mV].
BATTERY_FULLLIMIT = 4190  # Full charge definition [mV].
BATTERY_DELTA = 10  # mV between each element in the SoC vector.

BATTERY_VOLTAGE = (
    0,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,
    2,  2,  2,  2,  2,  2,  2,  2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,
    4,  5,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 11, 12, 13, 13, 14, 15, 16,
    18, 19, 22, 25, 28, 32, 36, 40, 44, 47, 51, 53, 56, 58, 60, 62, 64, 66, 67, 69,
    71, 72, 74, 76, 77, 79, 81, 82, 84, 85, 85, 86, 86, 86, 87, 88, 88, 89, 90, 91,
    91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 100
)

battery_in = analogio.AnalogIn(VOLTAGE_MONITOR)

class KMKKeyboard(_KMKKeyboard):
    battery_power_pin = microcontroller.pin.P0_28
    rgb_power = RGB_POWER
    col_pins = (C1, C2, C3, C4, C5, C6, C7, C8)
    row_pins = (R1, R2, R3, R4, R5, R6, R7, R8)

    diode_orientation = DiodeOrientation.COLUMNS

    coord_mapping = [
        0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13,
        27,26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14,
        28,29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,     40,
        52,51, 50, 49, 48, 47, 46, 45, 44, 43, 42,         41,
        53,  54, 55,             56,           57, 58, 59, 60
    ]

    def __init__(self):
        print("M60 Keyboard init...")

    def battery_power_on(self):
        #bttn = DigitalInOut(BTN)
        #bttn.direction = Direction.OUTPUT
        #bttn.value = False
        power_pin = DigitalInOut(self.battery_power_pin)
        power_pin.direction = Direction.INPUT
        power_pin.pull = Pull.UP

    def battery_level(self):
        # (3300 * 2 * battery.value) >> 16
        voltage = (3300 * battery_in.value) >> 15
        i = (voltage - BATTERY_LIMIT) // BATTERY_DELTA
        if i >= len(BATTERY_VOLTAGE):
            i = len(BATTERY_VOLTAGE) - 1
        elif i < 0:
            i = 0
        return BATTERY_VOLTAGE[i]

    def is_usb_connected(self):
        if supervisor.runtime.usb_connected:
            return 1
        else:
            return 0
