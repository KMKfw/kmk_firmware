# ScottoInvader

![Top Shot](https://user-images.githubusercontent.com/8194147/196335152-13ac8c44-c60d-4d09-b559-eb24fc87e797.jpg)

Please see the [ScottoInvader](https://github.com/joe-scotto/scottokeebs/tree/main/ScottoInvader) GitHub page for details on how and what with to build this board.

# Microcontroller Support

In `kb.py` file, replace `boardsource_blok` in the following line with a supported microcontroller listed in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
