import usb_hid

# fmt:off
report_descriptor = bytes(
    (
        0x05, 0x01,  # Usage Page (Generic Desktop Ctrls),
        0x09, 0x06,  # Usage (Keyboard),
        0xA1, 0x01,  # Collection (Application),
        0x85, 0x01,  #   Report ID (1)
        # modifiers
        0x05, 0x07,  #   Usage Page (Key Codes),
        0x19, 0xE0,  #   Usage Minimum (224),
        0x29, 0xE7,  #   Usage Maximum (231),
        0x15, 0x00,  #   Logical Minimum (0),
        0x25, 0x01,  #   Logical Maximum (1),
        0x75, 0x01,  #   Report Size (1),
        0x95, 0x08,  #   Report Count (8),
        0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        # LEDs
        0x05, 0x08,  #   Usage Page (LEDs),
        0x19, 0x01,  #   Usage Minimum (1),
        0x29, 0x05,  #   Usage Maximum (5),
        0x95, 0x05,  #   Report Count (5),
        0x75, 0x01,  #   Report Size (1),
        0x91, 0x02,  #   Output (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non- olatile)
        0x95, 0x01,  #   Report Count (1),
        0x75, 0x03,  #   Report Size (3),
        0x91, 0x01,  #   Output (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position,N n-volatile)
        # keys
        0x05, 0x07,  #   Usage Page (Kbrd/Keypad),
        0x19, 0x00,  #   Usage Minimum (0),
        0x29, 0x77,  #   Usage Maximum (119),
        0x15, 0x00,  #   Logical Minimum (0),
        0x25, 0x01,  #   Logical Maximum(1),
        0x95, 0x78,  #   Report Count (120),
        0x75, 0x01,  #   Report Size (1),
        0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0xC0,        # End Collection
    )
)
# fmt:on

NKRO_KEYBOARD = usb_hid.Device(
    report_descriptor=report_descriptor,
    usage_page=0x01,
    usage=0x06,
    report_ids=(0x01,),
    in_report_lengths=(16,),
    out_report_lengths=(1,),
)
