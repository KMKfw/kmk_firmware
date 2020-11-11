# Layers
Layers extention adds keys for accessing other layers. It can simply be added to
 the extentions list.

```python
from kmk.extensions.layers import Layers
keyboard.extensions.append(Layers())
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

