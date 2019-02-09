OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255, 0)
PURPLE = (180, 0, 255)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def color_chase(pixels, num_pixels, color, color2=OFF, speed=100, animation_state=0):
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


def rainbow_cycle(pixels, num_pixels, speed=100, animation_state=0, color_state=0):
    color_state += 1
    if color_state in range(255):
        print(animation_state)
        animation_state +=1
        if animation_state in range(num_pixels):
            rc_index = (animation_state * 256 // num_pixels) + animation_state
            print(pixels[animation_state])
            print(wheel(rc_index & 255))
            pixels[animation_state] = wheel(rc_index & 255)
        else:
            pixels.show()
            return 0, color_state
    else:
        return animation_state, 0



