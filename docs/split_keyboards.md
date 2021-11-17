# Split Keyboards
Split keyboards are mostly the same as unsplit. Wired UART is fully supported,
and testing of bluetooth splits, though we don't currently offer support for this.

Notice that this Split module must be added after the ModTap module to the keyboard.modules.

## Wired UART
Wired connections can use UART over 1 or 2 wires. With 2 wires, you will be able
to syncronize the halves allowing additional features in some extensions.
```python
from kb import data_pin
:from kmk.modules.split import Split, SplitType

split = Split(split_side=SplitSide.LEFT)
keyboard.modules.append(split)
```

## Bluetooth split (aka no TRRS) [Currently in testing]
Wireless splits are fully featured with 2 way communication allowing all extensions to work 100%.
```python
from kb import data_pin
from kmk.modules.split import Split, SplitType, Split_Side


split = Split(split_type=Split.BLE, split_side=SplitSide.LEFT)
OR
split = Split(split_type=Split.BLE, split_side=SplitSide.LEFT)
keyboard.modules.append(split)
```

### Config
Useful config options:
```python
split = Split(
    split_flip=True,  # If both halves are the same, but flipped, set this True
    split_side=None,  # Sets if this is to SplitSide.LEFT or SplitSide.RIGHT, or use EE hands
    split_type=SplitType.UART,  # Defaults to UART
    split_target_left=True,  # If you want the right to be the target, change this to false
    uart_interval=20,  # Sets the uarts delay. Lower numbers draw more power
    data_pin=None,  # The primary data pin to talk to the secondary device with
    data_pin2=None,  # Second uart pin to allow 2 way communication
    target_left=True,  # Assumes that left will be the one on USB. Set to folse if it will be the right
    uart_flip=True,  # Reverses the RX and TX pins if both are provided
)

```

### EE HANDS
If you want to plug USB in on either side, or are using bluetooth, this is for 
you.

Rename your CIRCUITPY drive to something different. The left side must 
end in L, the right must is in R. The name must be 11 characters or less! This is 
a limitation of the filesystem. You will receive an error if you choose a name 
longer than 11 characters. Instructions on how to do that are 
[here](https://learn.adafruit.com/welcome-to-circuitpython/the-circuitpy-drive).
For example on NYQUISTL for left and NYQUISTR for the right. 

For wired connections you don't need to pass anything. For bluetooth, remove the `split_side` like this
```python
# Wired
split = Split()
# Wireless
split = Split(split_type=Split.BLE)
```
