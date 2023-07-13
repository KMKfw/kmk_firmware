
from kmk.keys import KC
from kmk.handlers.sequences import simple_key_sequence, send_string

COUNTDOWN_TO_PASTE = simple_key_sequence(
    (
        KC.N3,
        KC.ENTER,
        KC.MACRO_SLEEP_MS(1000),
        KC.N2,
        KC.ENTER,
        KC.MACRO_SLEEP_MS(1000),
        KC.N1,
        KC.ENTER,
        KC.MACRO_SLEEP(1000),
        KC.LCTL(KC.V),
    )
)

GMAIL = send_string("eyalgindi@gmail.com")