# Lily 58 Pro

![Lily58](https://boardsource.imgix.net/af3d8d6d-5fbe-4578-a2ba-d09d7686fb29.jpg?raw=true)

The Lily58 is a 58 key split keyboard design by kata0510, featuring a 6x4
columnar stagger and 4 thumb cluster keys on each hand. The Lily58 is a perfect
choice for people who want to be on a split keyboard but still want to have a
fairly standard amount of keys.

Hardware Availability: [PCB & Case Source](https://github.com/kata0510/Lily58)  

Extensions enabled by default  
- [Layers](/docs/en/layers.md) Need more keys than switches? Use layers.
- [RGB](/docs/en/rgb.md) Light it up
- [BLE_Split](/docs/en/split.md) Connects halves without wires

Common Extensions
- [Split](/docs/en/split.md) Connects halves using a wire
- [Power](/docs/en/power.md) Powersaving features for battery life

## Microcontroller support

Update this line in `kb.py` to any supported microcontroller in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
