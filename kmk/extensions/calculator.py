from kmk.extensions.display import Display, TextEntry, ImageEntry

from kmk.keys import Key

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC

import time

from kmk.modules.macros import Macros

macros=Macros()

sendString = ""

binary = {
    '+': (lambda a, b: a+b, lambda a, b: a * (1+b/100)),
    '-': (lambda a, b: a-b, lambda a, b: a * (1-b/100)),
    '*': (lambda a, b: a*b, lambda a, b: a * (b/100)),
    '/': (lambda a, b: a/b, lambda a, b: a / (b/100)),
}

equation = ""
entry = ""
number1 = None
number2 = None
trail = ["Ready."]
op = None

class Calc(Key):
    def __init__(self, key, display, layer):
        self.key = key
        self.display = display
        self.layer = layer
        return

    def on_press(self, keyboard, coord_int=None):
        global entry
        global number1
        global number2
        global trail
        global op
        global binary
        global equation

        if len(self.key) == 1 and self.key in "0123456789":
            entry = entry + self.key
            equation = equation + self.key
            self.display.entries = [TextEntry(equation,x=10,y=10,y_anchor="T",layer=self.layer)]

        if self.key == "." and not "." in entry:
            if entry == "":
                entry = "0"
            entry = entry + self.key
            equation = equation + self.key
            self.display.entries = [TextEntry(equation,x=10,y=10,y_anchor="T",layer=self.layer)]

        if self.key == "c":
            entry = ""
            equation = ""
            number1 = None
            number2 = None
            op = None
            self.display.entries= [TextEntry("= Calculator Ready =",x=64,y=10,x_anchor="M",layer=self.layer)]

        if self.key == "=" and op is not None:
            if equation == "":
                equation = str(number1) + op + str(number2)
            if entry is not "":
                number2 = float(entry)
                entry = ""
            print("doing binary operation with " + str(number1) + ", " + op + ", " + str(number2))
            self.do_binary_op()
            self.display.entries=[TextEntry(equation,x=10,y=10,y_anchor="T",layer=self.layer),
                             TextEntry(format_number(str(number1)),x=118,y=54,x_anchor="R",y_anchor="B",layer=self.layer)]
            equation = ""

        if self.key in binary:
            self.display.entries=[TextEntry(equation,x=10,y=10,y_anchor="T",layer=self.layer)]
            if entry is not "":
                if number1 is None:
                    number1 = float(entry)
                    entry = ""
                elif number2 is None:
                    number2 = float(entry)
                    entry = ""
                    print("doing binary operation with " + str(number1) + ", " + op + ", " + str(number2))
                    self.do_binary_op()
            op = self.key
            if equation == "":
                equation = equation + format_number(str(number1))
            equation = equation + self.key
            self.display.entries=[TextEntry(equation,x=10,y=10,y_anchor="T",layer=self.layer)]

        if self.key == "s" and number1 is not None:
            keyboard.tap_key(KC.MACRO(format_number(str(number1))))

        self.display.render(self.layer)

    def on_release(self, keyboard, coord_int=None):
        return

    def do_binary_op(self):
        global number1
        global number2
        global op
        global binary
        global sendString
        if op and number2 is not None:
            number1 = binary[op][0](number1, number2)
            sendString = format_number(str(number1))

class InitCalc:
    def __init__(self,display,layer):
        display.entries += [TextEntry("= Calculator Ready =",x=64,y=10,x_anchor="M",layer=layer)]

def format_number(num_str):
    if "." in num_str:
        parts = num_str.split(".")
        integer_part = parts[0]
        decimal_part = parts[1].rstrip("0")
        if decimal_part:
            return f"{integer_part}.{decimal_part}"
        else:
            return integer_part
    return num_str
