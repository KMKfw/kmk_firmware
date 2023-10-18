# Corne Keyboard (CRKBD)

![Crkbd](https://boardsource.imgix.net/a90342e3-caa0-467c-bebd-d17f031d5210.jpg?raw=true)

![Crkbd](https://boardsource.imgix.net/9cbd31b7-3b37-42c6-919e-3be35a2578f6.jpg?raw=true)

A split keyboard with a 3x6 columnar stagger and 3 thumb keys.

Hardware Availability: [PCB & Case Source](https://github.com/foostan/crkbd)  

Extensions enabled by default  
- [Layers](/docs/en/layers.md) Need more keys than switches? Use layers.
- [RGB](/docs/en/rgb.md) Light it up
- [BLE_Split](/docs/en/split_keyboards.md) Connects halves without wires

Common Extensions
- [Split](/docs/en/split_keyboards.md) Connects halves using a wire
- [Power](/docs/en/power.md) Powersaving features for battery life

## Microcontroller support

Update this line in `kb.py` to any supported microcontroller in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
