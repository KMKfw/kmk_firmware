# Split Keyboards
Split keyboards are mostly the same as unsplit. Wired UART and Bluetooth are supported.


## Wired UART
Wired connections can use UART over 1 or 2 wires. With 2 wires, you will be able to syncronize the halves allowing additional features in some extentions.
```python
import board
from kmk.extensions.split import Split

uart_pin = board.SOMETHING
split = Split(uart_pin=uart_pin)
keyboard.extensions.append(split)
```

### Config
Useful config options:
```python
    split = Split(
        is_target=True,  # If this is the side connecting to the computer
        extra_data_pin=None,  # Second uart pin to allow 2 way communication
        split_offset=None,  # Default is column pins but allows an override
        split_flip=True,  # If both halves are the same, but flipped, set this True
        split_side=None,  # Sets if this is the left or right
        split_type=SplitType.UART,  # Defaults to UART
        target_left=True,  # Assumes that left will be the one on USB. Set to folse if it will be the right
        uart_flip=True,  # Reverses the RX and TX pins if both are provided
        uart_pin=None,  # The primary uart pin to talk to the secondary device with
        uart_timeout=20,  # Rarely needed to change, but is avaliable
    )

```

## Bluetooth split (aka no TRRS)
Wireless splits are fully featured with 2 way communication allowing all extentions to work 100%.
```python
split_side = 'Left'
split_side = 'Right'
split = BLE_Split(split_side=split_side)

keyboard.extensions.append(split)
```

### Config
Useful config options:
```python
    split = BLE_Split(
        split_side=split_side,  # See EE hands below
        uart_interval=30,  # Sets the uarts delay. Lower numbers draw more power
        hid_type=HIDModes.BLE,  # If using USB to connect to a computer, change this appropriately.
    )

```

### EE HANDS
If you want to plug USB in on either side, or are using bluetooth, this is for you. Pick one of the 2 options but not both.

## Renaming CIRCUITPY Drive
The easiest way is to rename your CIRCUITPY drive to something. The left side must end in L, the right must in in R. 
The name must be 11 characters or less! This is a limitation of the filesystem. You will receive an error if you choose a 
name longer than 11 characters. Instructions on how to do that are [here](https://learn.adafruit.com/welcome-to-circuitpython/the-circuitpy-drive). 
For example on NYQUISTL for left and NYQUISTR for the right. 

For wired connections you are done. For bluetooth, remove the `split_side` like tihs
```python
split = BLE_Split()

keyboard.extensions.append(split)
```


## Adding an extra file
If you have changed the name of the drive as stated above, do not follow this section.  
On each half of your keyboard make a file called kmk_side.py and add one of these lines to the file
depending on where each piece is physically located.
```python
split_side = "Left"
OR
split_side = "Right"
```

and then in your keymap, add the line
```python
from kmk_side import split_side
```

