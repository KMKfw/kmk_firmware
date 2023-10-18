# Reviung34

The Reviung34 is a 34 key keyboard designed by gtips, it is a slightly smaller
version of the popular Reviung 39. These "split non-split" keyboards offer a lot
of features split keyboards have in terms of comfort and ergonomics but do so in
a single-piece package. Many people consider keyboards in this style easier to
travel with since you don't have to manage two halves and there is of course no
need for a TRRS cable. This board sits somewhere between and Atreus and Corne,
and it is extremely comfortable to use.

Hardware Availability: [PCB & Case Data](https://github.com/gtips/reviung/tree/master)

Extensions enabled by default
- [Layers](/docs/en/layers.md) Need more keys than switches? Use layers.
- [RGB matrix](/docs/en/peg_rgb_matrix.md) Light it up

## Microcontroller support

Update this line in `kb.py` to any supported microcontroller in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
