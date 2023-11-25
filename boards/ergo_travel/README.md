# Ergo Travel

![ergo_travel](https://boardsource.imgix.net/fa53de62-fd37-4c75-8c5b-b4bec37927c1.jpg?raw=true)

As the name implies, the Ergo Travel was originally designed as a travel
keyboard, but it works just as well on your desk as a main daily use keyboard.
The Ergo Travel is a popular choice by many because it offers a few more keys
than other keyboards in similar sizes, and that is why we chose to stock it.
Additionally, the Ergo Travel has nice customization options in the thumb
cluster because you can configure the main thumb key to use a single larger 2u
key, or two smaller 1u keys depending on your preference. The clean and simple
aesthetic of the Ergo Travel and the few extra keys make it an awesome option
for people wanting a 40%-ish split keyboard.

Hardware Availability: [PCB & Case Source](https://github.com/jpconstantineau/ErgoTravel/blob/master/OrderingInstructions.md)  

Extensions enabled by default  
- [Layers](/docs/en/layers.md) Need more keys than switches? Use layers.
- [BLE_Split](/docs/en/split_keyboards.md) Connects halves without wires
- [MediaKeys](/docs/en/media_keys.md) Control volume and other media functions

Common Extensions
- [Split](/docs/en/split_keyboards.md) Connects halves using a wire
- [Power](/docs/en/power.md) Powersaving features for battery life


## Microcontroller support

Update this line in `kb.py` to any supported microcontroller in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
