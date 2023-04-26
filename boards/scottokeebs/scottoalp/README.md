# ScottoAlp

![TopShot](https://user-images.githubusercontent.com/8194147/193963094-ce0f174d-f67c-4a15-81d4-05b264ef2b11.jpg)

Please see the [ScottoAlp](https://github.com/joe-scotto/scottokeebs/tree/main/ScottoAlp) GitHub page for details on how and what with to build this board

# Microcontroller Support

In `kb.py` file, replace `boardsource_blok` in the following line with a supported microcontroller listed in `kmk/quickpin/pro_micro`:

```python
from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
```
