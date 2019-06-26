# Examples
Here you can find some examples of what some users have created in their personal keyboard configs. These are here to
help you understand how some of the tools may be used.

## Changing LED color based on layers
This allows you to create a layer key that also changes colors when pushing a layer key, and restore turn off the lights
when you release the layer key. The example uses the MO though any layer switch keys can be used if imported. Just use the
LAYER_1 key in your keymap, and it's ready to go! You can change animations, colors, or anything in there.

```python
LAYER_1 = KC.MO(1)
LAYER_1.after_press_handler(lambda *args, **kwargs: keyboard.pixels.set_hsv_fill(100, 100, 100))
LAYER_1.after_release_handler(lambda *args, **kwargs: keyboard.pixels.set_hsv_fill(0, 0, 0))

keyboard.keymap = [ ....... LAYER_1 ....... ]
```