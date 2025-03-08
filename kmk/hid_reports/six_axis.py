import usb_hid

# fmt:off
report_descriptor = bytes(
    (
        0x05, 0x01,        # Usage Page (Generic Desktop Ctrls)
        0x09, 0x08,        # Usage (Multi-axis Controller)
        0xA1, 0x01,        # Collection (Application)
        0xA1, 0x00,        #   Collection (Physical)
        0x85, 0x01,        #     Report ID (1)
        0x16, 0x0C, 0xFE,  #     Logical Minimum (-500)
        0x26, 0xF4, 0x01,  #     Logical Maximum (500)
        0x36, 0x00, 0x80,  #     Physical Minimum (-32768)
        0x46, 0xFF, 0x7F,  #     Physical Maximum (32767)
        0x55, 0x0C,        #     Unit Exponent (-4)
        0x65, 0x11,        #     Unit (System: SI Linear, Length: Centimeter)
        0x09, 0x30,        #     Usage (X)
        0x09, 0x31,        #     Usage (Y)
        0x09, 0x32,        #     Usage (Z)
        0x09, 0x33,        #     Usage (Rx)
        0x09, 0x34,        #     Usage (Ry)
        0x09, 0x35,        #     Usage (Rz)
        0x75, 0x10,        #     Report Size (16)
        0x95, 0x06,        #     Report Count (6)
        0x81, 0x02,        #     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0xC0,              #   End Collection

        0xA1, 0x00,        #   Collection (Physical)
        0x85, 0x03,        #     Report ID (3)
        0x05, 0x09,        #     Usage Page (Button)
        0x19, 0x01,        #     Usage Minimum (1)
        0x29, 0x02,        #     Usage Maximum (2)
        0x15, 0x00,        #     Logical Minimum (0)
        0x25, 0x01,        #     Logical Maximum (1)
        0x35, 0x00,        #     Physical Minimum (0)
        0x45, 0x01,        #     Physical Maximum (1)
        0x75, 0x01,        #     Report Size (1)
        0x95, 0x02,        #     Report Count (2)
        0x81, 0x02,        #     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0x95, 0x0E,        #     Report Count (14)
        0x81, 0x03,        #     Input (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0xC0,              #   End Collection

        0xA1, 0x02,        #   Collection (Logical)
        0x85, 0x04,        #     Report ID (4)
        0x05, 0x08,        #     Usage Page (LEDs)
        0x09, 0x4B,        #     Usage (Generic Indicator)
        0x15, 0x00,        #     Logical Minimum (0)
        0x25, 0x01,        #     Logical Maximum (1)
        0x95, 0x01,        #     Report Count (1)
        0x75, 0x01,        #     Report Size (1)
        0x91, 0x02,        #     Output (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
        0x95, 0x01,        #     Report Count (1)
        0x75, 0x07,        #     Report Size (7)
        0x91, 0x03,        #     Output (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
        0xC0,              #   End Collection
        0xC0,              # End Collection
    )
)
# fmt:on

SIX_AXIS = usb_hid.Device(
    report_descriptor=report_descriptor,
    usage_page=0x01,
    usage=0x08,
    report_ids=(
        0x01,
        0x03,
        0x04,
    ),
    in_report_lengths=(
        12,
        2,
        0,
    ),
    out_report_lengths=(
        0,
        0,
        1,
    ),
)


# Keyboard descriptors using Report ID 5

# fmt:off
report_descriptor = bytes(
    (
        0x05, 0x01,        # Usage Page (Generic Desktop Ctrls)
        0x09, 0x06,        # Usage (Keyboard)
        0xA1, 0x01,        # Collection (Application)
        0x85, 0x05,        #   Report ID (5)

        0x05, 0x07,        #   Usage Page (Kbrd/Keypad)
        0x19, 0xE0,        #   Usage Minimum (224)
        0x29, 0xE7,        #   Usage Maximum (231)
        0x15, 0x00,        #   Logical Minimum (0)
        0x25, 0x01,        #   Logical Maximum (1)
        0x75, 0x01,        #   Report Size (1)
        0x95, 0x08,        #   Report Count (8)
        0x81, 0x02,        #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0x95, 0x01,        #   Report Count (1)
        0x75, 0x08,        #   Report Size (8)
        0x81, 0x01,        #   Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0x95, 0x05,        #   Report Count (5)
        0x75, 0x01,        #   Report Size (1)

        0x05, 0x08,        #   Usage Page (LEDs)
        0x19, 0x01,        #   Usage Minimum (Num Lock)
        0x29, 0x05,        #   Usage Maximum (Kana)
        0x91, 0x02,        #   Output (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
        0x95, 0x01,        #   Report Count (1)
        0x75, 0x03,        #   Report Size (3)
        0x91, 0x01,        #   Output (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
        0x95, 0x06,        #   Report Count (6)
        0x75, 0x08,        #   Report Size (8)
        0x15, 0x00,        #   Logical Minimum (0)
        0x26, 0xFF, 0x00,  #   Logical Maximum (255)

        0x05, 0x07,        #   Usage Page (Kbrd/Keypad)
        0x19, 0x00,        #   Usage Minimum (0)
        0x2A, 0xFF, 0x00,  #   Usage Maximum (255)
        0x81, 0x00,        #   Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0xC0,              # End Collection
    )
)
# fmt:on

KEYBOARD = usb_hid.Device(
    report_descriptor=report_descriptor,
    usage_page=0x01,
    usage=0x06,
    report_ids=(0x05,),
    in_report_lengths=(8,),
    out_report_lengths=(1,),
)


# fmt:off
report_descriptor = bytes(
    (
        0x05, 0x01,        # Usage Page (Generic Desktop Ctrls),
        0x09, 0x06,        # Usage (Keyboard),
        0xA1, 0x01,        # Collection (Application),
        0x85, 0x05,        #   Report ID (5)
        # Modifiers
        0x05, 0x07,        #   Usage Page (Key Codes),
        0x19, 0xE0,        #   Usage Minimum (224),
        0x29, 0xE7,        #   Usage Maximum (231),
        0x15, 0x00,        #   Logical Minimum (0),
        0x25, 0x01,        #   Logical Maximum (1),
        0x75, 0x01,        #   Report Size (1),
        0x95, 0x08,        #   Report Count (8),
        0x81, 0x02,        #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        # LEDs
        0x05, 0x08,        #   Usage Page (LEDs),
        0x19, 0x01,        #   Usage Minimum (1),
        0x29, 0x05,        #   Usage Maximum (5),
        0x95, 0x05,        #   Report Count (5),
        0x75, 0x01,        #   Report Size (1),
        0x91, 0x02,        #   Output (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non- olatile)
        0x95, 0x01,        #   Report Count (1),
        0x75, 0x03,        #   Report Size (3),
        0x91, 0x01,        #   Output (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position,N n-volatile)
        # Keys
        0x05, 0x07,        #   Usage Page (Kbrd/Keypad),
        0x19, 0x00,        #   Usage Minimum (0),
        0x29, 0x77,        #   Usage Maximum (119),
        0x15, 0x00,        #   Logical Minimum (0),
        0x25, 0x01,        #   Logical Maximum(1),
        0x95, 0x78,        #   Report Count (120),
        0x75, 0x01,        #   Report Size (1),
        0x81, 0x02,        #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0xC0,              # End Collection
    )
)
# fmt:on

NKRO_KEYBOARD = usb_hid.Device(
    report_descriptor=report_descriptor,
    usage_page=0x01,
    usage=0x06,
    report_ids=(0x05,),
    in_report_lengths=(16,),
    out_report_lengths=(1,),
)


# Mouse descriptors using Report ID 6

# fmt:off
report_descriptor = bytes(
    (
        0x05, 0x01,        # Usage Page (Generic Desktop Ctrls)
        0x09, 0x02,        # Usage (Mouse)
        0xA1, 0x01,        # Collection (Application)
        0x09, 0x01,        #   Usage (Pointer)
        0xA1, 0x00,        #   Collection (Physical)
        0x85, 0x06,        #     Report ID (6)

        0x05, 0x09,        #     Usage Page (Button)
        0x19, 0x01,        #     Usage Minimum (1)
        0x29, 0x05,        #     Usage Maximum (5)
        0x15, 0x00,        #     Logical Minimum (0)
        0x25, 0x01,        #     Logical Maximum (1)
        0x95, 0x05,        #     Report Count (5)
        0x75, 0x01,        #     Report Size (1)
        0x81, 0x02,        #     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0x95, 0x01,        #     Report Count (1)
        0x75, 0x03,        #     Report Size (3)
        0x81, 0x01,        #     Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)

        0x05, 0x01,        #     Usage Page (Generic Desktop Ctrls)
        0x09, 0x30,        #     Usage (X)
        0x09, 0x31,        #     Usage (Y)
        0x09, 0x38,        #     Usage (Wheel)
        0x15, 0x81,        #     Logical Minimum (-127)
        0x25, 0x7F,        #     Logical Maximum (127)
        0x95, 0x03,        #     Report Count (3)
        0x75, 0x08,        #     Report Size (8)
        0x81, 0x06,        #     Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
        0xC0,              #   End Collection
        0xC0,              # End Collection
    )
)
# fmt:on


MOUSE = usb_hid.Device(
    report_descriptor=report_descriptor,
    usage_page=0x01,
    usage=0x02,
    report_ids=(0x06,),
    in_report_lengths=(4,),
    out_report_lengths=(0,),
)


# fmt:off
report_descriptor = bytes(
    (
        0x05, 0x01,        # Usage Page (Generic Desktop Ctrls)
        0x09, 0x02,        # Usage (Mouse)
        0xA1, 0x01,        # Collection (Application)
        0x09, 0x01,        #   Usage (Pointer)
        0xA1, 0x00,        #   Collection (Physical)
        0x85, 0x06,        #     Report ID (6)

        0x05, 0x09,        #     Usage Page (Button)
        0x19, 0x01,        #     Usage Minimum (1)
        0x29, 0x05,        #     Usage Maximum (5)
        0x15, 0x00,        #     Logical Minimum (0)
        0x25, 0x01,        #     Logical Maximum (1)
        0x95, 0x05,        #     Report Count (5)
        0x75, 0x01,        #     Report Size (1)
        0x81, 0x02,        #     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0x95, 0x01,        #     Report Count (1)
        0x75, 0x03,        #     Report Size (3)
        0x81, 0x01,        #     Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)

        0x05, 0x01,        #     Usage Page (Generic Desktop Ctrls)
        0x09, 0x30,        #     Usage (X)
        0x09, 0x31,        #     Usage (Y)
        0x09, 0x38,        #     Usage (Wheel)
        0x15, 0x81,        #     Logical Minimum (-127)
        0x25, 0x7F,        #     Logical Maximum (127)
        0x95, 0x03,        #     Report Count (3)
        0x75, 0x08,        #     Report Size (8)
        0x81, 0x06,        #     Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)

        0x05, 0x0C,        #     Usage Page (Consumer Devices)
        0x0A, 0x38, 0x02,  #     Usage (AC Pan)
        0x15, 0x81,        #     Logical Minimum (-127)
        0x25, 0x7F,        #     Logical Maximum (127)
        0x95, 0x01,        #     Report Count (1)
        0x75, 0x08,        #     Report Size (8)
        0x81, 0x06,        #     Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
        0xC0,              #   End Collection
        0xC0,              # End Collection
    )
)
# fmt:on


POINTER = usb_hid.Device(
    report_descriptor=report_descriptor,
    usage_page=0x01,
    usage=0x02,
    report_ids=(0x06,),
    in_report_lengths=(5,),
    out_report_lengths=(0,),
)


# Consumer Control descriptor using Report ID 7

# fmt:off
report_descriptor = bytes(
    (
        0x05, 0x0C,        # Usage Page (Consumer)
        0x09, 0x01,        # Usage (Consumer Control)
        0xA1, 0x01,        # Collection (Application)
        0x85, 0x07,        #   Report ID (7)
        0x75, 0x10,        #   Report Size (16)
        0x95, 0x01,        #   Report Count (1)
        0x15, 0x01,        #   Logical Minimum (1)
        0x26, 0x8C, 0x02,  #   Logical Maximum (652)
        0x19, 0x01,        #   Usage Minimum (Consumer Control)
        0x2A, 0x8C, 0x02,  #   Usage Maximum (AC Send)
        0x81, 0x00,        #   Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0xC0,              # End Collection
    )
)
# fmt:on


CONSUMER_CONTROL = usb_hid.Device(
    report_descriptor=report_descriptor,
    usage_page=0x0C,
    usage=0x01,
    report_ids=(0x07,),
    in_report_lengths=(2,),
    out_report_lengths=(0,),
)
