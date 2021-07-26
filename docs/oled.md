# Oled

**This only supports SSD1306 OLEDs currently over I2C connection**
Kinda useless, super cool!

## Enabling the extension

You need to place adafruit_displayio_ssd1306.mpy in your lib folder, and if you'd like to display text, you need to download adafruit_display_text and place the label.mpy file in your lib folder as well.
The constructor takes a minimun of 4 arguments: your SDA pin, your SCL pin, a file path to an **Indexed BMP file** OR a string to display.
If you want to display and image, you must create an indexed BMP file, and store said file on your KMK drive

### Constructor

SDA = The SDA pin on your board
SCL = The SCL pin on your board
The third argument will first check for a valid file bmp file path, if no file exists, it will resort to displaying text, and finally, if nothing is passed in, then it will default to showing the active layer.

    - Ex. "images\\tenor.bmp" or "Hello World"
 oWidth = Width of the oled display
 oHeight = height of oled display
 tileWidth = resolution of image -- Width
- Cannot be larger than the Width of your display

tileHeight = Resolution of image -- Height
- Cannot be larger than the height of your display

gridWidth = Number of tiles to display width wise
- Usually set to width of display, sets the width of the container for your tiles

gridHeight = Number of tiles to display height wise
- Usually set to height of display, sets the height of the container for your tiles

## Indexed BMP image

1. Install [Gimp](https://www.gimp.org/)
2. Open your image in GIMP
3. In the menu at the top, go to Image --> Crop to Content
4. Go to Image --> Mode --> Indexed --> Select "Use black and white (1-bit) palette --> Click Convert
- You are going to lose some detail here but it is a necessary evil
5. Click Image --> Scale image --> Enter your desired size
- Note: It must fit within the constraints of your display
- Ex. If my display is 128x32, my image must be of that size or smaller
- You can unlink the size auto adjustment by clicking the chain-link right next to Width & Height
- Leave X and Y Resolution
6. Go to Colors --> Invert
7. Your image should be completely black and white so naturally we are going to convert it back to RGB by going to Image --> Mode --> RGB
8. Anything, black or transparent we want to make a solid color that isn't white or black; I chose pink but you can use whatever color you want.
9. Right click the transparent section of the image if you have one and go to Select --> By Color
10. Select your color, and the paint bucket, and click your newly selected area.
11. Make anything else that isn't white, your selected color
12. Select Image --> Mode --> Indexed --> Generate Optimum Palette
13. Select Colors --> Map --> Rearrange Colormap --> Ensure your color is at index 0; If it is not, drag and drop it to position 0 --> Select OK
14. Select File --> Export As --> "Insert Name Here.bmp" --> Export --> Place it on your KMK Drive
15. Done :)

## Setup

1. Find a BMP image you like and convert it to an indexed BMP by following the above instructions
2. Place image somewhere on drive and make a note of the absolute path for later.
3. Enable extension by something similar to the code below, inputting image path or text where necessary

```
from from kmk.extensions.oledDisplay import oled
[...KMK CODE ]
keyboard.extensions.append(oled(board.GP21, board.GP20, toDisplay = "IMAGE\\PATH", oWidth = OLEDWIDTH, oHeight = OLEDHEIGHT, tileWidth = WIDTH OF IMAGE, tileHeight = HEIGHT OF IMAGE, gridWidth = IMAGE REPETITION ACROSS, gridHeight = IMAGE REPETITION UP))
# Note, my image is a 128x32 indexed bmp, if I had a 32x32 indexed BMP, it can repeat across my screen 4 times, so my constructor would look like this instead:
# keyboard.extensions.append(oled(board.GP21, board.GP20, toDisplay = "images\\f.bmp", oWidth = 128, oHeight = 32, tileWidth = 32, tileHeight = 32, gridWidth = 4, gridHeight = 1))
[...KMK CODE]
```

B. Text

```
from from kmk.extensions.oledDisplay import oled
[...KMK CODE ]
keyboard.extensions.append(oled(board.GP21, board.GP20, "Hello World"))
[...KMK CODE]
```

C. Active Layer

```
from from kmk.extensions.oledDisplay import oled
[...KMK CODE ]
keyboard.extensions.append(oled(board.GP21, board.GP20))
[...KMK CODE]
```
