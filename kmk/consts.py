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


HID_REPORT_STRUCTURE = bytes([
    # Regular keyboard
    0x05, HIDUsagePage.KEYBOARD,  # Usage Page (Generic Desktop)
    0x09, HIDUsage.KEYBOARD,  # Usage (Keyboard)
    0xA1, 0x01,  # Collection (Application)
    0x85, HIDReportTypes.KEYBOARD,  #   Report ID (1)
    0x05, 0x07,  #   Usage Page (Keyboard)
    0x19, 224,   #   Usage Minimum (224)
    0x29, 231,   #   Usage Maximum (231)
    0x15, 0x00,  #   Logical Minimum (0)
    0x25, 0x01,  #   Logical Maximum (1)
    0x75, 0x01,  #   Report Size (1)
    0x95, 0x08,  #   Report Count (8)
    0x81, 0x02,  #   Input (Data, Variable, Absolute)
    0x81, 0x01,  #   Input (Constant)
    0x19, 0x00,  #   Usage Minimum (0)
    0x29, 101,   #   Usage Maximum (101)
    0x15, 0x00,  #   Logical Minimum (0)
    0x25, 101,   #   Logical Maximum (101)
    0x75, 0x08,  #   Report Size (8)
    0x95, 0x06,  #   Report Count (6)
    0x81, 0x00,  #   Input (Data, Array)
    0x05, 0x08,  #   Usage Page (LED)
    0x19, 0x01,  #   Usage Minimum (1)
    0x29, 0x05,  #   Usage Maximum (5)
    0x15, 0x00,  #   Logical Minimum (0)
    0x25, 0x01,  #   Logical Maximum (1)
    0x75, 0x01,  #   Report Size (1)
    0x95, 0x05,  #   Report Count (5)
    0x91, 0x02,  #   Output (Data, Variable, Absolute)
    0x95, 0x03,  #   Report Count (3)
    0x91, 0x01,  #   Output (Constant)
    0xC0,        # End Collection
    # Regular mouse
    0x05, HIDUsagePage.MOUSE,  # Usage Page (Generic Desktop)
    0x09, HIDUsage.MOUSE,  # Usage (Mouse)
    0xA1, 0x01,  # Collection (Application)
    0x09, 0x01,  #   Usage (Pointer)
    0xA1, 0x00,  #   Collection (Physical)
    0x85, HIDReportTypes.MOUSE,  # Report ID (n)
    0x05, 0x09,  #     Usage Page (Button)
    0x19, 0x01,  #     Usage Minimum (0x01)
    0x29, 0x05,  #     Usage Maximum (0x05)
    0x15, 0x00,  #     Logical Minimum (0)
    0x25, 0x01,  #     Logical Maximum (1)
    0x95, 0x05,  #     Report Count (5)
    0x75, 0x01,  #     Report Size (1)
    0x81, 0x02,  #     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x95, 0x01,  #     Report Count (1)
    0x75, 0x03,  #     Report Size (3)
    0x81, 0x01,  #     Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x05, 0x01,  #     Usage Page (Generic Desktop Ctrls)
    0x09, 0x30,  #     Usage (X)
    0x09, 0x31,  #     Usage (Y)
    0x15, 0x81,  #     Logical Minimum (-127)
    0x25, 0x7F,  #     Logical Maximum (127)
    0x75, 0x08,  #     Report Size (8)
    0x95, 0x02,  #     Report Count (2)
    0x81, 0x06,  #     Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
    0x09, 0x38,  #     Usage (Wheel)
    0x15, 0x81,  #     Logical Minimum (-127)
    0x25, 0x7F,  #     Logical Maximum (127)
    0x75, 0x08,  #     Report Size (8)
    0x95, 0x01,  #     Report Count (1)
    0x81, 0x06,  #     Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,        #   End Collection
    0xC0,        # End Collection
    # Consumer ("multimedia") keys
    0x05, HIDUsagePage.CONSUMER,  # Usage Page (Consumer)
    0x09, HIDUsage.CONSUMER,  # Usage (Consumer Control)
    0xA1, 0x01,        # Collection (Application)
    0x85, HIDReportTypes.CONSUMER,  # Report ID (n)
    0x75, 0x10,        #   Report Size (16)
    0x95, 0x01,        #   Report Count (1)
    0x15, 0x01,        #   Logical Minimum (1)
    0x26, 0x8C, 0x02,  #   Logical Maximum (652)
    0x19, 0x01,        #   Usage Minimum (Consumer Control)
    0x2A, 0x8C, 0x02,  #   Usage Maximum (AC Send)
    0x81, 0x00,        #   Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,              # End Collection
    # Power controls
    0x05, HIDUsagePage.SYSCONTROL,  # Usage Page (Generic Desktop Ctrls)
    0x09, HIDUsage.SYSCONTROL,  # Usage (Sys Control)
    0xA1, 0x01,        # Collection (Application)
    0x85, HIDReportTypes.SYSCONTROL,  # Report ID (n)
    0x75, 0x02,        #   Report Size (2)
    0x95, 0x01,        #   Report Count (1)
    0x15, 0x01,        #   Logical Minimum (1)
    0x25, 0x03,        #   Logical Maximum (3)
    0x09, 0x82,        #   Usage (Sys Sleep)
    0x09, 0x81,        #   Usage (Sys Power Down)
    0x09, 0x83,        #   Usage (Sys Wake Up)
    0x81, 0x60,        #   Input (Data,Array,Abs,No Wrap,Linear,No Preferred State,Null State)
    0x75, 0x06,        #   Report Size (6)
    0x81, 0x03,        #   Input (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,              # End Collection
])


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
