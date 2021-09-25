# Mouse keys
To enable mouse cursor and/or mouse buttons control from the keyboard add this module to list:
```python
from kmk.modules.mouse_keys import MouseKeys
keyboard.modules.append(MouseKeys())
```

# Keycodes

|Keycode        | Description               |
|---------------|---------------------------|
|MB_LMB         |Left mouse button          |
|MB_RMB         |Right mouse button         |
|MB_MMB         |Middle mouse button        |
|MW_UP          |Mouse wheel up             |
|MW_DOWN, MW_DN |Mouse wheel down           |
|MS_UP          |Move mouse cursor up       |
|MS_DOWN, MS_DN |Move mouse cursor down     |
|MS_LEFT, MS_LT |Move mouse cursor left     |
|MS_RIGHT, MS_RT|Move mouse cursor right    |