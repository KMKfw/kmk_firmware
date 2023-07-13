from kmk.modules.holdtap import HoldTap
from kmk.keys import KC


#SPC_FN = KC.HT(KC.SPC, KC.MO(1))
SPC_FN = KC.HT(KC.SPC, KC.MO(1))
# LCTL = KC.HT(KC.SOMETHING, KC.LCTRL)	                     #   LCTRL if held kc if tapped
# LSFT = KC.HT(KC.SOMETHING, KC.LSFT)	                     #   LSHIFT if held kc if tapped
# LALT = KC.HT(KC.SOMETHING, KC.LALT)	                     #   LALT if held kc if tapped
# LGUI = KC.HT(KC.SOMETHING, KC.LGUI)	                     #   LGUI if held kc if tapped
# RCTL = KC.HT(KC.SOMETHING, KC.RCTRL)	                     #   RCTRL if held kc if tapped
# RSFT = KC.HT(KC.SOMETHING, KC.RSFT)	                     #   RSHIFT if held kc if tapped
# RALT = KC.HT(KC.SOMETHING, KC.RALT)	                     #   RALT if held kc if tapped
# RGUI = KC.HT(KC.SOMETHING, KC.RGUI)	                     #   RGUI if held kc if tapped
# SGUI = KC.HT(KC.SOMETHING, KC.LSHFT(KC.LGUI))	         #   LSHIFT and LGUI if held kc if tapped
# LCA  = KC.HT(KC.SOMETHING, KC.LCTRL(KC.LALT))	         #   LCTRL and LALT if held kc if tapped
# LCAG = KC.HT(KC.SOMETHING, KC.LCTRL(KC.LALT(KC.LGUI)))	 #   LCTRL and LALT and LGUI if held kc if tapped
# MEH  = KC.HT(KC.SOMETHING, KC.LCTRL(KC.LSFT(KC.LALT)))	 #   CTRL and LSHIFT and LALT if held kc if tapped
# HYPR = KC.HT(KC.SOMETHING, KC.HYPR)                       #	LCTRL and LSHIFT and LALT and LGUI if held kc if tapped