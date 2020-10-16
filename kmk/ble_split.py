from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()


def check_all_connections(is_target):
    connection_count = len(ble.connections)
    if is_target:
        return bool(connection_count > 1)
    return bool(connection_count > 0)


def initiator_scan():
    uart = None
    # See if any existing connections are providing UARTService.
    if ble.connected:
        for connection in ble.connections:
            if UARTService in connection:
                uart = connection
            break

    if not uart:
        print('Scanning...')
        for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=900):
            print('Scanning...')
            if UARTService in adv.services:
                print('found a UARTService advertisement')
                uart = ble.connect(adv)
                ble.stop_scan()
                print('Scan complete')
                break
    return uart


def send(uart, data):
    if uart and uart.connected:
        try:
            uart[UARTService].write(data)
        except OSError:
            try:
                uart.disconnect()
            except:  # noqa: E722
                print('UART disconnect failed')
            print('Connection error')
            uart = None
    return uart


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
            if check_all_connections(is_target=True):
                print('Advertising complete')
                return uart
