# Microdox

![microdox](https://boardsource.imgix.net/337ae65a-d061-46a4-b119-9916b043c58f.jpg?raw=true)

The Microdox is is a feature-packed 30% split columnar staggered keyboard. Even
though the Microdox is an extremely small keyboard it offers tons of features
from larger boards while maintaining a tiny footprint.

Retailers (USA)  
[Boardsource](https://boardsource.xyz/store/5f2e7e4a2902de7151494f92)  

Extensions enabled by default  
- [Layers](/docs/en/layers.md) Need more keys than switches? Use layers.
- [BLE_Split](/docs/en/split_keyboards.md) Connects halves without wires
- [HoldTap](/docs/en/holdtap.md) Allows mod keys to act as different keys when tapped.

Common Extensions
- [Split](/docs/en/split_keyboards.md) Connects halves using a wire
- [Power](/docs/enpower.md) Powersaving features for battery life

## Microcontroller support

Update this line in `kb.py` to any supported microcontroller in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
