# Peg RGB Matrix

## What you can and cannot do with this extension:

### Can Do

* Set any key's LED to be any color in a syntax very similar to your keymap
* Allows specific keys to be set to OFF
* Allows underglow LEDs to be a different color than per-key LEDs
* Allows modifier keys to be set to a different color than alpha keys
* Full split keyboard support
* Change brightness of LEDs from code or using keycodes

### Cannot Do (currently in progress)

* Adjust color at runtime. Currently the extension requires changes to main.py in order to make changes to your LEDs.
* Animations
* Change LED color based on current layer

## Keycodes

Currently this extension does not support changing LEDs at runtime, as a result there are only three keycodes available to interact with this extension,those are:

* `KC.RGB_TOG`. This keycode simply toggles all your LEDs on and off.
* `KC.RGB_BRI`. This keycode increases the brightness of the LEDs.
* `KC.RGB_BRD`. This keycode decreases the brightness of the LEDs.

## Required Libraries

The following libraries must be frozen in your CircuitPython distribution or in a 'lib' folder at the root of your drive.

* [Adafruit_CircuitPython_NeoPixel](https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel)
* [Download .mpy versions from Adafruit_CircuitPython_Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20220415/adafruit-circuitpython-bundle-7.x-mpy-20220415.zip)

## Required Changes to main.py and kb.py

In order to use this extension the user must make changes to both their kb.py and main.py files. Below you will find a more comprehensive list of changes required in order to use this extension.

### kb.py

It is possible your chosen board may already have these changes made, if not you will need to make these additions:

The board's kb.py needs 3 fields:

* LED Key Position `led_key_pos`
  * Much like `coord_mapping` this tells the extension where the LEDs are on your board.
* Brightness Limit `brightness_limit`
  * Limits your brightness and may be required in order to stabilize performance.
* Number of LEDs `num_pixels`
  * Used for calculations in order to ensure the LEDs map to the correct keys.

#### Non-split Example:

Below shows a simple non-split example for a board containing 48 LEDs total and 38 keys with per-key LEDs. 
This means we will have 10 underglow LEDs and 38 per-key LEDs.
For our example we will assume (because it is most common) the underglow LEDs are connected before the per-key LEDs.
Starting from 0, indexes 0-9 are all underglow, so our `led_key_pos` array starts at 10, the `led_key_pos` array always starts with the key in the upper left position on the board.
Our example is wired in such a way where the positions layout naturally and each row simply increases by 1 starting at the upper left of the board.
Of course if your board's LEDs are layed out different, your `led_key_pos` will need to match that layout.

Underglow LEDs always appear at the end of the `led_key_pos` array, because the array always starts with per-key LEDs.

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

#### Split Example:

Below shows a 58 key split keyboard's `led_key_pos` array for a board containing 70 LEDs in total.
The board has 58 keys, meaning we are left with 12 underglow LEDs total.
Since the board is a split and we can assume the LEDs are mirrored, that means each half has 29 per-key LEDs and 6 underglow LEDs.

Let's first focus on the left half of the board.
In this example the underglow LEDs are again connected first, and this half has 6 underglow LEDs.
Starting from position 0 this means 0-5 are underglow LEDs and our per-key lighting starts at 6.
Our example board is wired in such a way where the left half's first per-key LED is position in the upper right corner of that half.
The LEDs then incremement towards the right and follow a 'zig-zag' pattern until all are accounted for (6-34).  

Examining the other half (the right side) you'll notice the LEDs are connected in a similar way but mirrored.
The right half's LEDs start in the upper left position of the board and increment towards the right, and then follow a 'zig-zag' pattern until all are accounted for (41-69).

Underglow LEDs always appear at the end of the `led_key_pos` array, because the array always starts with per-key LEDs.

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

### main.py

It is possible your chosen board may already have these changes made, if not you will need to make these additions:

```python
from kmk.extensions.peg_rgb_matrix import Rgb_matrix,Rgb_matrix_data,Color
# ... Other code
rgb_ext = Rgb_matrix(...per key color data)
keyboard.extensions.append(rgb_ext)
```

Rgb_matrix extension requires one argument (`Rgb_matrix_data`), although additional arguments can be passed, here are all arguments that can be passed to 

Rgb_matrix:

* LED Display `ledDisplay`
  * This is our primary and only required field, this takes a `Rgb_matrix_data` class.
    * Rgb_matrix_data only takes two fields:
      * Keys: an array of colors with a length equal to the number of keys on your keyboard
      * Underglow: an array of colors with a length equal to the number of underglow leds on your keyboard
* Split `split`
  * This is an optional boolean and only to be used if the keyboard is a split.
* Right Side `rightSide`
  * This is optional boolean only to be used if the keyboard is split. This signals that this configuration is targetting the right side (off side).
* RGB Order `rgb_order`
  * This is optional and only needs to be set if you are not using a WS2812 based LED.
* Disable Auto Write `disable_auto_write`
  * This is optional and only serves to make all your LEDs turn on at once instead of animate to their on state.

### Colors

Colors are RGB and can be provided in one of two ways.
Colors can be defined as an array of three numbers (0-255) or you can use the `Color` class with its default colors, see example below.

#### Passing RGB Codes

```python
Rgb_matrix_data(
    keys=[[255,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],[55,55,55],"""... rest of colors""" ],                     
    underglow=[[0,0,55],[0,0,55],"""... rest of colors""" ]
             )
```

#### Using `Color` Class

```python
Rgb_matrix_data(
    keys=[Color.RED, Color.GREEN, Color.BLUE, Color.WHITE, Color.YELLOW, Color.ORANGE,"""... rest of colors""" ],                     
    underglow=[Color.PURPLE, Color.TEAL, Color.PINK, Color.OFF,"""... rest of colors""" ]
             )
```

### Full Examples

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

#### Bonus

Because creating `ledDisplay` can be time consuming, there is a utility avaiable that will generate a basic framework for you.

```python
Rgb_matrix_data.generate_led_map(58,10,Color.WHITE,Color.BLUE)
```

Call `Rgb_matrix_data.generate_led_map` before you do any configuration beyond imports and it will print an `Rgb_matrix_data` class to your CircuitPython REPL which you can view by using a tool like "screen" or "PUTTY".

Generate LED Map Arguments:

* Number of Keys
* Number of Underglow
* Key Color
* Underglow Color

Example Using Above Arguments:

```python
Rgb_matrix_data(keys=[[249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249], [249, 249, 249]],
underglow=[[0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255]])
```

[Connecting to the Serial Console](https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console)
