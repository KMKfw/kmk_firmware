# Layers
Layers module adds keys for accessing other layers. It can simply be added to
 the extensions list.

```python
from kmk.modules.layers import Layers
keyboard.modules.append(Layers())
```

## Keycodes

|Key         |Description                                                                  |
|-----------------|------------------------------------------------------------------------|
|`KC.DF(layer)`      |Switches the default layer                                           |
|`KC.MO(layer)`      |Momentarily activates layer, switches off when you let go            |
|`KC.LM(layer, mod)` |As `MO(layer)` but with `mod` active                                 |
|`KC.LT(layer, kc)`  |Momentarily activates layer if held, sends kc if tapped              |
|`KC.TG(layer)`      |Toggles the layer (enables it if no active, and vise versa)          |
|`KC.TO(layer)`      |Activates layer and deactivates all other layers                     |
|`KC.TT(layer)`      |Momentarily activates layer if held, toggles it if tapped repeatedly |

## Custom HoldTap Behavior
`KC.TT` and `KC.LT` use the same heuristic to determine taps and holds as
ModTap. Check out the [ModTap doc](modtap.md) to find out more.

## Example Code
For the below examples, assume an example 3x3 keyboard with 3 layers as follows:

```python
#EXAMPLE = example code

keyboard.keymap = [
	# Base layer
	[
		KC.A,	KC.B,	KC.C,
		KC.D,	KC.E,	KC.F,
		KC.G,	KC.H,	EXAMPLE,
	],

	# Arrow layer
	[
		KC.NO,	KC.UP,	KC.NO,	
		KC.LEFT,KC.DOWN,KC.RGHT,
		KC.NO,	KC.NO,	KC.TRNS,	
	],

	# Function Layer
	[
		KC.F1,	KC.F2,	KC.F3,
		KC.F4,	KC.F5,	KC.F6,
		KC.NO,	KC.NO,	KC.TRNS,	
	],
]
```

### KC.DF()
Changes the default layer until the keyboard is powered off. The following would change the above keymap 
so that the `EXAMPLE` key would set the arrow layer to be default until the kyeboard is powered off.

```python
EXAMPLE = KC.DF(1)
```

### KC.MO()
Activates specified layer while held, similar to how the `Fn` key works on a normal keyboard. The following 
would activate the Function layer while held.

```python
EXAMPLE = KC.MO(2)
```

### KC.LM()
Activates the specified layer with the specified modifier key active, which can be nicer than holding down 
multiple keys. The following example activates the Function layer with the `RALT` (right Alt) key active, too.

```python
EXAMPLE = KC.LM(2, KC.RALT)
```

### KC.LT()
Activates the specified layer when held but passes the specified keycode when tapped. The following would 
activate the Arrow layer when held but send an "i" when tapped.

```python
EXAMPLE = KC.LT(1, KC.I)
```

### KC.TG()
Toggles the specified layer on/off when tapped. Other active layers below the toggled layer in the stack 
may be applicable if the toggled layer has `KC.TRNS` in the same position. The following would toggle the 
Arrow layer on/off when tapped (note the `KC.TRNS` in the bottom-right position of the Arrow layer allows 
the `EXAMPLE` key to be pressed on the base layer even when the Arrow layer is active).

```python
EXAMPLE = KC.TG(1)
```

### KC.TO()
Toggles the specified layer _and deactivates all other layers._ *NOTE:* be careful using this keycode! If 
you don't have another layer switch on the toggled layer, the only way to return to the base layer is to 
power-cycle the keyboard. The following would turn the keyboard into a navigation pad with 5 useless keys 
until it was restarted by activating the Arrow layer and deactivating the base layer.

```python
EXAMPLE = KC.TO(1)
```

### KC.TT()
Momentarily switches to the specified layer when held or toggles that same layer when tapped. The following 
would momentarily activate the Function layer when held or toggle that layer when tapped (note that the layer 
can be toggled back thanks to the `KC.TRNS` on the Function layer, similar to the `KC.TG()` example above).

```python
EXAMPLE = KC.TT(2)
```
