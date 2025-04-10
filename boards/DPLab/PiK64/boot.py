import board
import digitalio
import storage

from kmk.bootcfg import bootcfg

noStorage = False
noStoragePin = digitalio.DigitalInOut(board.GP23)
noStoragePin.direction = digitalio.Direction.INPUT
noStoragePin.pull = digitalio.Pull.UP
noStorage = noStoragePin.value

if(noStorage == True):
    print("USB drive  enabled")
else:
    bootcfg(
        midi=False,
        mouse=False,
        storage=False,
        usb_id={'manufacturer': 'DPLab', 'product': 'PiK64 - Commodore 64 Keyboard'},
    )
    storage.disable_usb_drive()
    print("USB drive disable")