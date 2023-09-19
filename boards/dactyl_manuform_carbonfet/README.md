# Dactyl ManuForm Carbonfet
The [Dactyl ManuForm Carbonfet](https://github.com/carbonfet/dactyl-manuform) is a handwired, split bodied, tented, curved keywell keyboard.  
Forked from the [Dactyl ManuForm Mini](/boards/dactyl_manuform_mini), the Dactyl ManuForm Carbonfet appends the 5 key thumb cluster of the former with an additional key into a 2 row by 3 column arrangement.

![White](https://i.imgur.com/0ugz1C9.jpg)  
*Dactyl ManuForm Carbonfet 5x6 variant*

## Variants
Dactyl ManuForm Carbonfets are built in variations that cater for different row and column counts.  
Variants are denoted as `RowCount`*x*`ColumnCount` and share the common configuration of:
- The finger keywell bottom row has 2 keys; 1 each in ring and middle columns.
   Exception to this rule is the `5x7` variant that has two additional keys in this row.
- The thumb cluster has 5 keys: 2 (row) x 3 (column) arrangement with bottom left position omitted for left half, this arrangement mirrored for right half.

### Row
| Count | Description                                                                                                                |
| ----- | -------------------------------------------------------------------------------------------------------------------------- |
|     4 | Three rows, typically for alphabet and some punctuation characters, with two keys in bottom row of finger keywell section |
|     5 | As *4 rows* with number row above                                                                                          |
|     6 | As *5 rows* with function row above                                                                                        |

### Column
| Count | Description                                                                                             |
| ----- | ------------------------------------------------------------------------------------------------------- |
|     5 | A column for each finger with additional index finger column                                            |
|     6 | As *5 columns* with additional pinky finger column                                                      |
|     7 | As *6 columns* with either an additional index finger column (`5x7`) or additional pinky column (`6x7`) |

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

## KMK Specifics
Extensions enabled by default:  
- [Layers](/docs/en/layers.md)
- [Split](/docs/en/split_keyboards.md): Configured to 1-wire UART to match legacy configuration. Please see documentation for enabling 2-wire UART or, for capable controllers, Bluetooth.

## Microcontroller support
Replace `boardsource_blok` in variant's `kb.py` to a supported microcontroller in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
