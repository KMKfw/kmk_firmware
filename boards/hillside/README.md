# Hillside

Boards in the [Hillside](https://github.com/mmccoyd/hillside) family are [40%](https://deskthority.net/wiki/40%25) sized, split bodied with a [column-stagger](https://deskthority.net/wiki/Staggering#Columnar_layout).  
Hillside boards are only suitable for choc v1 switches and keycaps based on an 18 x 17mm switch spacing.


| Splayed | Non-Splayed |
| :---: | :---: |
| [Hillside 46](https://github.com/mmccoyd/hillside/tree/main/hillside46) <br> ![Hillside 46](https://github.com/mmccoyd/hillside/wiki/image/46/hill46_photo_600.png) | [Hillside 48](https://github.com/mmccoyd/hillside/tree/main/hillside48) <br> ![Hillside 48](https://github.com/mmccoyd/hillside/wiki/image/48/hill48_600.png) |
| [Hillside 52](https://github.com/mmccoyd/hillside/tree/main/hillside52) <br> ![Hillside 52](https://github.com/mmccoyd/hillside/wiki/image/52/hill52_photo_600.png) | [Hillside 56](https://github.com/mmccoyd/hillside/tree/main/hillside56) <br> ![Hillside 56](https://github.com/mmccoyd/hillside/wiki/image/family/hill56_600.png) |

Their specific differences are:
| Type | Board      | Layout  | Arrow <br> T | Encoder <br> Spots / Side | Hotswap <br> Option| Trimmed <br> Layout | Trimmed <br> Keys |
|:------------|:--------:|:--------|:----:|:----:|:-------:|:--------|:--:|
| Splayed     | [46](46) | 3x6+0+5 | no   | 2    | yes     | 3x5+0+5 | 40 |
|             | [52](52) | 3x6+3+5 | yes  | 3    | yes     | 3x5+2+5 | 44 |
| Non-Splayed | [48](48) | 3x6+1+5 | no   | 1    | no      | 3x5+1+5 | 42 |
|             | [56](56) | 3x6+5+5 | yes  | 4    | yes     | 3x5+4+5 | 48 |

## KMK Specifics

Extensions & modules enabled by default:  
- [Layers](/docs/en/layers.md)
- [Split](/docs/en/split_keyboards.md): Configured to 1-wire UART to match legacy configuration. Please see documentation for enabling 2-wire UART or, for capable controllers, Bluetooth
- [RGB](/docs/en/rgb.md)
- [MediaKeys](/docs/en/media_keys.md)
- [CgSwap](/docs/en/cg_swap.md)
- [StickyKeys](/docs/en/sticky_keys.md)
- [CapsWord](/docs/en/capsword.md)

## Microcontroller support

In `kb.py` file, replace `boardsource_blok` with any supported microcontroller listed in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
