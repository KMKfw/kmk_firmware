# Calculator

This extension adds a basic 4-function (+,-.*,/) calculator used with an attached display.

## Adding the calculator extension

You'll need to make sure you have a [display](Display.md) working first. Then import the calculator functions:

`from kmk.extensions.calculator import Calc, InitCalc`

Initialise the calculator, point it to the display, and tell it the layer you want your calculator functions associated with. For example, if your display is called "display" and your calculator buttons are going to be on layer 1, use:

`InitCalc(display,1)`

This will prepare a "calculator ready" screen on that layer.

Now you need to create the keys for your calculator. Normally there will be 17 of these: one for each digit, one for each arithmetic function, one for the decimal point, one for the equals/enter button, and one to clear. Each one needs to be pointed to the display and layer like the init function above:

```
KC_C0 = Calc("0",display,1)
KC_C1 = Calc("1",display,1)
KC_C2 = Calc("2",display,1)
KC_C3 = Calc("3",display,1)
KC_C4 = Calc("4",display,1)
KC_C5 = Calc("5",display,1)
KC_C6 = Calc("6",display,1)
KC_C7 = Calc("7",display,1)
KC_C8 = Calc("8",display,1)
KC_C9 = Calc("9",display,1)
KC_CEQ = Calc("=",display,1)
KC_CADD = Calc("+",display,1)
KC_CSUB = Calc("-",display,1)
KC_CMUL = Calc("*",display,1)
KC_CDIV = Calc("/",display,1)
KC_CPT = Calc(".",display,1)
KC_CCL = Calc("c",display,1)
```

Now you can add these new keycodes to your keymap and you'll have a working desktop calculator!
