'''

MIT License

Copyright (c) 2021 mfranck

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import board
import busio
import digitalio

import adafruit_pixelbuf
from micropython import const

_COMMAND_REGISTER            = const(0xFD)
_COMMAND_REGISTER_WRITE_LOCK = const(0xFE)
_INTERRUPT_MASK_REGISTER     = const(0xF0)
_INTERRUPT_STATUS_REGISTER   = const(0xF1)

_LED_CONTROL_REGISTER      = const(0x00)
_PWM_REGISTER              = const(0x01)
_AUTO_BREATH_MODE_REGISTER = const(0x02)
_FUNCTION_REGISTER         = const(0x03)

_WRITE_LOCK_DISABLE_ONCE = const(0xC5)

_LED_ONOFF_REGISTER_START = const(0x00)
_LED_OPEN_REGISTER_START  = const(0x18)
_LED_SHORT_REGISTER_START = const(0x30)

_CONFIGURATION_REGISTER               = const(0x00)
_CURRENT_CONTROL_REGISTER             = const(0x01)
_TIME_UPDATE_REGISTER                 = const(0x0E)
_PULLUP_RESISTOR_SELECTION_REGISTER   = const(0x0F)
_PULLDOWN_RESISTOR_SELECTION_REGISTER = const(0x10)
_RESET_REGISTER                       = const(0x11)

CONFIGURATION_SYNC_CLOCK_MASTER            = const(0b01000000)
CONFIGURATION_SYNC_CLOCK_SLAVE             = const(0b10000000)
CONFIGURATION_SYNC_CLOCK_HIGH_IMPEDANCE    = const(0b00000000)
CONFIGURATION_OPEN_SHORT_DETECTION_ENABLE  = const(0b00000100)
CONFIGURATION_OPEN_SHORT_DETECTION_DISABLE = const(0b00000000)
CONFIGURATION_ABM_ENABLE                   = const(0b00000010)
CONFIGURATION_PWM_ENABLE                   = const(0b00000000)
CONFIGURATION_SOFTWARE_SHUTDOWN            = const(0b00000000)
CONFIGURATION_NORMAL_OPERATION             = const(0b00000001)

AUTO_CLEAR_INTERRUPT_ENABLE = const(0x08)
AUTO_CLEAR_INTERRUPT_DISABLE = const(0x00)
AUTO_BREATH_INTERRUPT_ENABLE = const(0x04)
AUTO_BREATH_INTERRUPT_DISABLE = const(0x00)
DOT_SHORT_INTERRUPT_ENABLE = const(0x02)
DOT_SHORT_INTERRUPT_DISABLE = const(0x00)
DOT_OPEN_INTERRUPT_ENABLE = const(0x01)
DOT_OPEN_INTERRUPT_DISABLE = const(0x00)

LED_MODE_PWM  = const(0x00)
LED_MODE_ABM1 = const(0x01)
LED_MODE_ABM2 = const(0x02)
LED_MODE_ABM3 = const(0x03)

ABM_T1_T3_210MS   = const(0x00)
ABM_T1_T3_420MS   = const(0x20)
ABM_T1_T3_840MS   = const(0x40)
ABM_T1_T3_1680MS  = const(0x60)
ABM_T1_T3_3360MS  = const(0x80)
ABM_T1_T3_6720MS  = const(0xA0)
ABM_T1_T3_13440MS = const(0xC0)
ABM_T1_T3_26880MS = const(0xE0)

ABM_T2_T4_0MS     = const(0x00)
ABM_T2_T4_210MS   = const(0x02)
ABM_T2_T4_420MS   = const(0x04)
ABM_T2_T4_840MS   = const(0x06)
ABM_T2_T4_1680MS  = const(0x08)
ABM_T2_T4_3360MS  = const(0x0A)
ABM_T2_T4_6720MS  = const(0x0C)
ABM_T2_T4_13440MS = const(0x0E)
ABM_T2_T4_26880MS = const(0x10)

ABM_T4_53760MS  = const(0x12)
ABM_T4_107520MS = const(0x14)

ABM_LOOP_BEGIN_T1 = const(0x00)
ABM_LOOP_BEGIN_T2 = const(0x10)
ABM_LOOP_BEGIN_T3 = const(0x20)
ABM_LOOP_BEGIN_T4 = const(0x30)

ABM_LOOP_END_T3 = const(0x00)
ABM_LOOP_END_T1 = const(0x40)

RESISTOR_NONE = const(0x00)
RESISTOR_500  = const(0x01)
RESISTOR_1K   = const(0x02)
RESISTOR_2K   = const(0x03)
RESISTOR_4K   = const(0x04)
RESISTOR_8K   = const(0x05)
RESISTOR_16K  = const(0x06)
RESISTOR_32K  = const(0x07)



class IS31FL3733:
    def __init__(self, address = 0x50):
        self._address = address
        self._page = 0x00
        self._brightness = 0x00
        self._sync_mode = CONFIGURATION_SYNC_CLOCK_HIGH_IMPEDANCE
        self._software_shutdown_mode = CONFIGURATION_SOFTWARE_SHUTDOWN
        self._breathing_enable_mode = CONFIGURATION_PWM_ENABLE 
        self._auto_clear_interrupt = AUTO_CLEAR_INTERRUPT_DISABLE
        self._auto_breath_interrupt = AUTO_BREATH_INTERRUPT_DISABLE
        self._dot_short_interrupt = DOT_SHORT_INTERRUPT_DISABLE
        self._dot_open_interrupt = DOT_OPEN_INTERRUPT_DISABLE
        self._pullup_resistor = RESISTOR_NONE
        self._pulldown_resistor = RESISTOR_NONE

        self.pwm_pixels = bytearray(12 * 16)
        self.abm_pixels = bytearray(12 * 16)
        self.onoff_pixels = bytearray(12 * 16)

        self.power = digitalio.DigitalInOut(board.RGB_POWER)
        self.power.direction = digitalio.Direction.OUTPUT
        self.power.value = 1

        # self.i2c = board.I2C()
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
        self.i2c.try_lock()

        self.reset()
        self.configure_auto_breath_mode()
        self.software_shutdown_mode = CONFIGURATION_NORMAL_OPERATION
        self.pullup_resistor = RESISTOR_32K
        self.pulldown_resistor = RESISTOR_32K
        for i in range(192):
            self.onoff_pixels[i] = 0x01
        self.update_onoff_pixels()
        self.brightness = 128


    @property
    def page(self, n):
        return self._page

    @page.setter
    def page(self, n):
        if self._page is n:
            return
        self.i2c.writeto(self._address, bytearray((_COMMAND_REGISTER_WRITE_LOCK, _WRITE_LOCK_DISABLE_ONCE)))
        self.i2c.writeto(self._address, bytearray((_COMMAND_REGISTER, n)))
        self._page = n

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, n):
        self.page = _FUNCTION_REGISTER
        self.i2c.writeto(self._address, bytearray((_CURRENT_CONTROL_REGISTER, n)))
        self._brightness = n

    @property
    def sync_mode(self):
        return self._sync_mode
    
    @sync_mode.setter
    def sync_mode(self, sync_mode):
        value = (sync_mode | self._breathing_enable_mode | self._software_shutdown_mode)
        self.page = _FUNCTION_REGISTER
        self.i2c.writeto(self._address, bytearray((_CONFIGURATION_REGISTER, value)))
        self._sync_mode = sync_mode

    @property
    def breathing_enable_mode(self):
        return self._breathing_enable_mode
    
    @breathing_enable_mode.setter
    def breathing_enable_mode(self, breathing_enable_mode):
        value = (self._sync_mode | breathing_enable_mode | self._software_shutdown_mode)
        self.page = _FUNCTION_REGISTER
        self.i2c.writeto(self._address, bytearray((_CONFIGURATION_REGISTER, value)))
        self._breathing_enable_mode = breathing_enable_mode

    @property
    def software_shutdown_mode(self):
        return self._software_shutdown_mode
    
    @software_shutdown_mode.setter
    def software_shutdown_mode(self, software_shutdown_mode):
        value = (self._sync_mode | self._breathing_enable_mode | software_shutdown_mode)
        self.page = _FUNCTION_REGISTER
        self.i2c.writeto(self._address, bytearray((_CONFIGURATION_REGISTER, value)))
        self._software_shutdown_mode = software_shutdown_mode

    @property
    def pullup_resistor(self):
        return self._pullup_resistor

    @pullup_resistor.setter
    def pullup_resistor(self, resistor):
        self.page = _FUNCTION_REGISTER
        self.i2c.writeto(self._address, bytearray((_PULLUP_RESISTOR_SELECTION_REGISTER, resistor)))
        self._pullup_resistor = resistor

    @property
    def pulldown_resistor(self):
        return self._pulldown_resistor

    @pulldown_resistor.setter
    def pulldown_resistor(self, resistor):
        self.page = _FUNCTION_REGISTER
        self.i2c.writeto(self._address, bytearray((_PULLDOWN_RESISTOR_SELECTION_REGISTER, resistor)))
        self._pulldown_resistor = resistor

    @property
    def auto_clear_interrupt(self):
        return self._auto_clear_interrupt

    @auto_clear_interrupt.setter
    def auto_clear_interrupt(self, auto_clear_interrupt):
        value = (auto_clear_interrupt | self._auto_breath_interrupt | self._dot_short_interrupt | self._dot_open_interrupt)
        self.i2c.writeto(self._address, bytearray((_INTERRUPT_MASK_REGISTER, value)))
        self._auto_clear_interrupt = auto_clear_interrupt

    @property
    def auto_breath_interrupt(self):
        return self._auto_breath_interrupt

    @auto_breath_interrupt.setter
    def auto_breath_interrupt(self, auto_breath_interrupt):
        value = (self._auto_clear_interrupt | auto_breath_interrupt | self._dot_short_interrupt | self._dot_open_interrupt)
        self.i2c.writeto(self._address, bytearray((_INTERRUPT_MASK_REGISTER, value)))
        self._auto_breath_interrupt = auto_breath_interrupt

    @property
    def dot_short_interrupt(self):
        return self._dot_short_interrupt

    @dot_short_interrupt.setter
    def dot_short_interrupt(self, dot_short_interrupt):
        value = (self._auto_clear_interrupt | self._auto_breath_interrupt | dot_short_interrupt | self._dot_open_interrupt)
        self.i2c.writeto(self._address, bytearray((_INTERRUPT_MASK_REGISTER, value)))
        self._dot_short_interrupt = dot_short_interrupt

    @property
    def dot_open_interrupt(self):
        return self._dot_open_interrupt

    @dot_open_interrupt.setter
    def dot_open_interrupt(self, dot_open_interrupt):
        value = (self._auto_clear_interrupt | self._auto_breath_interrupt | self._dot_short_interrupt | dot_open_interrupt)
        self.i2c.writeto(self._address, bytearray((_INTERRUPT_MASK_REGISTER, value)))
        self._dot_open_interrupt = dot_open_interrupt

    @property
    def interrupt_status_register(self):
        buffer = bytearray(0x01)
        self.i2c.writeto_then_readfrom(self._address, bytes([_INTERRUPT_STATUS_REGISTER]), buffer)
        return buffer

    @property
    def open_pixels(self):
        self.page = _LED_CONTROL_REGISTER
        buffer = bytearray(0x18)
        self.i2c.writeto_then_readfrom(self._address, bytes([_LED_OPEN_REGISTER_START]), buffer)
        return buffer

    @property
    def short_pixels(self):
        self.page = _LED_CONTROL_REGISTER
        buffer = bytearray(0x18)
        self.i2c.writeto_then_readfrom(self._address, bytes([_LED_SHORT_REGISTER_START]), buffer)
        return buffer

    def reset(self):
        self.page = _FUNCTION_REGISTER
        buffer = bytearray(0x01)
        self.i2c.writeto_then_readfrom(self._address, bytes([_RESET_REGISTER]), buffer)

    def trigger_open_short_detection(self):
        on = (self._sync_mode | CONFIGURATION_OPEN_SHORT_DETECTION_ENABLE | self._breathing_enable_mode | self._software_shutdown_mode)
        off = (self._sync_mode | CONFIGURATION_OPEN_SHORT_DETECTION_DISABLE | self._breathing_enable_mode | self._software_shutdown_mode)
        self.page = _FUNCTION_REGISTER
        self.i2c.writeto(self._address, bytearray((_CURRENT_CONTROL_REGISTER, 0x01)))
        self.i2c.writeto(self._address, bytearray((_CONFIGURATION_REGISTER, on)))
        self.i2c.writeto(self._address, bytearray((_CONFIGURATION_REGISTER, off)))
        self.i2c.writeto(self._address, bytearray((_CURRENT_CONTROL_REGISTER, self._brightness)))

    def configure_auto_breath_mode(self, abm_num = 1, abm_t1 = ABM_T1_T3_3360MS, abm_t2 = ABM_T2_T4_210MS, abm_t3 = ABM_T1_T3_3360MS, abm_t4 = ABM_T2_T4_210MS, loop_begin = ABM_LOOP_BEGIN_T4, loop_end = ABM_LOOP_END_T3):
        start = 0x02 + (abm_num - 1) * 4
        self.page = _FUNCTION_REGISTER
        self.i2c.writeto(self._address, bytearray((start, (abm_t1 | abm_t2))))
        self.i2c.writeto(self._address, bytearray((start + 1, (abm_t3 | abm_t4))))
        self.i2c.writeto(self._address, bytearray((start + 2, (loop_begin | loop_end))))
        self.i2c.writeto(self._address, bytearray((_TIME_UPDATE_REGISTER , 0x00)))

    def set_pwm_pixel(self, i, value):
        buffer = self.pwm_pixels
        row = i // 16
        col = i & 15 
        offset = row * 48 + col
        buffer[offset] = value[1]
        buffer[offset + 16] = value[0]
        buffer[offset + 32] = value[2]
        self.pwm_pixels = buffer

    def set_abm_pixel(self, i, value):
        buffer = self.abm_pixels
        row = i // 16
        col = i & 15 
        offset = row * 48 + col
        buffer[offset] = value[1]
        buffer[offset + 16] = value[0]
        buffer[offset + 32] = value[2]
        self.abm_pixels = buffer

    def set_onoff_pixel(self, i, value):
        buffer = self.onoff_pixels
        row = i // 16
        col = i & 15 
        offset = row * 48 + col
        buffer[offset] = value
        buffer[offset + 16] = value
        buffer[offset + 32] = value
        self.onoff_pixels = buffer
    
    def update_pwm_pixels(self):
        self.page = _PWM_REGISTER
        buffer = bytes([0x00]) + self.pwm_pixels
        self.i2c.writeto(self._address, buffer)

    def update_abm_pixels(self):
        self.page = _AUTO_BREATH_MODE_REGISTER
        buffer = bytes([0x00]) + self.abm_pixels
        self.i2c.writeto(self._address, buffer)

    def update_onoff_pixels(self):
        buffer = bytearray(0x18)
        array = self.onoff_pixels
        r = range(0,len(array))
        for i in r:
            byte = i // 8
            bit = i & 7
            value = (2 ** bit) * array[i] 
            buffer[byte] += value
        self.page = _LED_CONTROL_REGISTER
        buffer = bytes([_LED_ONOFF_REGISTER_START]) + buffer
        self.i2c.writeto(self._address, buffer)

    def clear_pwm_pixels(self):
        buffer = self.pwm_pixels
        r = range(192)
        for i in r:
            buffer[i] = 0x00
        self.pwm_pixels = buffer

    def clear_abm_pixels(self):
        buffer = self.abm_pixels
        r = range(192)
        for i in r:
            buffer[i] = 0x00
        self.abm_pixels = buffer

    def clear_onoff_pixels(self):
        buffer = self.onoff_pixels
        r = range(192)
        for i in r:
            buffer[i] = 0x00
        self.onoff_pixels = buffer


# Helper for Adafruit_CircuitPython_LED_Animation, and so on.
class Helper(adafruit_pixelbuf.PixelBuf):

    driver = IS31FL3733()
    class LED:
        def __init__(self, i, rgb):
            self.fill(rgb)
        def fill(self, value):
            self.driver.set_pwm_pixel(i, value)
            self.driver.update_pwm_pixels()


    def fill(self, value):
        for i in range(0,len(self)):
            self.driver.set_pwm_pixel(i, value)
        #self.led.update_pwm_pixels()

    def __getitem__(self, i):
        return LED(i, (buffer[offset], buffer[offset + 16], buffer[offset + 32]))

    def __setitem__(self, i, value):
        self.driver.set_pwm_pixel(i, value)

    @property
    def brightness(self):
        """
        Float value between 0 and 1.  Output brightness.
        When brightness is less than 1.0, a second buffer will be used to store the color values
        before they are adjusted for brightness.
        """
        return self._brightness

    @brightness.setter
    def brightness(self, value: float):
        self.driver.brightness = int(value*255)
        self._brightness = value

    def show(self): 
        self.driver.update_pwm_pixels()