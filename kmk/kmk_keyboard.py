# There's a chance doing preload RAM hacks this late will cause recursion
# errors, but we'll see. I'd rather do it here than require everyone copy-paste
# a line into their keymaps.
import kmk.preload_imports  # isort:skip # NOQA
from kmk import led, rgb
import busio
from kmk.consts import LeaderMode, UnicodeMode
from kmk.hid import AbstractHID, HIDModes
from kmk.internal_state import InternalState
from kmk.keys import KC
from kmk.kmktime import sleep_ms
from kmk.matrix import MatrixScanner
from kmk.matrix import intify_coordinate as ic
from kmk.encoder import Encoder
from kmk.graphics import Graphics as Icon
import adafruit_ssd1306
#import usb_hid
#from adafruit_hid.consumer_control import ConsumerControl
#from adafruit_hid.consumer_control_code import ConsumerControlCode



class KMKKeyboard:
    debug_enabled = False

    keymap = None
    coord_mapping = None

    row_pins = None
    col_pins = None
    diode_orientation = None
    matrix_scanner = MatrixScanner
    uart_buffer = []

    unicode_mode = UnicodeMode.NOOP
    tap_time = 300
    leader_mode = LeaderMode.TIMEOUT
    leader_dictionary = {}
    leader_timeout = 1000

    # Split config
    extra_data_pin = None
    split_offsets = ()
    split_flip = False
    target_side = None
    split_type = None
    split_target_left = True
    is_target = None
    uart = None
    uart_flip = True
    uart_pin = None

    # RGB config
    rgb_pixel_pin = None
    rgb_config = rgb.rgb_config

    # led config (mono color)
    led_pin = None
    led_config = led.led_config

    # encoder setup
    enable_encoder = False
    enc_a = None
    enc_b = None
    encoder = []
    encoder_resolution = None
    increment_keys = None
    decrement_keys = None
    encoder_count = None
    encoder_map = None
    use_encoder_map = False

    # OLED Setup - i2c SSD1306 only at the moment 2 oleds supported
    i2c_bus0 = None
    i2c_bus1 = None
    oleds = []
    oled_sda = None
    oled_scl = None
    oled_height = None
    oled_width = None
    oled_bus = None
    oled_count = None
    oled_addr = [0x31,0x32]
    enable_oleds = False
    # prev_key = ''
    # prev_layer_name = 'BASE'
    # layer_names = []
    # key_log = []
    # prev_key_string = ''
    # prev_key_log = []


    graphics = None

    # mode badge handling
    # prev = None
    # icon = None
    # prev_icon = []


    def __repr__(self):
        return (
            'KMKKeyboard('
            'debug_enabled={} '
            'keymap=truncated '
            'coord_mapping=truncated '
            'row_pins=truncated '
            'col_pins=truncated '
            'diode_orientation={} '
            'matrix_scanner={} '
            'unicode_mode={} '
            'tap_time={} '
            'leader_mode={} '
            'leader_dictionary=truncated '
            'leader_timeout={} '
            'hid_helper={} '
            'extra_data_pin={} '
            'split_offsets={} '
            'split_flip={} '
            'target_side={} '
            'split_type={} '
            'split_target_left={} '
            'is_target={} '
            'uart={} '
            'uart_flip={} '
            'uart_pin={}'
            'enable_encoder={}'
            'enc_a={}'
            'enc_b={}'
            'encoder={}'
            'encoder_resolution={}'
            'increment_keys={}'
            'decrement_keys={}'
            'encoder_count={}'
            'i2c_bus0={}'
            'i2c_buz1={}'
            'oleds={}'
            'oled_sda={}'
            'oled_scl={}'
            'oled_height={}'
            'oled_width={}'
            'oled_bus={}'
            'oled_count'
            'oled_addr={}'
            ')'
        ).format(
            self.debug_enabled,
            # self.keymap,
            # self.coord_mapping,
            # self.row_pins,
            # self.col_pins,
            self.diode_orientation,
            self.matrix_scanner,
            self.unicode_mode,
            self.tap_time,
            self.leader_mode,
            # self.leader_dictionary,
            self.leader_timeout,
            self.hid_helper.__name__,
            self.extra_data_pin,
            self.split_offsets,
            self.split_flip,
            self.target_side,
            self.split_type,
            self.split_target_left,
            self.is_target,
            self.uart,
            self.uart_flip,
            self.uart_pin,
            self.enable_encoder,
            self.enc_a,
            self.enc_b,
            self.encoder,
            self.encoder_resolution,
            self.increment_keys,
            self.decrement_keys,
            self.encoder_count,
            self.i2c_bus0,
            self.i2c_bus1,
            self.oleds,
            self.oled_sda,
            self.oled_scl,
            self.oled_height,
            self.oled_width,
            self.oled_bus,
            self.oled_count,
            self.oled_addr
        )


    def draw_badge(self, oled, mode_badge):
        #self.clear_oled(oled)
        for i in self._state.prev_mode_badge:
            oled.pixel(i[0]+95,i[1],0)

        for i in mode_badge:
            oled.pixel(i[0]+95,i[1],1)

        self.draw_layer_name(oled)
        oled.show()
        self._state.prev_mode_badge = mode_badge

    def draw_logo(self, oled, logo):
        #self.clear_oled(oled)
        for i in self._state.prev_logo:
            oled.pixel(i[0],i[1],0)

        for i in logo:
            oled.pixel(i[0],i[1],1)
        self._state.prev_logo = logo



    def draw_key(self, oled):
        # undraw last char
        oled.text(self._state.prev_key_string,40,18,0)

        if len(self._state.key_log) < 9:
            self._state.key_log.append(self._state.current_key)
        else:
            self._state.key_log.pop(0)
            self._state.key_log.append(self._state.current_key)
        
        self._state.prev_key_string = ''
        # traverse in the string
        for ele in self._state.key_log:
            self._state.prev_key_string += ele

        # draw current char
        oled.text(self._state.prev_key_string,40,18,1)
        oled.show()
        # set prev char
        self._state.prev_key_log = self._state.key_log
        self._state.prev_key = self._state.current_key

    def draw_layer_name(self, oled):
        # get center of display, must be int
        center = int(self.oled_width[0]/2)
        # get length to middle of mode name
        mid = int(len(self._state.prev_layer_name)/2 +len(self._state.prev_layer_name)%2)

        # erase old mode name
        oled.text(self._state.prev_layer_name,center-(mid*5),0,0)

        # get length of current mode name
        mid = int(len(self.layer_names[self._state.active_layers[0]])/2 + len(self.layer_names[self._state.active_layers[0]])%2)

        # draw current mode name
        oled.text(self.layer_names[self._state.active_layers[0]],center-(mid*5),0,1)

        # set prev mode name
        self._state.prev_layer_name = self.layer_names[self._state.active_layers[0]]

    def make_oleds(self):
        self.i2c_bus0 = busio.I2C(self.oled_scl[0], self.oled_sda[0])
        for i in range(self.oled_count):
            self.oleds.append(
                adafruit_ssd1306.SSD1306_I2C(
                    self.oled_width[i],
                    self.oled_height[i],
                    self.i2c_bus0
                    )
                )

    def clear_oled(self, oled):
        # start with a blank screen
        oled.fill(0)
        # we just blanked the framebuffer.
        # to push the framebuffer onto the display, we call show()
        oled.show()

    def make_encoders(self):
        for i in range(self.encoder_count):
            self.encoder.append(
                    Encoder(
                    self.enc_a[i],  # encoder pin a
                    self.enc_b[i],  # encoder pin b
                    None,  # button pin, defaults to None
                    True,  # invert increment/decrement - defaults to False
                    #self.increment_keys[i],  # keycode for increment
                    #self.decrement_keys[i],  # keycode for decrement
                    vel_mode = False # use velocity mode
                    )
                )

    def _send_hid(self):
        self._hid_helper_inst.create_report(self._state.keys_pressed).send()
        self._state.resolve_hid()

    def _send_key(self, key):
        if not getattr(key, 'no_press', None):
            self._state.add_key(key)
            self._send_hid()

        if not getattr(key, 'no_release', None):
            self._state.remove_key(key)
            self._send_hid()

    def _handle_matrix_report(self, update=None):
        '''
        Bulk processing of update code for each cycle
        :param update:
        '''
        if update is not None:

            self._state.matrix_changed(update[0], update[1], update[2])

    def _send_to_target(self, update):
        if self.split_target_left:
            update[1] += self.split_offsets[update[0]]
        else:
            update[1] -= self.split_offsets[update[0]]
        if self.uart is not None:
            self.uart.write(update)

    def _receive_from_initiator(self):
        if self.uart is not None and self.uart.in_waiting > 0 or self.uart_buffer:
            if self.uart.in_waiting >= 60:
                # This is a dirty hack to prevent crashes in unrealistic cases
                import microcontroller

                microcontroller.reset()

            while self.uart.in_waiting >= 3:
                self.uart_buffer.append(self.uart.read(3))
            if self.uart_buffer:
                update = bytearray(self.uart_buffer.pop(0))

                # Built in debug mode switch
                if update == b'DEB':
                    print(self.uart.readline())
                    return None
                return update

        return None

    def _send_debug(self, message):
        '''
        Prepends DEB and appends a newline to allow debug messages to
        be detected and handled differently than typical keypresses.
        :param message: Debug message
        '''
        if self.uart is not None:
            self.uart.write('DEB')
            self.uart.write(message, '\n')

    def init_uart(self, pin, timeout=20):
        if self.is_target:
            return busio.UART(tx=None, rx=pin, timeout=timeout)
        else:
            return busio.UART(tx=pin, rx=None, timeout=timeout)

    def send_encoder_keys(self, encoder_key, encoder_idx):
        # position in the encoder map tuple
        encoder_resolution = 2 
        for _ in range(self.encoder_map[self._state.active_layers[0]][encoder_idx][encoder_resolution]):
            self._send_key(self.encoder_map[self._state.active_layers[0]][encoder_idx][encoder_key])

    def go(self, hid_type=HIDModes.USB, **kwargs):
        assert self.keymap, 'must define a keymap with at least one row'
        assert self.row_pins, 'no GPIO pins defined for matrix rows'
        assert self.col_pins, 'no GPIO pins defined for matrix columns'
        assert self.diode_orientation is not None, 'diode orientation must be defined'
        assert (
            hid_type in HIDModes.ALL_MODES
        ), 'hid_type must be a value from kmk.consts.HIDModes'

        # Attempt to sanely guess a coord_mapping if one is not provided

        if not self.coord_mapping:
            self.coord_mapping = []

            rows_to_calc = len(self.row_pins)
            cols_to_calc = len(self.col_pins)

            if self.split_offsets:
                rows_to_calc *= 2
                cols_to_calc *= 2

            for ridx in range(rows_to_calc):
                for cidx in range(cols_to_calc):
                    self.coord_mapping.append(ic(ridx, cidx))
        self.icon = Icon()
        self._state = InternalState(self)
        if hid_type == HIDModes.NOOP:
            self.hid_helper = AbstractHID
        elif hid_type == HIDModes.USB:
            try:
                from kmk.hid import USBHID

                self.hid_helper = USBHID
            except ImportError:
                self.hid_helper = AbstractHID
                print('USB HID is unsupported ')
        elif hid_type == HIDModes.BLE:
            try:
                from kmk.ble import BLEHID

                self.hid_helper = BLEHID
            except ImportError:
                self.hid_helper = AbstractHID
                print('Bluetooth is unsupported ')

        self._hid_helper_inst = self.hid_helper(**kwargs)

        # Split keyboard Init
        if self.split_type is not None:
            try:
                # Working around https://github.com/adafruit/circuitpython/issues/1769
                self._hid_helper_inst.create_report([]).send()
                self.is_target = True

                # Sleep 2s so target portion doesn't "appear" to boot quicker than
                # dependent portions (which will take ~2s to time out on the HID send)
                sleep_ms(2000)
            except OSError:
                self.is_target = False

            if self.split_flip and not self.is_target:
                self.col_pins = list(reversed(self.col_pins))
            if self.target_side == 'Left':
                self.split_target_left = self.is_target
            elif self.target_side == 'Right':
                self.split_target_left = not self.is_target
        else:
            self.is_target = True

        if self.uart_pin is not None:
            self.uart = self.init_uart(self.uart_pin)

        if self.rgb_pixel_pin:
            self.pixels = rgb.RGB(self.rgb_config, self.rgb_pixel_pin)
            self.rgb_config = None  # No longer needed
            self.pixels.loopcounter = 0
        else:
            self.pixels = None

        if self.led_pin:
            self.led = led.led(self.led_pin, self.led_config)
            self.led_config = None  # No longer needed
        else:
            self.led = None

        self.matrix = self.matrix_scanner(
            cols=self.col_pins,
            rows=self.row_pins,
            diode_orientation=self.diode_orientation,
            rollover_cols_every_rows=getattr(self, 'rollover_cols_every_rows', None),
        )

        # Compile string leader sequences
        for k, v in self.leader_dictionary.items():
            if not isinstance(k, tuple):
                new_key = tuple(KC[c] for c in k)
                self.leader_dictionary[new_key] = v

        for k, v in self.leader_dictionary.items():
            if not isinstance(k, tuple):
                del self.leader_dictionary[k]

        if self.oleds != None:
            self.clear_oled(self.oleds[0])

        if self.enable_oleds:
            self.draw_logo(self.oleds[0], self.icon.logos['Python'])

        while True:
            if self.split_type is not None and self.is_target:
                update = self._receive_from_initiator()
                if update is not None:
                    self._handle_matrix_report(update)


            update = self.matrix.scan_for_changes()

            if update is not None:
                if self.is_target:
                    self._handle_matrix_report(update)
                else:
                    # This keyboard is a initiator, and needs to send data to target
                    self._send_to_target(update)

            if self.enable_oleds:
                if self._state.active_layers[0] != self._state.prev_active_layer:
                    self.draw_badge(
                        self.oleds[0],
                        self.icon.mode_badges[self._state.active_layers[0]][1]
                        )
                    self._state.prev_active_layer = self._state.active_layers[0]

                if self._state.keylog_update:
                    self.draw_key(self.oleds[0])
                    self._state.keylog_update = False


            if self.enable_encoder:
                for idx in range(self.encoder_count):
                    encoder_key = self.encoder[idx].report()
                    if encoder_key is not None:
                        self.send_encoder_keys(encoder_key,idx)

            if self._state.hid_pending:
                self._send_hid()

            old_timeouts_len = len(self._state.timeouts)
            self._state.process_timeouts()
            new_timeouts_len = len(self._state.timeouts)

            if old_timeouts_len != new_timeouts_len:
                if self._state.hid_pending:
                    self._send_hid()

            if self.pixels and self.pixels.animation_mode:
                self.pixels.loopcounter += 1
                if self.pixels.loopcounter >= 30:
                    self.pixels = self.pixels.animate()
                    self.pixels.loopcounter = 0

            if self.led and self.led.enabled and self.led.animation_mode:
                self.led = self.led.animate()
