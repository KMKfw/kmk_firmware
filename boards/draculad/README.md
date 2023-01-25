# Draculad


The Draculad is is a feature-packed 30% split columnar staggered keyboard.
Retailers (USA)  
[Boardsource](https://boardsource.xyz/store)  

Extensions enabled by default  
- [Layers](/docs/en/layers.md) Need more keys than switches? Use layers.
- [ModTap](/docs/en/modtap.md) Allows mod keys to act as different keys when tapped.
- [Split](/docs/en/split_keyboards.md) Connects halves using a wire
- [peg_RGB_matrix](/docs/en/peg_rgb_matrix.md) Allows mod keys to act as different keys when tapped.
- [peg_oled_display](/docs/en/peg_oled_display.md) Connects halves using a wire

Common Extensions
- [Power](/docs/enpower.md) Powersaving features for battery life

## Microcontroller support

Update this line in `kb.py` to any supported microcontroller in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
