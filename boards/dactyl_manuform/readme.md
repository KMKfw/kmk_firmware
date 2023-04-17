# Dactyl Manuform

The [Dactyl Manuform](https://github.com/tshort/dactyl-keyboard) is a handwired, split bodied, tented, curved keywell keyboard - adapted from the [Dactyl](https://github.com/adereth/dactyl-keyboard) keyboard with the thumb cluster design of the [ManuForm](https://geekhack.org/index.php?topic=46015.0) keyboard. Information for building a Dactyl Manuform found in first link.

![Imgur](https://i.imgur.com/7y0Vbyd.jpg)
*Two wired Dactyl Manuform 4x6 variants*

## Variants

Dactyl Manuform's are built in variations that cater for different row and column counts, and thumb clusters.  

As standard: 
- The finger keywell bottom row has 2 keys, 1 each in ring and middle columns
    - Exception to this rule is the 7 column variants, that have two additional keys in this row
- The thumb cluster has 6 keys, arranged in 2 columns by 3 rows 

Variants are denoted as `RowCount`*x*`ColumnCount`

### Row
| Count | Description |
| --- | --- |
| 4 | Three rows, typically for alphabet and some puncuation characters, with 2 key (finger keywell) bottom row |
| 5 | As *4 row* with number row above |
| 6 | As *5 row* with function row above |

### Column
| Count | Description |
| --- | --- |
| 5 | A column for each finger with additional column for first finger |  
| 6 | As *5 column* with additional pinky finger column |
| 7 | As *6 column* with additional first finger column |

## Microcontroller support

Amend `controller` in the following line of desired variant's `kb.py` file to supported microcontroller listed in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.controller import pinout as pins
```
For example, nice!nano controller(s): 
```python
from kmk.quickpin.pro_micro.nice_nano import pinout as pins
```

## KMK Specifics

Extentions enabled by default:  
- [Layers](/docs/en/layers.md): As many as you want/need
- [Split](/docs/en/split_keyboards.md): Configured to 1 wire UART to match legacy configuration. Please see documentation for enabling 2 wire UART or bluetooth, for capable controllers
