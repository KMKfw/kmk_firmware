import time

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

def scan():
    ble = BLERadio()

    uart_connection = None
    # See if any existing connections are providing UARTService.
    if ble.connected:
        for connection in ble.connections:
            if UARTService in connection:
                uart_connection = connection
            break

    if not uart_connection:
        print("Scanning...")
        for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=30):
            if UARTService in adv.services:
                print("found a UARTService advertisement")
                uart_connection = ble.connect(adv)
                ble.stop_scan()
                print('Scan complete')
                break
        # Stop scanning whether or not we are connected.
    return uart_connection

def send(uart_connection, data):
    if uart_connection and uart_connection.connected:
        try:
            uart_connection[UARTService].write(data)
        except OSError:
            try:
                uart_connection.disconnect()
            except:  # pylint: disable=bare-except
                pass
            uart_connection = None

def advertise():
    print('Advertising')
    ble = BLERadio()
    uart = UARTService()
    advertisement = ProvideServicesAdvertisement(uart)

    while True:
        ble.start_advertising(advertisement)
        while not ble.connected:
            pass
        while ble.connected:
            print('Advertising complete')
            return uart

def receive(uart):
    update = uart.read(3)
    if update == b'':
        update = None
    return update
