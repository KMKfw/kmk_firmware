import logging
from collections import namedtuple

from micropython import const

from kmk.common.keycodes import Keycodes
from kmk.common.util import reset_bootloader

KEY_UP_EVENT = const(1)
KEY_DOWN_EVENT = const(2)
INIT_FIRMWARE_EVENT = const(3)
NEW_MATRIX_EVENT = const(4)
HID_REPORT_EVENT = const(5)
KEYCODE_UP_EVENT = const(6)
KEYCODE_DOWN_EVENT = const(7)
MACRO_COMPLETE_EVENT = const(8)
PENDING_KEYCODE_POP_EVENT = const(9)

logger = logging.getLogger(__name__)


InitFirmware = namedtuple('InitFirmware', (
    'type',
    'keymap',
    'row_pins',
    'col_pins',
    'diode_orientation',
    'unicode_mode',
))

KeyUpDown = namedtuple('KeyUpDown', ('type', 'row', 'col'))
KeycodeUpDown = namedtuple('KeycodeUpDown', ('type', 'keycode'))
NewMatrix = namedtuple('NewMatrix', ('type', 'matrix'))
BareEvent = namedtuple('BareEvent', ('type',))


def init_firmware(keymap, row_pins, col_pins, diode_orientation, unicode_mode):
    return InitFirmware(
        type=INIT_FIRMWARE_EVENT,
        keymap=keymap,
        row_pins=row_pins,
        col_pins=col_pins,
        diode_orientation=diode_orientation,
        unicode_mode=unicode_mode,
    )


def key_up_event(row, col):
    return KeyUpDown(
        type=KEY_UP_EVENT,
        row=row,
        col=col,
    )


def key_down_event(row, col):
    return KeyUpDown(
        type=KEY_DOWN_EVENT,
        row=row,
        col=col,
    )


def keycode_up_event(keycode):
    '''
    Press a key by Keycode object, bypassing the keymap. Used mostly for
    macros.
    '''
    return KeycodeUpDown(
        type=KEYCODE_UP_EVENT,
        keycode=keycode,
    )


def keycode_down_event(keycode):
    '''
    Release a key by Keycode object, bypassing the keymap. Used mostly for
    macros.
    '''
    return KeycodeUpDown(
        type=KEYCODE_DOWN_EVENT,
        keycode=keycode,
    )


def new_matrix_event(matrix):
    return NewMatrix(
        type=NEW_MATRIX_EVENT,
        matrix=matrix,
    )


def hid_report_event():
    return BareEvent(
        type=HID_REPORT_EVENT,
    )


def macro_complete_event():
    return BareEvent(
        type=MACRO_COMPLETE_EVENT,
    )


def pending_keycode_pop_event():
    return BareEvent(
        type=PENDING_KEYCODE_POP_EVENT,
    )


def matrix_changed(new_pressed):
    def _key_pressed(dispatch, get_state):
        dispatch(new_matrix_event(new_pressed))

        state = get_state()

        if state.hid_pending:
            dispatch(hid_report_event())

        if Keycodes.KMK.KC_RESET in state.keys_pressed:
            reset_bootloader()

        if state.pending_keys:
            for key in state.pending_keys:
                if not key.no_press:
                    dispatch(keycode_down_event(key))
                    dispatch(hid_report_event())

                if not key.no_release:
                    dispatch(keycode_up_event(key))
                    dispatch(hid_report_event())

                dispatch(pending_keycode_pop_event())

        if state.macro_pending:
            macro = state.macro_pending

            for event in macro(state):
                dispatch(event)

            dispatch(macro_complete_event())

    return _key_pressed
