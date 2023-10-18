# Dactyl ManuForm Mini

The [Dactyl ManuForm Mini](https://github.com/l4u/dactyl-manuform-mini-keyboard) is a handwired, split bodied, tented, curved keywell keyboard.  
Forked from the [Dactyl ManuForm](/boards/dactyl_manuform), the Dactyl ManuForm Mini replaces the 6 thumb cluster of the former with a 5 key thumb cluster.  

![Black-Grey](https://i.imgur.com/76hbOkBl.jpg)  
*Dactyl ManuForm Mini 5x6 variant*  
![Choc](https://preview.redd.it/uzyygioqvek61.jpg?width=640&crop=smart&auto=webp&v=enabled&s=7a0fb7e3a89f51524e4c8d43d9ea1f2ee4d2537a)  
*5x6 variant with Choc switches and keycaps, and wider 1.5u outer pinky column*  

## Variants

Dactyl ManuForm Mini's are built in variations that cater for different row and column counts.  
Variants are denoted as `RowCount`*x*`ColumnCount` and share the common configuration of:
- The finger keywell bottom row has 2 keys; 1 each in ring and middle columns.
    - Exception to this rule is the `5x7` variant that has two additional keys in this row.
- The thumb cluster has 5 keys: 2 (row) x 3 (column) arrangement with bottom left position omitted for left half, this arrangement mirrored for right half.

### Row
| Count | Description |
| --- | --- |
| 4 | Three rows, typically for alphabet and some punctuation characters, with two keys in bottom row of finger keywell section |
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
- [Layers](/docs/en/layers.md)
- [Split](/docs/en/split_keyboards.md): Configured to 1-wire UART to match legacy configuration. Please see documentation for enabling 2-wire UART or, for capable controllers, Bluetooth.

## Microcontroller support

Replace `boardsource_blok` in variant's `kb.py` to a supported microcontroller in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
