import time

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()

def initiator_scan():
    uart_connection = None
    # See if any existing connections are providing UARTService.
    if ble.connected:
        for connection in ble.connections:
            if UARTService in connection:
                uart_connection = connection
            break

    if not uart_connection:
        print("Scanning...")
        for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=900):
            print("Scanning...")
            if UARTService in adv.services:
                print("found a UARTService advertisement")
                uart_connection = ble.connect(adv)
                ble.stop_scan()
                print('Scan complete')
                break
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
            print('Connection error')
            uart_connection = None
    return uart_connection


def target_advertise(uart):
    print('Advertising')
    # Uart must not change on this connection if reconnecting
    if not uart:
        uart = UARTService()
    advertisement = ProvideServicesAdvertisement(uart)

    ble.start_advertising(advertisement)

    while True:
        while not ble.connected:
            pass
        while ble.connected:
            connnection_count = len(ble.connections)
            if connnection_count > 1:
                print('Advertising complete')
                return uart

def check_all_connections(is_target):
    connnection_count = len(ble.connections)
    if is_target:
        if connnection_count > 1:
            return True
        else:
            return False
    else:
        if connnection_count > 0:
            return True
        else:
            return False
