# Code thanks to https://github.com/JanLunge
import digitalio
import usb_hid

import storage
import usb_cdc

from kmk.quickpin.pro_micro.helios import pinout as pins

# If this key is held during boot, don't run the code which hides the storage and disables serial
col = digitalio.DigitalInOut(pins[18])
row = digitalio.DigitalInOut(pins[1])

col.switch_to_output(value=True)
row.switch_to_input(pull=digitalio.Pull.DOWN)

if not row.value:
    storage.disable_usb_drive()
    # Equivalent to usb_cdc.enable(console=False, data=False)
    usb_cdc.disable()
    usb_hid.enable(boot_device=1)

row.deinit()
col.deinit()
