# ScottoAlp

![Top Shot](https://user-images.githubusercontent.com/8194147/193963346-4ea0b40f-e1c6-48a5-aed3-ec57282a3b16.jpg)

Please see the [ScottoAlp](https://github.com/joe-scotto/scottokeebs/tree/main/ScottoAlp) GitHub page for details on how and what with to build this board.

# Microcontroller Support

In `kb.py` file, replace `boardsource_blok` in the following line with a supported microcontroller listed in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
