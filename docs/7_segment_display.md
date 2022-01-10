# 7 segment display using HT16K33
want another way to display your current layer? At this time is is only avaible using custom hardware but if you want to add it to your board the code is done.

## Circuitpython
this does require the HT16K33 an bus_device library from Adafruit. 
This can be downloaded 
[HT16K33 here](https://github.com/adafruit/Adafruit_CircuitPython_HT16K33).
[bus_device here](https://github.com/adafruit/Adafruit_CircuitPython_BusDevice).
They are a part of the [Adafruit CircuitPython Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle).
Simply put this in "root/lib" of your circuitpython device. If unsure, root the folder with main.py in it, and should be the first folder you see when you open the device. Then make a folder named lib put it in there.

## Enabling the extension
The only required values that you need to give the 7 segment extension are the SCL and SDA pins.
```python
from board import SCL, SDA
from kmk.extensions.segment_display import Segment
keyboard.extensions.append(Segment(SDA,SCL))
```