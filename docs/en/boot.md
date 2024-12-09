# boot.py
`boot.py` lives in the root of your keyboard when mounted as a storage device.
There is a more detailed explanation in the [CircuitPython Documentation](https://docs.circuitpython.org/en/latest/README.html),
however there are some common use cases for your keyboard listed on this page.


## KMK's builtin boot configurator

KMK ships with a handy boot configuration function that does all the hard work
for you.
The interface may change in the future, but there is a safety mechanism in
place: if anything goes wrong, it'll boot into a mountable and debuggable
configuration.


### Signature

```python
from kmk.bootcfg import bootcfg

bootcfg(
    # optional:
    sense: Optional[microcontroller.Pin, digitalio.DigitalInOut] = None,
    source: Optional[microcontroller.Pin, digitalio.DigitalInOut] = None,
    autoreload: bool = True,
    boot_device: int = 0,
    cdc_console: bool = True,
    cdc_data: bool = False,
    consumer_control: bool = True,
    keyboard: bool = True,
    midi: bool = True,
    mouse: bool = True,
    nkro: bool = False,
    pan: bool = False,
    storage: bool = True,
    usb_id: Optional[tuple[str, str]] = None,
    **kwargs,
) -> bool
```
All optional parameters are set to reflect common CircuitPython defaults, however
they may differ from board specific defaults.


#### `sense`
`sense` accepts either uninitialized `Pin`s or `DigitalInOut` instances for
maximum flexibility.
The lockout-prone subset of boot configuration is only applied if `sense` reads `True` or "high", and
skipped if it reads `False` or "low". The latter is also true if `sense` is not provided.
If `sense` is an uninitialized `Pin`, it'll be configured as pulled-up input; it
wont be further configured if it is a `DigitalInOut`.


#### `source`
`source` accepts either uninitialized `Pin`s or `DigitalInOut` instances for
maximum flexibility.
It's the "source" of the test voltage to be read by the sense pin.
If `source` is an uninitialized `Pin`, it'll be configured as a "low" output; it
wont be further configured if it is a `DigitalInOut`.

Common matrix and direct pin configurations (see also the examples below):

|diode_orientation |sense pin  |source pin |
|------------------|-----------|-----------|
|`COL2ROW`         |column     |row        |
|`ROW2COL`         |row        |column     |
|direct pin        |direct pin |`None`     |


#### `autoreload`
CircuitPython will automatically reload when any data or meta data is written to
the CircuitPython drive.
Certain operating systems tend to do that without asking; in that case
`autoreload` can be disabled as a workaround.


#### `boot_device`
Boot HID device configuration for `usb_hid`, see the [`usb_hid` documentation](https://docs.circuitpython.org/en/latest/shared-bindings/usb_hid/index.html#usb_hid.enable)
for details.


#### `cdc_console`
This will enable or disable the USB endpoint for the serial console with REPL.
**Caution**: If erroneous `sense` parameter is provided, changing this might make recovery problematic.


#### `cdc_data`
This will enable or disable the USB endpoint for the data serial.


#### `consumer_control`
Enable the HID endpoint for consumer control reports. Those are extra keys for
things like multimedia control and browser shortcuts.


#### `keyboard`
Enable the keyboard HID endpoint. Why would you disable that? For a split half
that isn't connected to USB and needs extra memory for a massive display maybe?


#### `midi`
It's MIDI over USB. Enabled by default in CircuitPython, but most keyboards don't use it.


#### `mouse`
Enable the HID endpoint for a pointing device. A pointing device, or mouse, is
like a keyboard, but with continuous instead of binary keys... which also go
sideways.


#### `nkro`
Enable n-key rollover support. If the default keyboard is enabled, this option
will replace the standard 6-key rollover endpoint with an n-key rollover one.
This is technically not a standard HID endpoint, but if you want this, you
probably know what you're doing.


#### `pan`
Enable panning, aka horizontal scrolling, for the pointing device, aka mouse,
hid endpoint.


#### `storage`
Disable storage if you don't want your computer to go "there's a new thumb drive
I have to mount!" every time you plug in your keyboard.
**Caution**: If erroneous `sense` parameter is provided, changing this might make recovery problematic.


#### `usb_id`
A recent addition to CircuitPython 8 is the ability to give your keyboard an
identity other than "MCU board manufacturer" - "CircuitPython device".


#### return value
`bootcfg` returns `true` if boot configuration applied successfully and `false`
if it was skipped, in case you want to use the sense pin mechanism for other
custom boot configurations.
Any *unexpected* errors are intentionally not handled, in order to be recorded
to the `boot_out.txt` file for easier debugging.


### Example 1
* diode direction from columns to rows,
* disabled storage
* disabled midi
* disabled mouse
* custom vendor and device names

```python
import board

from kmk.bootcfg import bootcfg

bootcfg(
    sense=board.GP0,  # column
    source=board.GP8, # row
    midi=False,
    mouse=False,
    storage=False,
    usb_id=('KMK Keyboards', 'Custom 60% Ergo'),
)

```
*Tip*: for a diode direction from rows to columns, switch row and column GPIOs
when assigning them to sense and source.


### Example 2
Dedicated switch to disable boot configuration, connected to ground:

```python
import board

from kmk.bootcfg import bootcfg

bootcfg(sense=board.GP22, ...)
```

### Example 3
Shut-in mode:
**Always** apply boot configuration and disable any contact to the outside
world.
**Caution**: this an example for a `DigitalInOut` sense pin, and probably an
unwise thing to do in actuality.

```python
import board
import digitalio

from kmk.bootcfg import bootcfg

sense = digitalio.DigitalInOut(board.GP42)
sense.direction = digitalio.Direction.OUTPUT
sense = True

bootcfg(
    sense=sense,
    cdc_console=False,
    consumer_control=False,
    keyboard=False,
    midi=False,
    mouse=False,
    storage=False,
)
```

We generally advise against importing your keyboard definition and using
rows/columns to define sense and source pins, because that essentially loads
the firmware twice, almost doubling boot times.
