import usb_hid

# fmt:off
report_descriptor = bytes(
    (
        0x05, 0x01,        # Usage Page (Generic Desktop Ctrls)
        0x09, 0x08,        # Usage (Multi-axis Controller)
        0xA1, 0x01,        # Collection (Application)
        0xA1, 0x00,        #   Collection (Physical)
        0x85, 0x04,        #     Report ID (4)
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
        0xC0,              # End Collection
    )
)
# fmt:on


SIX_AXIS = usb_hid.Device(
    report_descriptor=report_descriptor,
    usage_page=0x01,
    usage=0x08,
    report_ids=(0x04,),
    in_report_lengths=(12,),
    out_report_lengths=(0,),
)
