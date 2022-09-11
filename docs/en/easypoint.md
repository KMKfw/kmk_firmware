# AS5013 (aka 'EasyPoint')

Module handles the AM5013 Two-dimensional magnetic position sensor with digital coordinates output

Product page: https://www.mouser.dk/ProductDetail/ams/AS5013-IQFT?qs=abmNkq9no6D3ApA%252BrWSMNQ%3D%3D

### Usage

Declare I2C bus and add this module in your main class.

```python
from kmk.modules.easypoint import Easypoint
import busio

i2c = busio.I2C(scl=board.GP1, sda=board.GP0)

easypoint = Easypoint(i2c, address=0x40)
keyboard.modules.append(easypoint)
```

Further configuring the AS5013 involved x/y-offset, and deadzone.

```python
easypoint = Easypoint(i2c, address=0x40, y_offset=Y_OFFSET, x_offset=X_OFFSET, dead_x=DEAD_X, dead_y=DEAD_Y)
```
