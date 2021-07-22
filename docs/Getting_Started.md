# Getting Started
> Life was like a box of chocolates. You never know what you're gonna get.

KMK is a keyboard focused and optimised layer that sits on top of [CircuitPython](https://circuitpython.org/). As such, it should work with most [boards that support CircuitPython](https://circuitpython.org/downloads). It is recommanded to use the last stable version (>5.0).
Known working and recommanded devices can be found [here](Officially_Supported_Microcontrollers.md)

If you're wondering why use KMK rather than barebone CircuitPython, we tried to compare both approaches [here](kmk_vs_circuitpython.md)

<br>

## TL;DR Quick start guide
> To infinity and beyond!
1. [Install CircuitPython on your board](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython). With certain boards (pico, I look at you !), it can be as easy as drag and dropping the firmware on the drive
2. Get a [copy of KMK](https://github.com/KMKfw/kmk_firmware/archive/refs/heads/master.zip) from the master branch 
3. Unzip it and copy the KMK folder and the boot.py file at the root of the USB drive corresponding to your board (often appearing as CIRCUITPY)
4. Create a new file in the same root directory (same level as boot.py) with the example content hereunder : 



***IMPORTANT :*** adapt the GP0 / GP1 pins to your specific board ! <br>

NB : You can call it whatever you want or "mybrandnewboard.py


```
print("Starting")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.matrix import DiodeOrientation

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP0,)
keyboard.row_pins = (board.GP1,)
keyboard.diode_orientation = DiodeOrientation.COLUMNS

keyboard.keymap = [
    [KC.A,]
]

if __name__ == '__main__':
    keyboard.go()
```

5. With a wire / paperclip / whatever, connect GPIO 0 & GPIO 1 together (or the pins you chose for your boards)

6. If it prints a "A" (or a "Q" or ... depending on your keyboard layout), you're done !

<br>


## Now that you're up and running, you may want to go further  ...
> This is your last chance. After this, there is no turning back. You take the blue pill—the story ends, you wake up in your bed and believe whatever you want to believe. You take the red pill—you stay in Wonderland, and I show you how deep the rabbit hole goes. Remember: all I'm offering is the truth. Nothing more.

### You're extremely lucky and you have a fully supported keyboard
If your keyboard and microcontroller are officially supported, simply visit the  page for your files, and dropping them on the root of the "flash drive". Those pages can be found [here](https://github.com/KMKfw/boards). You will need the `kb.py` and `main.py`. More advanced instructions can be found [here](config_and_keymap.md). If using Curcuitpython and NOT KMKPython, you will also need [boot.py](https://github.com/KMKfw/kmk_firmware/blob/master/boot.py)

### You've got another, maybe DIY, board and want to customise KMK for it  
First, be sure to understand how your device work, and particularly its specific matrix configuration. You can google or have read of the [fantastic guide](https://docs.qmk.fm/#/hand_wire) provided by the QMK team for handwired keyboards
<br>Once you've got the gist of it:
- You can have a look [here](porting_to_kmk.md) to start customizing your file (not a typo : all your keyboard config can sit in the same file you started with)
- You can also get ideas from the various [user examples](https://github.com/KMKfw/user_keymaps) that we provide
- Want to have fun features such as RGB, split keyboards and more? Check out what extensions can do [here](extensions.md)

<br>

## Additional help and support
> Roads? Where we're going we don't need roads.

In case you need it, debugging help can be found [here](debugging.md)

If you need support with KMK or just want to say hi, find us in 
[#kmkfw:klar.sh on Matrix](https://matrix.to/#/#kmkfw:klar.sh).  This channel is 
bridged to Discord [here](https://discordapp.com/widget?id=493256121075761173&theme=dark) 
for convenience. If you ask for help on chat or open a bug report, if possible 
please give us your commit SHA, found by running 
`from kmk.consts import KMK_RELEASE;  print(KMK_RELEASE)` in the REPL on your 
controller.
 





