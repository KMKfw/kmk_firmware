def test_neopixel(micropython, neopixel):
    from kmk.rgb import RGB, rgb_config

    rgb_config.update({'num_pixels': 16})

    rgb = RGB(rgb_config, 1)
    assert neopixel.NeoPixel.called_once_with(
        1, rgb_config['num_pixels'], rgb_config['rgb_order'], auto_write=False
    )

    rgb.set_rgb((255, 0, 0), 0)
    rgb.show()


def test_apa102_dotstar(micropython, digitalio):
    from kmk.leds.apa102 import RGB
    from kmk.rgb import rgb_config

    rgb_config.update({'num_pixels': 16})

    rgb = RGB(rgb_config, (1, 2))

    rgb.set_rgb((255, 0, 0), 0)
    rgb.show()
