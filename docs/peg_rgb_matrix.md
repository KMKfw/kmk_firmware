# Peg Rgb Matrix
 To use this you need to make some changes to your kb.py as well as you main.py I will break it into two sections for you. 

### What you can and cant do with this extension.

#### Can do
* Set any key to be any color in a syntax that is very similar to your keymap
* Set some keys/leds to be off
* Have your underglow leds be a different color then your keys
* Set mods to be a different color to your alphas
* Work on split keyboards


#### Cant do yet / on the way
* Adjust color on the fly
* Animate 
* Alow led color to change with layer

### Key codes
Because you cant do any adjustments at run time there is only one keycode KC.RGB_TOG, this just toggles your leds on and off.

## Required Libs
You need these frozen into your circuitpython or in a "lib" folder at the root of your drive.
* [Adafruit_CircuitPython_NeoPixel](https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel)
* [Download .mpy versions from here](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20220415/adafruit-circuitpython-bundle-7.x-mpy-20220415.zip)


## kb.py
Your chosen board may already have these changes done If not you will need to add them.

The keyboard needs 3 fields 
* Led key position `led_key_pos` 
    * This is much like your "coord_mapping" you are telling the extension what led to light up when you want to light up "WASD" for example.
* Brightness limit `brightness_limit`
    * This will limit your brightness and may be required to get stable performance depending on how many leds you have on your keyboard.
* Number of leds `num_pixels`
    * This is used to do some math for laying out the leds on the right keys, simply just your number of leds.

In the example below I have layed out a 58 key split keyboard. We have 70 leds on this keyboard and 58 keys so that is going to leave us with 12 underglow leds.
In your `led_key_pos` will start on your top left key and work along the row and start over on the next row. Each number should be that leds index, so if the first led that is connected to your controller is under your ESC key then your first number would be 0. In the below example we start with 11 because we have 12 underglow leds connected before this one. We continue on to the split to the second side where we reverse it and add 35 in this case (70/2). This repeats for each row until we finish the thumb cluster our final row. Then we get into our underglow leds, underglow pos always goes at the end of the keys.

Split Example:
```python
    led_key_pos =[
        11,10,9 ,8 ,7 ,6 ,       41,42,43,44,45,46,
        12,13,14,15,16,17,       52,51,50,49,48,47,
        23,22,21,20,19,18,       53,54,55,56,57,58,
        24,25,26,27,28,29,30, 65,64,63,62,61,60,59,
                 34,33,32,31, 66,67,68,69,
                 3 ,4 ,5 ,       40,39,38,
                 2 ,1 ,0 ,       35,36,37
                 ]
    brightness_limit = 1.0
    num_pixels = 70

```
Below you will find a more simple non-split example again we have 10 underglow leds that are connected before any of the perkey leds so our fist number is 10. We continue on until 47 then go into the underglow leds.

Non-split Example:
```python
    led_key_pos=[
        10,11,12,13,14,15,16,17,18,19,
        20,21,22,23,24,25,26,27,28,29,
        30,31,32,33,34,35,36,37,38,39,
           40,41,42,43,44,45,46,47,
                 5, 6, 7, 8, 9,
                 0, 1, 2, 3, 4
        ]
    brightness_limit = 1.0
    num_pixels = 48
```

## Main.py
These are the changes that need to be made / added to your main.py
```python
from kmk.extensions.peg_rgb_matrix import Rgb_matrix,Rgb_matrix_data,Color
# ... Other code
rgb_ext = Rgb_matrix(...per key color data)
keyboard.extensions.append(rgb_ext)
```
Rgb_matrix is our extension and it takes at least one argument and that is your `Rgb_matrix_data`, lets go over everything you can pass into this now.

* Led display `ledDisplay`
    * This is our primary and only required field This takes a `Rgb_matrix_data` class.
        * Rgb matrix data Only takes two fields 
            * Keys array of colors with a length equal to the number of keys on your keyboard
            * Underglow array of colors with a length equal to the number of underglow leds on your keyboard
* Split `split`
    * This is optional only to be used if the keyboard is split takes a boolean.
* Right side `rightSide`
    * This is optional only to be used if the keyboard is split and this config is happening on the right side (the off side) takes a boolean.
* RGB order `rgb_order`
    * This is optional and only needs to be set if you are not using a WS2812 based led.
* Disable auto write `disable_auto_write`
    * This is optional and only serves to make all your leds turn on at once instead of a little animation.

### Colors 
Colors are RGB and can be provided in one of two ways. You can pass an array of three number 0-255 or you can use the `Color` class with its default colors see Example below.
```python
Rgb_matrix_data(
    keys=[[255,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],"""... rest of colors""" ],                     
    underglow=[[0,0,55],[0,0,55],"""... rest of colors""" ]
             )
``` 
```python
Rgb_matrix_data(
    keys=[Color.RED, Color.GREEN, Color.BLUE, Color.WHITE, Color.YELLOW, Color.ORANGE,"""... rest of colors""" ],                     
    underglow=[Color.PURPLE, Color.TEAL, Color.PINK, Color.OFF,"""... rest of colors""" ]
             )
``` 

### Full examples

```python
rgb_ext = Rgb_matrix(ledDisplay=Rgb_matrix_data(
    keys=[
    [255,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],                        [55,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],[255,55,55],
    [255,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],                        [55,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],[255,55,55],
    [255,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],                        [55,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],[255,55,55],
    [255,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],[255,55,55],[255,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],[255,55,55],
                                     [255,55,55],[55,55,55],[55,55,55],[255,55,55],[255,55,55],[55,55,55],[55,55,55],[255,55,55]],
                                    
    underglow=[ 
             [0,0,55],[0,0,55],[0,0,55],[0,0,55],[0,0,55],[0,0,55],[0,0,55],[0,0,55],[0,0,55],[0,0,55],[0,0,55],[0,0,55]]
             ),
    split=True,
    rightSide=True,
    disable_auto_write=True)
```

### Bonus
Because it can be time consuming to create these maps and quick to edit there is a utility you can use that will generate it for you.
```python
Rgb_matrix_data.generate_led_map(58,10,Color.WHITE,Color.BLUE)
```
Call `Rgb_matrix_data.generate_led_map` before you do any config beyond imports and it will print this out to your circuit python REPL witch you can view by using a tool like "screen" or "PUTTY" to view the output (see link below).

Generate led map arguments:
* number of keys 
* number of underglow
* key color
* underglow color

Example using above arguments:

```python
Rgb_matrix_data(keys=[[249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249]],
underglow=[[0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255]])
```
[Connecting to the Serial Console](https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console)


