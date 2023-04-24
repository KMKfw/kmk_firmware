# Dactyl ManuForm Mini

The [Dactyl ManuForm Mini](https://github.com/l4u/dactyl-manuform-mini-keyboard) is a fork of [Dactyl ManuForm](https://github.com/tshort/dactyl-keyboard); this fork replaces the 6 thumb cluster of the latter with a 5 key thumb cluster

![BlackGrey](https://i.imgur.com/76hbOkBl.jpg)  
*Dactyl Manuform Mini 5x6 variant*  
![Lp_Wider6thC](https://preview.redd.it/uzyygioqvek61.jpg?width=640&crop=smart&auto=webp&v=enabled&s=7a0fb7e3a89f51524e4c8d43d9ea1f2ee4d2537a)  
*5x6 variant with Choc (Low Profile) switches and accompanying keycaps, and wider 1.5u outer pinky column*  

## Variants

Dactyl Manuform Mini's are built in variations that cater for different row and column counts.  
Variants are denoted as `RowCount`*x*`ColumnCount` and share the common configuration of:
- The finger key-well bottom row has 2 keys; 1 each in ring and middle columns.
    - Exception to this rule is the 7 column variants that have two additional keys in this row.
- The thumb cluster has 5 keys; 2 (row) x 3 (column) arrangement with bottom left position ommited for left half, this arrangment mirrored for right half.

### Row
| Count | Description |
| --- | --- |
| 4 | Three rows, typically for alphabet and some punctuation characters, with 2 key (finger keywell) bottom row |
| 5 | Like *4 rows* with number row above |
| 6 | Like *5 rows* with function row above |

### Column
| Count | Description |
| --- | --- |
| 5 | A column for each finger with additiona index finger column |  
| 6 | Like *5 columns* with additional pinky finger column |
| 7 | Like *6 columns* with either an additional index finger column (`5x7`) or additional pinky column (`6x7`) |

## KMk Specifics

Extentions enabled by default:  
- [Layers](/docs/en/layers.md)
- [Split](/docs/en/split_keyboards.md): Configured to 1-wire UART to match legacy configuration. Please see documentation for enabling 2-wire UART or, for capable controllers, Bluetooth.

## Microcontroller support

Replace `boardsource_blok` in variant's `kb.py` to a supported microcontroller in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
