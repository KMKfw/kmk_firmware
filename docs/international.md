# International Keycodes
International extension adds keys for non US layouts. It can simply be added to 
the extensions list.

```python
from kmk.extensions.international import International
keyboard.extensions.append(International())
```

## Keycodes

|Key                    |Aliases             |Description                                    |
|-----------------------|--------------------|-----------------------------------------------|
|`KC.NONUS_HASH`        |`KC.NUHS`           |Non-US `#` and `~`                             |
|`KC.NONUS_BSLASH`      |`KC.NUBS`           |Non-US `\` and <code>&#124;</code>             |
|`KC.INT1`              |`KC.RO`             |JIS `\` and <code>&#124;</code>                |
|`KC.INT2`              |`KC.KANA`           |JIS Katakana/Hiragana                          |
|`KC.INT3`              |`KC.JYEN`           |JIS `¥`                                        |
|`KC.INT4`              |`KC.HENK`           |JIS Henkan                                     |
|`KC.INT5`              |`KC.MHEN`           |JIS Muhenkan                                   |
|`KC.INT6`              |                    |JIS Numpad `,`                                 |
|`KC.INT7`              |                    |International 7                                |
|`KC.INT8`              |                    |International 8                                |
|`KC.INT9`              |                    |International 9                                |
|`KC.LANG1`             |`KC.HAEN`           |Hangul/English                                 |
|`KC.LANG2`             |`KC.HANJ`           |Hanja                                          |
|`KC.LANG3`             |                    |JIS Katakana                                   |
|`KC.LANG4`             |                    |JIS Hiragana                                   |
|`KC.LANG5`             |                    |JIS Zenkaku/Hankaku                            |
|`KC.LANG6`             |                    |Language 6                                     |
|`KC.LANG7`             |                    |Language 7                                     |
|`KC.LANG8`             |                    |Language 8                                     |
|`KC.LANG9`             |                    |Language 9                                     |


