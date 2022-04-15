# Peg Oled Display
To use this you need to make some changes to your kb.py as well as you main.py I will break it into two sections for you. 

### What you can and cant do

#### Can do
* display images
* display text
* set images or text to react to your layer


#### Cant do yet / on the way
* react to battery percentage
* react to WPM 

## kb.py
Your chosen board may already have these changes done If not you will need to add them.

you need to add SCL and SDA to your keyboard. The pins the oled are connected to on your controller may not be called "SCL"and "SDA" they could be "GP21" and "GP13" for example. The best way to find out what they are is look at the boards pinout.
```python
    SCL=board.SCL
    SDA=board.SDA
```


## Main.py
These are the changes that need to be made / added to your main.py
### Config
no mater how you are going to use the oled you need this part
```python
    from kmk.extensions.peg_oledDisplay import oled
    keyboard = KMKKeyboard()
    # ... Other oled code
    keyboard.extensions.append(oled_ext) 

```
### Photos
So the config for photos is quite simple. Getting the photos maybe not so much. I will explain.

oled takes 3-4 arguments 
1. keyboard
    * this is where we get the config from
2.  array of data
    * this array can have a length of 1 or 4. For images we use a length of 1.
    * Every item in the array has 2 fields 
    * 0: this is the reaction type right now it can be "LAYER" or "STATIC"
    * 1: the items you want to show for the reaction. In this example 4 images to switch on the 4 layers
3. toDisplay this takes a string "TXT" or "IMG".
    * this tells the extension to load images or text.
4. flip Boolean this will simply flip your display.

![code layout](https://i.imgur.com/MrRYzo8.png)

```python
oled_ext = oled(keyboard, [{0:"LAYER",1:["1.bmp","2.bmp","3.bmp","4.bmp"]}],toDisplay='IMG',flip=True)
```
In this code example we are saying to react to the layer change and load a image filed named "1.bmp" for layer one and "2.bmp" for layer two and so on.
### Preparing the images
So you need to include all the images in your circuitpython drive in the root along side main.py

Your images need to be 128x32px and should only be black and white. After you have made your image you can save as a "monochrome bmp" this will save you a lot of space.

### Text
Ok now we get into something that looks a lot more complicated but we will get though it.

Almost everything is the same we are still passing in the keyboard for pin config. We swap toDisplay to "TXT" lets get into that array.

So each item in the array is a corner of the oled display

0. top left
1. top right
2. bottom left
3. bottom right
After that is the same as the previous example. Each one has two fields 0:the reaction type. 1:what to display

In this code we will always display the word "layer" in the top left corner of the screen then the other 3 corners will swap depending on the layer. 

![code layout](https://i.imgur.com/wXl8nmZ.png)


```python
oled_ext = oled(keyboard,[
    {0:"STATIC",1:["layer"]},
    {0:"LAYER",1:["1","2","3","4"]},
    {0:"LAYER",1:["base","raise","lower","adjust"]},
    {0:"LAYER",1:["qwerty","nums","shifted","leds"]}
    ],toDisplay='TXT',flip=False)
```
![example](https://boardsource.imgix.net/a4f155e0-bc83-11ec-a4ed-79d542ba3127.gif)

