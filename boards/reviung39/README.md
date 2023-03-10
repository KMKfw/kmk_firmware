# Reviung39

![Reviung39](https://boardsource.imgix.net/d6215164-6100-4b72-b355-1a67b7704463.jpg?raw=true)

Reviung39 is a 39 key keyboard designed by gtips. The Reviung39 sits somewhere
between an Atreus and a Corne, you get some nice ergonomic benefits based on its
quasi-split design and since a true split keyboard isn't for everyone, this is
an awesome middle ground. I find this keyboard extremely comfortable to use.

kb.py is designed to work with the nice!nano

Hardware Availability: [PCB & Case Data](https://github.com/gtips/reviung)  

Retailers (USA)  
[Boardsource](https://boardsource.xyz/store/5ecb734486879c9a0c22dab3)  

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
```
