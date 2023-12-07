# Keycodes Internacionais

A extensão internacional acrescenta teclas para teclados não-americanos. Ela
pode ser acrescentada à lista de exceções.

```python
from kmk.extensions.international import International
keyboard.extensions.append(International())
```

## Keycodes

| Tecla             | Alternativo | Descrição                        |
|-------------------|-------------|----------------------------------|
| `KC.NONUS_HASH`   | `KC.NUHS`   | Non-US `#` e `~`                 |
| `KC.NONUS_BSLASH` | `KC.NUBS`   | Non-US `\` e <code>&#124;</code> |
| `KC.INT1`         | `KC.RO`     | JIS `\` e <code>&#124;</code>    |
| `KC.INT2`         | `KC.KANA`   | JIS Katakana/Hiragana            |
| `KC.INT3`         | `KC.JYEN`   | JIS `¥`                          |
| `KC.INT4`         | `KC.HENK`   | JIS Henkan                       |
| `KC.INT5`         | `KC.MHEN`   | JIS Muhenkan                     |
| `KC.INT6`         |             | JIS Numpad `,`                   |
| `KC.INT7`         |             | 7 Internacional                  |
| `KC.INT8`         |             | 8 Internacional                  |
| `KC.INT9`         |             | 9 Internacional                  |
| `KC.LANG1`        | `KC.HAEN`   | Hangul/English                   |
| `KC.LANG2`        | `KC.HANJ`   | Hanja                            |
| `KC.LANG3`        |             | JIS Katakana                     |
| `KC.LANG4`        |             | JIS Hiragana                     |
| `KC.LANG5`        |             | JIS Zenkaku/Hankaku              |
| `KC.LANG6`        |             | Linguagem 6                      |
| `KC.LANG7`        |             | Linguagem 7                      |
| `KC.LANG8`        |             | Linguagem 8                      |
| `KC.LANG9`        |             | Linguagem 9                      |
