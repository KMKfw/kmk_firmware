# Reviung41

![Reviung41](https://boardsource.imgix.net/ea77f3f8-6cc4-4cb4-a801-cf58b5af8fcc.jpg?raw=true)

The Reviung41 is a 41 key keyboard designed by gtips, it is a slightly larger
version of the popular Reviung 39. These "split non-split" keyboards offer a lot
of features split keyboards have in terms of comfort and ergonomics but do so in
a single-piece package. Many people consider keyboards in this style easier to
travel with since you don't have to manage two halves and there is of course no
need for a TRRS cable. This board sits somewhere between and Atreus and Corne,
and it is extremely comfortable to use.

Hardware Availability: [PCB & Case Data](https://github.com/gtips/reviung/tree/master/reviung41)

Retailers (USA)  
[Boardsource](https://boardsource.xyz/store/5f2ef1b52bf5e8714a60f613)  

Extensions enabled by default  
- [Layers](/docs/en/layers.md) Need more keys than switches? Use layers.
- [RGB](/docs/en/rgb.md) Light it up
- [HoldTap](/docs/en/holdtap.md) Allows mod keys to act as different keys when tapped.

Common Extensions
- [Power](/docs/en/power.md) Powersaving features for battery life

## Microcontroller support

Update this line in `kb.py` to any supported microcontroller in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
