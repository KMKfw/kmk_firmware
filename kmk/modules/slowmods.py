'''Modifier keys designed to work over Remote Desktop/Hyper-V'''
from kmk.keys import KC, make_argumented_key
from kmk.modules import Module
from kmk.types import HoldTapKeyMeta

def slowmod_validator(kc, tap_time=None):
    return HoldTapKeyMeta(kc=kc, prefer_hold=False, tap_time=tap_time)

class SlowMods(Module):
    def __init__(self):
        self._shifted_numbers = range(KC.EXCLAIM.code, KC.QUESTION.code)
        make_argumented_key(
            validator=slowmod_validator,
            names=('SCTL',),
            on_press=self.slowmod_pressed,
            on_release=self.slowmod_released, 
            has_modifiers={KC.LCTL.code}
        )
        make_argumented_key(
            validator=slowmod_validator,
            names=('SSFT',),
            on_press=self.slowmod_pressed,
            on_release=self.slowmod_released, 
            has_modifiers={KC.LSFT.code}
        )
        make_argumented_key(
            validator=slowmod_validator,
            names=('SALT',),
            on_press=self.slowmod_pressed,
            on_release=self.slowmod_released, 
            has_modifiers={KC.LALT.code}
        )
        make_argumented_key(
            validator=slowmod_validator,
            names=('SGUI',),
            on_press=self.slowmod_pressed,
            on_release=self.slowmod_released, 
            has_modifiers={KC.LGUI.code}
        )
        make_argumented_key(
            validator=slowmod_validator,
            names=('SCS',),
            on_press=self.slowmod_pressed,
            on_release=self.slowmod_released, 
            has_modifiers={KC.LCTL.code, KC.LSFT.code, }
        )

    def code_to_key(self, code):
        mod_key = KC.NO 
        if code == KC.LCTL.code:
            mod_key = KC.LCTL
        elif code == KC.LSFT.code:
            mod_key = KC.LSFT
        elif code == KC.LALT.code:
            mod_key = KC.LALT
        elif code == KC.LGUI.code:
            mod_key = KC.LGUI
        else:
            raise ValueError('SlowMods code_to_key() tried to convert an invalid code to a key')
        return mod_key

    def slowmod_pressed(self, key, keyboard, *args, **kwargs):
        for mod in key.has_modifiers:
            keyboard.process_key(self.code_to_key(mod), True)
        keyboard._send_hid()
        keyboard.process_key(key.meta.kc, True)
        return keyboard

    def slowmod_released(self, key, keyboard, *args, **kwargs):
        keyboard.process_key(key.meta.kc, False)
        keyboard._send_hid()
        for mod in key.has_modifiers:
            keyboard.process_key(self.code_to_key(mod), False)
        return keyboard
    
    def process_key(self, keyboard, key, is_pressed, int_coord):
        if key.has_modifiers is not None:
            if KC.LSFT.code in key.has_modifiers:
                if key.code in self._shifted_numbers:
                    keyboard.process_key(KC.LSFT, is_pressed)
                    keyboard._send_hid()
        return key

    # Excluding this results in the error:
    # Failed to load module  <SlowMods object at 0x20009a50>
    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    #def matrix_detected_press(self, keyboard):
    #    return

    #def on_powersave_enable(self, keyboard):
    #    return

    #def on_powersave_disable(self, keyboard):
    #    return