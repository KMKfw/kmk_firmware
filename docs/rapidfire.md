# RapidFire

The RapidFire module lets a user send repeated key presses while a key is held.

Some instances where this may be useful are:

- MMOs and other games where you are encouraged to repeatedly spam a key
- More responsive volume up and volume down
- Faster cursor key navigation
- Combine with the [Mouse Keys](https://github.com/KMKfw/kmk_firmware/blob/master/docs/mouse_keys.md) module to create rapid-fire mouse clicks
- Anywhere else you may need an ergonomic alternative to repetitive key tapping

## Keycodes

| Key     | Description                                          |
| :------ | :--------------------------------------------------- |
| `KC.RF` | Repeatedly sends the specified keycode while pressed |

## Usage

Each repeat counts as one full cycle of pressing and releasing. RapidFire works with chording (i.e., holding Shift plus a RapidFire key will repeatedly send the shifted version of that RapidFire key) and chaining (i.e., `KC.RF(KC.LSHIFT(KC.A))`. Multiple RapidFire keys can be held down at the same time, and their timers work independently of each other.

The RapidFire keycode has a few different options:

|        Option         | Default Value | Description                                                                                                                                        |
| :-------------------: | :-----------: | :------------------------------------------------------------------------------------------------------------------------------------------------- |
|       `repeat`        |     `100`     | The delay between repeats. Note: `2` appears to be the minimum effective value. If you run into issues, try increasing this value.                 |
|        `wait`         |     `200`     | The delay before starting to repeat. Useful if you want to be able to type with keys that have a low `repeat` value.                               |
|  `randomize_repeat`   |    `False`    | Randomize the value of `repeat`. Useful for making the repetitive input look human in instances where you may be flagged as a bot otherwise.       |
| `randomize_magnitude` |     `15`      | The magnitude of the randomization. If randomization is enabled, the repeat delay will be `repeat` plus or minus a random value up to this amount. |
|       `toggle`        |    `False`    | Toggle RapidFire state on keypress rather than needing to be held. Toggle functionality starts after the `wait` period.                            |

### Example Code

```python
from kmk.modules.rapidfire import RapidFire

keyboard.modules.append(RapidFire())

# After 200 milliseconds, repeatedly send Shift+A every 75-125 milliseconds until the button is pressed again
keyboard.keymap = [[
    KC.RF(KC.LSFT(KC.A), wait=200, repeat=100, randomize_repeat=True, randomize_magnitude=25, toggle=True)
    ]]

```
