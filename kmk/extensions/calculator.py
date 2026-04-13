from kmk.extensions.display import Display, TextEntry, ImageEntry

from kmk.keys import Key

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC

import time

from kmk.modules.macros import Macros

macros=Macros()


binary = {
    '+','-','*','/'
}

equation = ""
entry = ""
result = ""
op = None

class Calc(Key):
    def __init__(self, key, display, layer):
        self.key = key
        self.display = display
        self.layer = layer
        return

    def on_press(self, keyboard, coord_int=None):
        global entry
        global result
        global op
        global binary
        global equation

        if len(self.key) == 1 and self.key in "0123456789":
            if result is not "":
                entry = ""
                result = ""
            entry = entry + self.key
            equation = equation + self.key
            print("equation: " + equation)
            self.display.entries = [TextEntry(equation,x=10,y=10,y_anchor="T",layer=self.layer)]

        elif self.key == "." and not "." in entry:
            if entry == "":
                entry = "0"
            entry = entry + self.key
            equation = equation + self.key
            self.display.entries = [TextEntry(equation,x=10,y=10,y_anchor="T",layer=self.layer)]

        elif self.key == "c":
            entry = ""
            equation = ""
            result = ""
            op = None
            self.display.entries= [TextEntry("= Calculator Ready =",x=64,y=10,x_anchor="M",layer=self.layer)]

        elif self.key == "=":
            if equation == "" and op is not None:
                equation = str(result) + op + str(entry)
            print("evaluating equation: " + equation)
            result = eval(equation)
            self.display.entries=[TextEntry(equation,x=10,y=10,y_anchor="T",layer=self.layer),
                             TextEntry(format_number(str(result)),x=118,y=54,x_anchor="R",y_anchor="B",layer=self.layer)]
            equation = ""

        elif self.key in binary and equation is not "" and equation[-1:] not in binary:
            self.display.entries=[TextEntry(equation,x=10,y=10,y_anchor="T",layer=self.layer)]
            if entry is not "":
                entry = ""
            elif equation == "":
                equation = format_number(str(result))
            equation = equation + self.key
            op = self.key
            self.display.entries=[TextEntry(equation,x=10,y=10,y_anchor="T",layer=self.layer)]

        elif self.key in binary and result is not "":
            equation = str(result) + self.key
            self.display.entries = [TextEntry(equation,x=10,y=10,y_anchor="T",layer=self.layer)]

        elif self.key == "s" and result is not "":
            keyboard.tap_key(KC.MACRO(format_number(str(result))))

        self.display.render(self.layer)

    def on_release(self, keyboard, coord_int=None):
        return

    def do_binary_op(self):
        global number1
        global number2
        global op
        global binary
        if op and number2 is not None:
            number1 = binary[op][0](number1, number2)
            print("number1 is now " + str(number1))

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
