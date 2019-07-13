CIRCUITPYTHON = 'CircuitPython'
MICROPYTHON = 'MicroPython'


class HIDReportTypes:
    KEYBOARD = 1
    MOUSE = 2
    CONSUMER = 3
    SYSCONTROL = 4


class HIDUsage:
    KEYBOARD = 0x06
    MOUSE = 0x02
    CONSUMER = 0x01
    SYSCONTROL = 0x80


class HIDUsagePage:
    CONSUMER = 0x0C
    KEYBOARD = MOUSE = SYSCONTROL = 0x01


# Currently only used by the CircuitPython HIDHelper because CircuitPython
# actually enforces these limits with a ValueError. Unused on PyBoard because
# we can happily send full reports there and it magically works.
HID_REPORT_SIZES = {
    HIDReportTypes.KEYBOARD: 8,
    HIDReportTypes.MOUSE: 4,
    HIDReportTypes.CONSUMER: 2,
    HIDReportTypes.SYSCONTROL: 8,  # TODO find the correct value for this
}


class DiodeOrientation:
    '''
    Orientation of diodes on handwired boards. You can think of:
    COLUMNS = vertical
    ROWS = horizontal
    '''

    COLUMNS = 0
    ROWS = 1


class UnicodeMode:
    NOOP = 0
    LINUX = IBUS = 1
    MACOS = OSX = RALT = 2
    WINC = 3


class LeaderMode:
    TIMEOUT = 0
    TIMEOUT_ACTIVE = 1
    ENTER = 2
    ENTER_ACTIVE = 3
