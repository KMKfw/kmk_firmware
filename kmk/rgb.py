COLORS = {
    'OFF': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255, 0),
    'YELLOW': (255, 150, 0),
    'CYAN': (0, 255, 255),
    'PURPLE': (180, 0, 255),
    'WHITE': (255, 255, 255),
}


def pixelinit():
    return {
        'h': 0,
        's': 255,
        'v': 255,
        'animation_mode': None,
        'speed': 0,
        'enable': True
    }


def color_chase(pixels, num_pixels, color, color2=COLORS['OFF'], speed=100, animation_state=0):
    if animation_state not in range(num_pixels):
        color = color2
        pixels[int(animation_state - num_pixels)] = color

    else:
        pixels[animation_state] = color

    pixels.show()
    animation_state += 1

    if animation_state >= num_pixels * 2:
        animation_state = 0

    return animation_state, 0


def sethsv(hue, sat, val, pixels, index):
    r = 0
    g = 0
    b = 0
    # TODO Actually pass this limit to allow overrides
    RGBLIGHT_LIMIT_VAL = 255

    if val > RGBLIGHT_LIMIT_VAL:
      val=RGBLIGHT_LIMIT_VAL

    if sat == 0:
        r = val
        g = val
        b = val

    else:
        base = ((255 - sat) * val) >> 8
        color = (val - base) * (hue % 60) / 60

    x = hue / 60
    if x == 0:
        r = val
        g = base + color
        b = base
    elif x == 1:
        r = val - color
        g = val
        b = base
    elif x == 2:
        r = base
        g = val
        b = base + color
    elif x == 3:
        r = base
        g = val - color
        b = val
    elif x == 4:
        r = base + color
        g = base
        b = val
    elif x == 5:
        r = val
        g = base
        b = val - color

    rgb = (r, g, b)
    setrgb(rgb, pixels, index)


def setrgb(rgb, pixels, index):
    pixels[index] = (rgb[0], rgb[1], rgb[2])


def setrgbfill(rgb, pixels):
    pixels.fill(rgb[0], rgb[1], rgb[2])


def increasehue(hue, step):
    return hue + step % 360


def decreasehue(hue, step):
    if hue - step < 0:
        return (hue + 360 - step) % 360
    else:
        return hue - step % 360

