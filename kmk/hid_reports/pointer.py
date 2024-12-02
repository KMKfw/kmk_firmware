import usb_hid

# fmt:off
report_descriptor = bytes(
    (
        0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
        0x09, 0x02,  # Usage (Mouse)
        0xA1, 0x01,  # Collection (Application)
        0x09, 0x01,  #   Usage (Pointer)
        0xA1, 0x00,  #   Collection (Physical)
        0x85, 0x02,  #     10, 11 Report ID (2)
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
        0x09, 0x38,  #     Usage (Wheel)
        0x05, 0x0C,  #     Usage Page (Consumer Devices) 0x0A,
        0x38, 0x02,  #     Usage (AC Pan)
        0x15, 0x81,  #     Logical Minimum (-127)
        0x25, 0x7F,  #     Logical Maximum (127)
        0x95, 0x04,  #     Report Count (4)
        0x75, 0x08,  #     Report Size (8)
        0x81, 0x06,  #     Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
        0xC0,        #   End Collection
        0xC0,        # End Collection
    )
)
# fmt:on


POINTER = usb_hid.Device(
    report_descriptor=report_descriptor,
    usage_page=0x01,
    usage=0x02,
    report_ids=(0x02,),
    in_report_lengths=(5,),
    out_report_lengths=(0,),
)
