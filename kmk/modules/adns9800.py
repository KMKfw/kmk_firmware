import busio
import digitalio
import microcontroller

import time

from kmk.keys import AX
from kmk.modules import Module
from kmk.modules.adns9800_firmware import firmware


class REG:
    Product_ID = 0x0
    Revision_ID = 0x1
    MOTION = 0x2
    DELTA_X_L = 0x3
    DELTA_X_H = 0x4
    DELTA_Y_L = 0x5
    DELTA_Y_H = 0x6
    SQUAL = 0x7
    PIXEL_SUM = 0x8
    Maximum_Pixel = 0x9
    Minimum_Pixel = 0xA
    Shutter_Lower = 0xB
    Shutter_Upper = 0xC
    Frame_Period_Lower = 0xD
    Frame_Period_Upper = 0xE
    Configuration_I = 0xF
    Configuration_II = 0x10
    Frame_Capture = 0x12
    SROM_Enable = 0x13
    Run_Downshift = 0x14
    Rest1_Rate = 0x15
    Rest1_Downshift = 0x16
    Rest2_Rate = 0x17
    Rest2_Downshift = 0x18
    Rest3_Rate = 0x19
    Frame_Period_Max_Bound_Lower = 0x1A
    Frame_Period_Max_Bound_Upper = 0x1B
    Frame_Period_Min_Bound_Lower = 0x1C
    Frame_Period_Min_Bound_Upper = 0x1D
    Shutter_Max_Bound_Lower = 0x1E
    Shutter_Max_Bound_Upper = 0x1F
    LASER_CTRL0 = 0x20
    Observation = 0x24
    Data_Out_Lower = 0x25
    Data_Out_Upper = 0x26
    SROM_ID = 0x2A
    Lift_Detection_Thr = 0x2E
    Configuration_V = 0x2F
    Configuration_IV = 0x39
    Power_Up_Reset = 0x3A
    Shutdown = 0x3B
    Inverse_Product_ID = 0x3F
    Snap_Angle = 0x42
    Motion_Burst = 0x50
    SROM_Load_Burst = 0x62
    Pixel_Burst = 0x64


class ADNS9800(Module):
    tswr = tsww = 120
    tsrw = tsrr = 20
    tsrad = 100
    tbexit = 1
    baud = 2000000
    cpol = 1
    cpha = 1
    DIR_WRITE = 0x80
    DIR_READ = 0x7F

    def __init__(self, cs, sclk, miso, mosi, invert_x=False, invert_y=False):
        self.cs = digitalio.DigitalInOut(cs)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.spi = busio.SPI(clock=sclk, MOSI=mosi, MISO=miso)
        self.invert_x = invert_x
        self.invert_y = invert_y

    def adns_start(self):
        self.cs.value = False

    def adns_stop(self):
        self.cs.value = True

    def adns_write(self, reg, data):
        while not self.spi.try_lock():
            pass
        try:
            self.spi.configure(baudrate=self.baud, polarity=self.cpol, phase=self.cpha)
            self.adns_start()
            self.spi.write(bytes([reg | self.DIR_WRITE, data]))
        finally:
            self.spi.unlock()
            self.adns_stop()

    def adns_read(self, reg):
        result = bytearray(1)
        while not self.spi.try_lock():
            pass
        try:
            self.spi.configure(baudrate=self.baud, polarity=self.cpol, phase=self.cpha)
            self.adns_start()
            self.spi.write(bytes([reg & self.DIR_READ]))
            microcontroller.delay_us(self.tsrad)
            self.spi.readinto(result)
        finally:
            self.spi.unlock()
            self.adns_stop()

        return result[0]

    def adns_upload_srom(self):
        while not self.spi.try_lock():
            pass
        try:
            self.spi.configure(baudrate=self.baud, polarity=self.cpol, phase=self.cpha)
            self.adns_start()
            self.spi.write(bytes([REG.SROM_Load_Burst | self.DIR_WRITE]))
            for b in firmware:
                self.spi.write(bytes([b]))
        finally:
            self.spi.unlock()
            self.adns_stop()

    def delta_to_int(self, high, low):
        comp = (high << 8) | low
        if comp & 0x8000:
            return (-1) * (0xFFFF + 1 - comp)
        return comp

    def adns_read_motion(self):
        result = bytearray(14)
        while not self.spi.try_lock():
            pass
        try:
            self.spi.configure(baudrate=self.baud, polarity=self.cpol, phase=self.cpha)
            self.adns_start()
            self.spi.write(bytes([REG.Motion_Burst & self.DIR_READ]))
            microcontroller.delay_us(self.tsrad)
            self.spi.readinto(result)
        finally:
            self.spi.unlock()
            self.adns_stop()
        microcontroller.delay_us(self.tbexit)
        self.adns_write(REG.MOTION, 0x0)
        return result

    def during_bootup(self, keyboard):

        self.adns_write(REG.Power_Up_Reset, 0x5A)
        time.sleep(0.1)
        self.adns_read(REG.MOTION)
        microcontroller.delay_us(self.tsrr)
        self.adns_read(REG.DELTA_X_L)
        microcontroller.delay_us(self.tsrr)
        self.adns_read(REG.DELTA_X_H)
        microcontroller.delay_us(self.tsrr)
        self.adns_read(REG.DELTA_Y_L)
        microcontroller.delay_us(self.tsrr)
        self.adns_read(REG.DELTA_Y_H)
        microcontroller.delay_us(self.tsrw)

        self.adns_write(REG.Configuration_IV, 0x2)
        microcontroller.delay_us(self.tsww)
        self.adns_write(REG.SROM_Enable, 0x1D)
        microcontroller.delay_us(1000)
        self.adns_write(REG.SROM_Enable, 0x18)
        microcontroller.delay_us(self.tsww)

        self.adns_upload_srom()
        microcontroller.delay_us(2000)

        laser_ctrl0 = self.adns_read(REG.LASER_CTRL0)
        microcontroller.delay_us(self.tsrw)
        self.adns_write(REG.LASER_CTRL0, laser_ctrl0 & 0xF0)
        microcontroller.delay_us(self.tsww)
        self.adns_write(REG.Configuration_I, 0x10)
        microcontroller.delay_us(self.tsww)

        if keyboard.debug_enabled:
            print('ADNS: Product ID ', hex(self.adns_read(REG.Product_ID)))
            microcontroller.delay_us(self.tsrr)
            print('ADNS: Revision ID ', hex(self.adns_read(REG.Revision_ID)))
            microcontroller.delay_us(self.tsrr)
            print('ADNS: SROM ID ', hex(self.adns_read(REG.SROM_ID)))
            microcontroller.delay_us(self.tsrr)
            if self.adns_read(REG.Observation) & 0x20:
                print('ADNS: Sensor is running SROM')
            else:
                print('ADNS: Error! Sensor is not runnin SROM!')

        return

    def before_matrix_scan(self, keyboard):
        motion = self.adns_read_motion()
        if motion[0] & 0x80:
            delta_x = self.delta_to_int(motion[3], motion[2])
            delta_y = self.delta_to_int(motion[5], motion[4])

            if self.invert_x:
                delta_x *= -1
            if self.invert_y:
                delta_y *= -1

            if delta_x:
                AX.X.move(delta_x)

            if delta_y:
                AX.Y.move(delta_y)

            if keyboard.debug_enabled:
                print('Delta: ', delta_x, ' ', delta_y)

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return
