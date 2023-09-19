# Dactyl Maximus

![KeycapLess](https://i.imgur.com/OJs3bkWh.jpg)  
*Thanks to [unit-5370](https://github.com/unit-5370) for image*

The largest key count [Dactyl](/boards/dactyl/) variation available from a Dactyl generator; 7 columns with an 8 key thumb cluster.

Hardware Availability: [Dactyl Generator](https://ryanis.cool/dactyl/#original)
* 'Keys' settings:
   * Number of Columns: 7 
   * Use Number Row: true
   * Use Bottom Row: true
   * Thumb Key Count: 8

## KMK Specifics

Extensions enabled by default  
- [Layers](/docs/en/layers.md)
- [Split](/docs/en/split_keyboards.md): Configured to 1-wire UART to match legacy configuration. Please see documentation for enabling 2-wire UART or, for capable controllers, Bluetooth

## Microcontroller support

Replace `kb2040` in the following line of `kb.py` to a supported microcontroller listed in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.kb2040 import pinout as pins
```
