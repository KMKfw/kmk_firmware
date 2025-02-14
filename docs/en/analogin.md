# AnalogIn

Make use of input sources that implement CircuitPython's `analogio` interface.

## Usage

### AnalogInputs 

The module that reads and maps "analog" inputs to events/actions.

```python
from kmk.modules.analogin import AnalogInputs, AnalogInput

analog = AnalogInputs(
    inputs: list(AnalogInput),
    evtmap=[[]],
    update_interval: int = 10,
)
```

#### `inputs`

A list of `AnalogInput` objects, see below.

#### `evtmap`

The event map is `AnalogIn`s version of `keyboard.keymap`, but for analog events
instead of keys.
It supports KMK's layer mechanism and `KC.TRNS` and `KC.NO`.
Any other keys have to be wrapped in `AnalogKey`, see below.

#### `update_interval`
The update interval limits how often new values are read from inputs; the value
unit is milliseconds and the default is set to 10ms.
In addition to limiting analog conversions, which can take a significant amount
of time if there's a lot of them, a fixed interval provides a more predictable
time base for repeating events.

### AnalogInput

A light wrapper around objects that implement CircuitPython's analogio
interface, i.e. objects that have a `value` property that contains the current
value in the domain [0, 65535].

```python
from kmk.modules.analogin import AnalogInput
a = AnalogInput(
    input: AnalogInput,
    filter: Optional(Callable[AnalogInput, int]) = lambda input:input.value>>8,
)

a.value
a.delta

```

#### `input`

An `AnalogIn` like object.

#### `filter`

A customizable function that reads and transforms `input.value`.
The default transformation maps uint16 ([0-65535]) to uint8 ([0-255]) resolution.

#### `value`

Holds the transformed value of the `AnalogIn` input.
To be used in handler functions.

#### `delta`

Holds the amount of change of transformed value of the `AnalogIn` input.
To be used in handler functions.


### AnalogEvent

The analog version of [`Key` objects](keys.md).

```python
from kmk.modules.analogin import AnalogEvent

AE = AnalogEvent(
    on_change: Callable[self, AnalogInput, Keyboard, None] = pass,
    on_stop: Callable[self, AnalogInput, Keyboard, None] = pass,
)
```

### AnalogKey

A "convenience" implementation of `AnalogEvent` that emits `Key` objects.

```python
from kmk.modules.analogin.keys import AnalogKey

AK = AnalogKey(
    key: Key,
    threshold: Optional[int] = 127,
)
```

## Examples

### Analogio with AnalogKeys

```python
import board
from analogio import AnalogIn
from kmk.modules.analogin import AnalogInput, AnalogInputs
from kmk.modules.analogin.keys import AnalogKey

analog = AnalogInputs(
    [
        AnalogInput(AnalogIn(board.A0)),
        AnalogInput(AnalogIn(board.A1)),
        AnalogInput(AnalogIn(board.A2)),
    ],
    [
        [AnalogKey(KC.X), AnalogKey(KC.Y), AnalogKey(KC.Z)],
        [KC.TRNS, KC.NO, AnalogKey(KC.W, threshold=96)],
    ],
)

keyboard.modules.append(analog)
```

### External DAC with AnalogEvent

Use an external ADC to adjust `HoldTap.tap_time` at runtime between 20 and 2000 ms.
If no new readings occur: change RGB hue.
But careful: if changed by more than 100 units at a time, the board will reboot.

```python
# setup of holdtap and rgb omitted for brevity
# holdtap = ...
# rgb = ...

import board
import busio
import adafruit_mcp4725

from kmk.modules.analogin import AnalogEvent, AnalogInput, AnalogInputs

i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c)

def adj_ht_taptime(self, event, keyboard):
    holdtap.tap_time = event.value
    if abs(event.change) > 100:
        import microcontroller
        microcontroller.reset()

HTT = AnalogEvent(
    on_change=adj_ht_taptime,
    on_stop=lambda self, event, keyboard: rgb.increase_hue(16),
)

a0 = AnalogInput(dac, lambda _: int(_.value / 0xFFFF * 1980) + 20)

analog = AnalogInputs(
    [a0],
    [[HTT]],
)

keyboard.modules.append(analog)
```
