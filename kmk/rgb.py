from math import sin, exp, pi
import time

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
        'pos': 0,
        'timer': None,
        'intervals': (0, 0, 0, 0),
        'speed': 120,  # Bigger is slower
        'enable': True
    }


def time_ms():
    return time.monotonic_ns() / 10


def hsv_to_rgb(hue, sat, val):
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

    return r, g, b


def set_hsv(hue, sat, val, pixels, index):
    set_rgb(hsv_to_rgb(hue, sat, val), pixels, index)


def set_hsv_fill(hue, sat, val, pixels):
    pixels.fill(hsv_to_rgb(hue, sat, val))
    pixels.show()


def set_rgb(rgb, pixels, index):
    pixels[index] = (rgb[0], rgb[1], rgb[2])
    pixels.show()


def set_rgb_fill(rgb, pixels):
    pixels.fill(rgb[0], rgb[1], rgb[2])
    pixels.show()


def increase_hue(hue, step):
    return hue + step % 360


def decrease_hue(hue, step):
    if hue - step < 0:
        return (hue + 360 - step) % 360
    else:
        return hue - step % 360


def animate(state, pixels):
    if state['animation_mode'] == 'breathing':
        return effect_breathing(state, pixels)
    elif state['animation_mode'] == 'rainbow':
        return effect_rainbow(state, pixels)

    return state


def animation_step(state):
    interval = state['time'] - time_ms()
    if interval in state['intervals']:
        return interval
    else:
        return False


def effect_breathing(state, pixels):
    if animation_step(state):
        # http://sean.voisen.org/blog/2011/10/breathing-led-with-arduino/
        state['v'] = (exp(sin(state['step'] / 2000.0 * pi)) - 0.36787944) * 108.0
        set_hsv_fill(state['h'], state['s'], state['v'], pixels)

    return state


def effect_rainbow(state, pixels):
    if animation_step(state):
        state['h'] = increase_hue(state['h'], 1)
        set_hsv_fill(state['h'], state['s'], state['v'], pixels)

    return state


def effect_rainbow_swirl(state, pixels):
    interval = animation_step(state)
    if interval:
        MAX_RGB_NUM = 12  # TODO Actually pass this
        for i in range(0, MAX_RGB_NUM):
            state['h'] = (360 / MAX_RGB_NUM * i + state['h']) % 360
            set_hsv_fill(state['h'], state['s'], state['v'], pixels)

    if interval % 2:
        state['h'] = increase_hue(state['h'], 1)
    else:
        state['h'] = decrease_hue(state['h'], 1)

    return state
