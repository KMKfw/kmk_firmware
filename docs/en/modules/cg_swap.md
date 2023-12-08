# Ctrl GUI Swap
This module allows to swap Ctrl with GUI and vice versa. This will reset on restart to the default implementation

## Enabling the module
```python
from kmk.modules.cg_swap import CgSwap
# cg_swap disabled on startup
cg_swap = CgSwap()
# cg_swap enabled on startup
# cg_swap = CgSwap(cg_swap_enable=True)
keyboard.modules.append(cg_swap)

keyboard.keymap = [
	[
        KC.CG_SWAP, # swap ctrl and gui
        KC.CG_NORM, # unswap ctrl and gui
        KC.CG_TOGG, # toggles ctrl and gui swap
    ],
]
```

