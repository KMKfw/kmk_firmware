# DracuLad

The [DracuLad](https://github.com/MangoIV/dracuLad) is a feature-packed 30% sized, split bodied, columnar staggered keyboard.

![Top View](https://github.com/mangoiv/draculad/raw/master/pictures/rev1/both_sides_underglow_oleds.jpg)

Extensions enabled by default
- [Layers](/docs/en/layers.md) Need more keys than switches? Use layers.
- [Split](/docs/en/split_keyboards.md) Connects halves using a wire.
- [Peg RGB](/docs/en/peg_rgb_matrix.md)
- [Display](/docs/en/display.md) Show information on the mini OLED display

## Microcontroller support

Replace `boardsource_blok` in `kb.py` to any supported microcontroller in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
