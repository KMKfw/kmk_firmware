# Dactyl ManuForm

![Wired ManuForm](https://i.imgur.com/7y0Vbyd.jpg)
*Two wired Dactyl ManuForm 4x6 variants*

![Wireless ManuForm](https://i.imgur.com/FpkRuCH.jpeg)
*Wireless Dactyl ManuForm 5x6 variant*

The [Dactyl ManuForm](https://github.com/tshort/dactyl-keyboard) is a handwired, split bodied, tented, curved keywell keyboard.  
Forked from the [Dactyl](/boards/dactyl) keyboard, the Dactyl ManuForm combines the thumb cluster from the [ManuForm](https://geekhack.org/index.php?topic=46015.0) keyboard (2013-07).  
Information for building this keyboard is found in first link.

## Variants

Dactyl ManuForms are built in variations that cater for different row and column counts, and thumb clusters.  
Variants are denoted as `RowCount`*x*`ColumnCount` and share the common configuration of:
- The finger keywell bottom row has 2 keys; 1 each in ring and middle columns.
    - Exception to this rule is the 7 column variants that have two additional keys in this row.
- The thumb cluster has 6 keys, arranged in 2 columns by 3 rows.

### Row
| Count | Description |
| --- | --- |
| 4 | Three rows, typically for alphabet and some punctuation characters, with 2 key (finger keywell) bottom row |
| 5 | As *4 rows* with number row above |
| 6 | As *5 rows* with function row above |

### Column
| Count | Description |
| --- | --- |
| 5 | A column for each finger with additional index finger column |  
| 6 | As *5 columns* with additional pinky finger column |
| 7 | As *6 columns* with either an additional index finger column (`5x7`) or additional pinky column (`6x7`) |

## Extended Bottom Row

Further to this board's customizable ethos, the bottom row of the finger keywell can be extended, outward, from the default two keys.

*Note: This does not apply to the `5x7` variant, as its bottom row is already extended*

To accommodate this, in files of chosen variant:
### `kb.py`  
`coord_mapping` element: Populate the extended row positions with numbers that continue numerical pattern of each half.  
e.g. in the case of `4x6` variant:
- `18, 19,` positions would be placed left of `20,` position.
- `52, 53,` positions would be placed right of `51,` position.

### `main.py`  
`keyboard.keymap` element: For each layer, append with keycodes in the respective extended bottom row positions.

## Case Files Generator

[Dactyl Generator](https://ryanis.cool/dactyl), created by [rianadon](https://github.com/rianadon), is a web based file generator that negates composing case files using a programming language, which was a requirement when using the GitHub repository for this board, by instead compiling case files based on options and parameters configured in a web front end.

## KMK Specifics

Extensions enabled by default:  
- [Layers](/docs/en/layers.md): As many as you want/need
- [Split](/docs/en/split_keyboards.md): Configured to 1-wire UART to match legacy configuration. Please see documentation for enabling 2-wire UART or, for capable controllers, Bluetooth.

## Microcontroller Support

If microcontrollers are not 0xCB Helios:  
Please amend `helios` in the following line of desired variant's `kb.py` file to supported microcontroller listed in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.helios import pinout as pins
```
For example, nice!nano controller(s): 
```python
from kmk.quickpin.pro_micro.nice_nano import pinout as pins
```
