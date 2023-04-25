# Alt GUI Swap
This module allows to swap Alt with GUI and vice versa. This will reset on restart to the default implementation

## Enabling the module
```python
from kmk.modules.ag_swap import AgSwap
# ag_swap disabled on startup
ag_swap = AgSwap()
# ag_swap enabled on startup
# ag_swap = AgSwap(ag_swap_enable=True)
keyboard.modules.append(ag_swap)

keyboard.keymap = [
	[
        KC.AG_SWAP, # swap alt and gui
        KC.AG_NORM, # unswap alt and gui
        KC.AG_TOGG, # toggles alt and gui swap
    ],
]
```
