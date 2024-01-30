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

| Keycode   | Description   |
|-----------|---------------|
| STN_LS1   | S1-           |
| STN_LS2   | S2-           |
| STN_LT    | T-            |
| STN_LK    | K-            |
| STN_LP    | P-            |
| STN_LW    | W-            |
| STN_LH    | H-            |
| STN_LR    | R-            |
| STN_A     | A             |
| STN_O     | O             |
| STN_AS1   | * Top-left    |
| STN_AS2   | * Lower-left  |
| STN_AS3   | * Top-right   |
| STN_AS4   | * Lower-right |
| STN_E     | E             |
| STN_U     | U             |
| STN_RF    | -F            |
| STN_RR    | -R            |
| STN_RP    | -P            |
| STN_RB    | -B            |
| STN_RL    | -L            |
| STN_RT    | -T            |
| STN_RS    | -S            |
| STN_RD    | -D            |
| STN_RZ    | -Z            |
| STN_N1    | Number bar 1  |
| STN_N2    | Number bar 2  |
| STN_N3    | Number bar 3  |
| STN_N4    | Number bar 4  |
| STN_N5    | Number bar 5  |
| STN_N6    | Number bar 6  |
| STN_N7    | Number bar 7  |
| STN_N8    | Number bar 8  |
| STN_N9    | Number bar 9  |
| STN_NA    | Number bar A  |
| STN_NB    | Number bar B  |
| STN_NC    | Number bar C  |
| STN_FN    | Function      |
| STN_RES1  | Reset 2       |
| STN_RES2  | Reset 1       |
| STN_PWR   | Power         |

## Connecting Plover

Open the Plover configuration to the Machine tab. Set Machine to Gemini PR. Then, under Connection set the Port to the keyboard's serial data interface (this may take some trial and error if you are unsure which one to use). All other settings can be left as their defaults.
