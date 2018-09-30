try:
    from collections import namedtuple
except ImportError:
    from ucollections import namedtuple

HIDMode = namedtuple('HIDMode', (
    'subclass',
    'protocol',
    'max_packet_length',
    'polling_interval',
    'report_descriptor',
))

hid_keyboard = HIDMode(0, 0, 0, 0, bytearray(0))
