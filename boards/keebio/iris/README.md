# Iris Rev 2

A split keyboard with a 4x6 layout with additional 4 thumb buttons

kb_converter.py is designed to work with an itsybitsy with converter board found [here](/hardware)

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
