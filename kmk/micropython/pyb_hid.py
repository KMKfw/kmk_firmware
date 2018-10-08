from pyb import USB_HID, delay, hid_keyboard

from kmk.common.abstract.hid import AbstractHidHelper
from kmk.common.consts import HID_REPORT_STRUCTURE


def generate_pyb_hid_descriptor():
    existing_keyboard = list(hid_keyboard)
    existing_keyboard[-1] = HID_REPORT_STRUCTURE
    return tuple(existing_keyboard)


class HIDHelper(AbstractHidHelper):
    # For some bizarre reason this can no longer be 8, it'll just fail to send
    # anything. This is almost certainly a bug in the report descriptor sent
    # over in the boot process. For now the sacrifice is that we only support
    # 5KRO until I figure this out, rather than the 6KRO HID defines.
    REPORT_BYTES = 7

    def post_init(self):
        self._hid = USB_HID()
        self.hid_send = self._hid.send

    def send(self):
        self.logger.debug('Sending HID report: {}'.format(self._evt))
        self.hid_send(self._evt)

        # Without this delay, events get clobbered and you'll likely end up with
        # a string like `heloooooooooooooooo` rather than `hello`. This number
        # may be able to be shrunken down. It may also make sense to use
        # time.sleep_us or time.sleep_ms or time.sleep (platform dependent)
        # on non-Pyboards.
        #
        # It'd be real awesome if pyb.USB_HID.send/recv would support
        # uselect.poll or uselect.select to more safely determine when
        # it is safe to write to the host again...
        delay(5)

        return self
