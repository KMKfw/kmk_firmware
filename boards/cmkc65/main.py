#==================================
# This code is meant to be a sanity check after assembling the circuits on the PCB.
# and flashing the uC. We can check that every button is "seen" when we press it.
#==================================

#print("Hello World!")

import board
import digitalio
import time


from kb import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.extensions.peg_oled_Display import Oled,OledDisplayMode,OledReactionType,OledData
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.handlers.sequences import send_string
from kmk.handlers.sequences import simple_key_sequence


WOW = send_string("Wow, KMK is awesome!")





#==================================
# E and LE pins
#==================================
    #LE needs to be high
    #E needs to be low
LE = digitalio.DigitalInOut(board.P0_24)
LE.direction = digitalio.Direction.OUTPUT
LE.value = 1

E = digitalio.DigitalInOut(board.P0_31)
E.direction = digitalio.Direction.OUTPUT
E.value = 0

#print(dir(board))  #shows all pins names on uC


#from kb import KMKKeyboard
keyboard = KMKKeyboard()

keyboard.modules.append(Layers())
keyboard.extensions.append(MediaKeys())

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

print("Starting")


# Regular GPIO Encoder
encoder_handler.pins = (
    # regular direction encoder and a button
    ( board.P1_06, board.P1_04, board.P0_11,),
    )    # encoder #1 

 # Rotary Encoder (1 encoder / 1 definition per layer)
encoder_handler.map = [ ((KC.UP, KC.DOWN, KC.MPLY),), # Standard                        
                        ((KC.VOLU, KC.VOLD, KC.MPLY),), # Extra
                        ((KC.A, KC.Z, KC.N1),), # NumPad not yet properly configured
                        ((KC.A, KC.Z, KC.N1),), # Gaming not yet properly configured
                        ]  
                        
encoder_handler.divisor = 2

keyboard.keymap = [
    # Base Layer
    [
        KC.ESC, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.MINUS, KC.EQUAL, KC.BSPC, KC.NO, KC.NO,
        KC.TAB, KC.Q, KC.W, KC.E, KC.R, KC.T, KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRACKET, KC.RBRACKET, KC.BSLASH, KC.DELETE, KC.NO,
        KC.CAPS, KC.A, KC.S, KC.D, KC.F, KC.G, KC.H, KC.J, KC.K, KC.L, KC.SCOLON, KC.QUOTE, KC.NO, KC.ENTER, KC.HOME, KC.NO,
        KC.LSHIFT, KC.Z, KC.X, KC.C, KC.V, KC.B, KC.N, KC.M, KC.COMMA, KC.DOT, KC.SLASH, KC.RSHIFT, KC.NO, KC.UP, KC.END, KC.NO, 
        KC.LCTRL, KC.LGUI, KC.LALT, KC.NO, KC.NO, KC.SPACE, KC.NO, KC.NO, KC.RALT, KC.TT(1), KC.RCTRL, KC.LEFT, KC.NO, KC.DOWN, KC.RIGHT, KC.NO,
    ],
    
    # Function Layer
    [
        KC.TILDE, KC.F1, KC.F2, KC.F3, KC.F4, KC.F5, KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.F11, KC.F12, KC.TRNS, KC.NO, KC.NO,
        KC.TRNS, KC.BT_PREV_CONN, KC.BT_NEXT_CONN, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.NO,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.PGUP, KC.NO,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.PGDN, KC.NO, KC.NO,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TT(0), KC.TT(2), KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,
    ],
    
     # Meme Layer
    [
        KC.TO(0), WOW, KC.NO, KC.NO, KC.F4, KC.F5, KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.F11, KC.F12, KC.TRNS, KC.NO, KC.NO,
        KC.TRNS, KC.BT_PREV_CONN, KC.BT_NEXT_CONN, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.NO,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.PGUP, KC.NO,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.PGDN, KC.NO, KC.NO,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.NO, KC.TT(0), KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,
    ],
]


oled_ext = Oled(
    OledData(
        corner_one={0:OledReactionType.STATIC,1:["layer"]},
        corner_two={0:OledReactionType.LAYER,1:["1","2","3","4"]},
        corner_three={0:OledReactionType.LAYER,1:["base","fn layer","meme time","adjust"]},
        corner_four={0:OledReactionType.LAYER,1:["qwerty","function","memes bro","leds"]}
        ),
        toDisplay=OledDisplayMode.TXT,flip=False)

keyboard.extensions.append(oled_ext) 

print("here bottom of main.py")
if __name__ == '__main__':
    keyboard.go()