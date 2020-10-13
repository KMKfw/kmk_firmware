# Split Keyboards
Split keyboards are mostly the same as unsplit and very easy to adapt a keymap for. Currently
UART is supported, though other modes will come later such as Bluetooth and i2c.


## UART
To enable uart it's as simple as adding this line, of course changing the pin
```python
keyboard.split_type = "UART"
keyboard.uart_pin = board.SCL
```

## Config
Useful config options:
```python
keyboard.split_flip = True  # If your boards are identical but one is flipped, this option is for you 
keyboard.split_offsets = [6, 6, 6, 6]  # This is the how many keys are on each column on the "target" half
```

### EE HANDS
If you want to plug in on either side, it can be done fairly easily but requires setup. 

On each half of your keyboard make a file called kmk_side.py and add one of these lines to the file
depending on where each piece is physically located.
```python
split_target = "Left"
OR
split_target = "Right"
```

and then in your keymap, add the line
```python
from kmk_side import split_target
```

