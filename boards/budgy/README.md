# Budgy Keyboard Rev 1
Split 34 key keyboard powered by a Raspberry Pi Pico and diode-less.

![Budgy](https://i.imgur.com/2iLX4xt.jpg)

Keyboard created by [Alex Miller](https://github.com/doesntfazer)
Keyboard build guide at: [Build Guide](https://github.com/doesntfazer/Budgy/blob/main/Build%20Guides/readme.md)
KMK config created by [Jakob Edvardsson](https://github.com/JakobEdvardsson)

## Layout
This config has both US-qwerty and Swedish-Colemak-DH in mind.
The default keymap is US-qwerty, in order to switch to the Swedish-Colemak-DH keymap,
comment out the US-qwerty keymap and uncomment the Swedish-Colemak-DH keymap in the main.py file.

US-qwerty layer:
```python
#import keymap_sw as keymap  
import keymap_us as keymap
```

Swedish-Colemak-DH layer:
```python
import keymap_sw as keymap
#import keymap_us as keymap
```
