# What's this?
# This is a keycode conversion script. With this, KMK will work as a JIS keyboard.

# Usage
# ```python
# import kmk.extensions.keymap_extras.keymap_jp
# ```

from kmk.keys import KC

KC.CIRC = KC.EQL  # ^
KC.AT = KC.LBRC  # @
KC.LBRC = KC.RBRC  # [
KC.EISU = KC.CAPS  # Eisū (英数)
KC.COLN = KC.QUOT  # :
KC.LCBR = KC.LSFT(KC.RBRC)  # {
KC.RBRC = KC.NUHS  # ]
KC.BSLS = KC.INT1  # (backslash)
KC.PLUS = KC.LSFT(KC.SCLN)
KC.TILD = KC.LSFT(KC.EQL)  # ~
KC.GRV = KC.LSFT(KC.AT)  # `
KC.DQUO = KC.LSFT(KC.N2)  # "
KC.AMPR = KC.LSFT(KC.N6)  # &
KC.ASTR = KC.LSFT(KC.QUOT)  # *
KC.QUOT = KC.LSFT(KC.N7)  # '
KC.LPRN = KC.LSFT(KC.N8)  # (
KC.RPRN = KC.LSFT(KC.N9)  # )
KC.EQL = KC.LSFT(KC.MINS)  # =
KC.PIPE = KC.LSFT(KC.INT3)  # |
KC.RCBR = KC.LSFT(KC.NUHS)  # }
KC.LABK = KC.LSFT(KC.COMM)  # <
KC.RABK = KC.LSFT(KC.DOT)  # >
KC.QUES = KC.LSFT(KC.SLSH)  # ?
KC.UNDS = KC.LSFT(KC.INT1)  # _
