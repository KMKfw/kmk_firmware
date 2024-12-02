# ScottoSlant

![Top Shot](https://user-images.githubusercontent.com/8194147/192114474-df9b38e6-ece1-4d7f-81fb-bbc910054847.jpg)

Please see the [ScottoSlant](https://github.com/joe-scotto/scottokeebs/tree/main/ScottoSlant) GitHub page for details on how and what with to build this board.

# Microcontroller Support

In `kb.py` file, replace `boardsource_blok` in the following line with a supported microcontroller listed in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
