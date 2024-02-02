# Steno

Communicate with stenography software such as [Plover](https://www.openstenoproject.org/plover/) over the Gemini PR protocol.

## Setup

You must include the following in `boot.py` to enable data serial.

```python
import usb_cdc
usb_cdc.enable(data=True)
```

Then, instantiate the module as usual and add steno keys to your keymap.

```python
from kmk.modules.steno import Steno
keyboard.modules.append(Steno())
```

## Keys

The following keys are created for use in your keymap:

| Keycode    | Description   |
|------------|---------------|
| `KC.STN_LS1`  | S1-           |
| `KC.STN_LS2`  | S2-           |
| `KC.STN_LT`   | T-            |
| `KC.STN_LK`   | K-            |
| `KC.STN_LP`   | P-            |
| `KC.STN_LW`   | W-            |
| `KC.STN_LH`   | H-            |
| `KC.STN_LR`   | R-            |
| `KC.STN_A`    | A             |
| `KC.STN_O`    | O             |
| `KC.STN_AS1`  | * Top-left    |
| `KC.STN_AS2`  | * Lower-left  |
| `KC.STN_AS3`  | * Top-right   |
| `KC.STN_AS4`  | * Lower-right |
| `KC.STN_E`    | E             |
| `KC.STN_U`    | U             |
| `KC.STN_RF`   | -F            |
| `KC.STN_RR`   | -R            |
| `KC.STN_RP`   | -P            |
| `KC.STN_RB`   | -B            |
| `KC.STN_RL`   | -L            |
| `KC.STN_RT`   | -T            |
| `KC.STN_RS`   | -S            |
| `KC.STN_RD`   | -D            |
| `KC.STN_RZ`   | -Z            |
| `KC.STN_N1`   | Number bar 1  |
| `KC.STN_N2`   | Number bar 2  |
| `KC.STN_N3`   | Number bar 3  |
| `KC.STN_N4`   | Number bar 4  |
| `KC.STN_N5`   | Number bar 5  |
| `KC.STN_N6`   | Number bar 6  |
| `KC.STN_N7`   | Number bar 7  |
| `KC.STN_N8`   | Number bar 8  |
| `KC.STN_N9`   | Number bar 9  |
| `KC.STN_NA`   | Number bar A  |
| `KC.STN_NB`   | Number bar B  |
| `KC.STN_NC`   | Number bar C  |
| `KC.STN_FN`   | Function      |
| `KC.STN_RES1` | Reset 2       |
| `KC.STN_RES2` | Reset 1       |
| `KC.STN_PWR`  | Power         |

## Connecting Plover

Open the Plover configuration to the Machine tab. Set Machine to Gemini PR. Then, under Connection set the Port to the keyboard's serial data interface (this may take some trial and error if you are unsure which one to use). All other settings can be left as their defaults.
