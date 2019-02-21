from math import sin, exp, pi, floor
from math import e as M_E
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
        'h': 180,
        's': 100,
        'v': 80,
        'animation_mode': 'Breathing',
        'pos': 0,
        'time': time_ms(),
        'intervals': (30, 20, 10, 5),
        'speed': 120,  # Bigger is slower
        'enable': True
    }


def time_ms():
    return floor(time.monotonic() * 10)


def hsv_to_rgb(hue, sat, val):
    r = 0
    g = 0
    b = 0
    RGBLIGHT_LIMIT_VAL = 255

    if val > 255:
        val = 255

    if sat == 0:
        r = val
        g = val
        b = val

    else:
        base = ((255 - sat) * val) >> 8
        color = (val - base) * (hue % 60) / 60

        x = floor(hue / 60)
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

    return floor(r), floor(g), floor(b)


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
    return (hue + step) % 360


def decrease_hue(hue, step):
    if hue - step < 0:
        return (hue + 360 - step) % 360
    else:
        return (hue - step) % 360


def off(pixels):
    set_hsv_fill(0, 0, 0, pixels)


def animate(state, pixels):
    if state['enable']:
        if state['animation_mode'] == 'breathing':
            return effect_breathing(state, pixels)
        elif state['animation_mode'] == 'rainbow':
            return effect_rainbow(state, pixels)
    else:
        off(pixels)

    return state


def animation_step(state):
    interval = time_ms() - state['time']
    if interval >= max(state['intervals']):
        state['time'] = time_ms()
        return max(state['intervals'])
    if interval in state['intervals']:
        return interval
    else:
        return False


def effect_breathing(state, pixels):
    RGBLIGHT_EFFECT_BREATHE_CENTER = 1.5  # 1.0-2.7
    RGBLIGHT_EFFECT_BREATHE_MAX = 150  # 0-255
    interval = time_ms() - state['time']
    # http://sean.voisen.org/blog/2011/10/breathing-led-with-arduino/
    # https://github.com/qmk/qmk_firmware/blob/9f1d781fcb7129a07e671a46461e501e3f1ae59d/quantum/rgblight.c#L787
    state['v'] = floor((exp(sin((state['pos']/255.0)*pi)) - RGBLIGHT_EFFECT_BREATHE_CENTER/M_E)*(RGBLIGHT_EFFECT_BREATHE_MAX/(M_E-1/M_E)))
    state['pos'] = (state['pos'] + 1) % 256;
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
