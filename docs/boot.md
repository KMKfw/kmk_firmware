## There is a more detailed explanation in the [circuit python docs](https://docs.circuitpython.org/en/latest/README.html), however there are some common use cases for your keyboard listed here

### You can hide your device from showing up as a usb storage

```python
storage.disable_usb_drive()
```

### Make your keyboard work in bios

```python
usb_hid.enable(boot_device=1)
```

### Disable serial comms

```python
# Equivalent to usb_cdc.enable(console=False, data=False)
usb_cdc.disable()
```

### A fully working example, with a

```python
import supervisor
import board
import digitalio
import storage
import usb_cdc
import usb_hid

supervisor.set_next_stack_limit(4096 + 4096)

# If this key is held during boot, don't run the code which hides the storage and disables serial
col = digitalio.DigitalInOut(board.GP2)
row = digitalio.DigitalInOut(board.GP13)
col.switch_to_output(value=True)
row.switch_to_input(pull=digitalio.Pull.DOWN)

if not row.value:
    storage.disable_usb_drive()
    # Equivalent to usb_cdc.enable(console=False, data=False)
    usb_cdc.disable()
    usb_hid.enable(boot_device=1)

row.deinit()
col.deinit()
```
