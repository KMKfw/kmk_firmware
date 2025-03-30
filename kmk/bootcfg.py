try:
    from typing import Optional
except ImportError:
    pass

import digitalio
import microcontroller
import usb_hid


def bootcfg(
    sense: Optional[microcontroller.Pin, digitalio.DigitalInOut] = None,
    source: Optional[microcontroller.Pin, digitalio.DigitalInOut] = None,
    autoreload: bool = True,
    boot_device: int = 0,
    cdc_console: bool = True,
    cdc_data: bool = False,
    consumer_control: bool = True,
    keyboard: bool = True,
    midi: bool = True,
    mouse: bool = True,
    nkro: bool = False,
    pan: bool = False,
    six_axis: bool = False,
    storage: bool = True,
    usb_id: Optional[dict, tuple[str, str]] = {},
    **kwargs,
) -> bool:

    if len(kwargs):
        print('unknown option', kwargs)

    if isinstance(sense, microcontroller.Pin):
        sense = digitalio.DigitalInOut(sense)
        sense.direction = digitalio.Direction.INPUT
        sense.pull = digitalio.Pull.UP

    if isinstance(source, microcontroller.Pin):
        source = digitalio.DigitalInOut(source)
        source.direction = digitalio.Direction.OUTPUT
        source.value = False

    if not autoreload:
        import supervisor

        supervisor.runtime.autoreload = False

    # Parse `usb_id` tuple for backwards compatibility. This can be removed at
    # some point in the future(TM).
    if type(usb_id) is tuple:
        usb_id = {'manufacturer': usb_id[0], 'product': usb_id[1]}

    # configure HID devices
    devices = []
    if six_axis:
        from kmk.hid_reports import six_axis

        # SpaceMouse Compact
        usb_id['vid'] = 0x256F
        usb_id['pid'] = 0xC635

        if keyboard:
            if nkro:
                devices.append(six_axis.NKRO_KEYBOARD)
            else:
                devices.append(six_axis.KEYBOARD)
            keyboard = False
        if mouse:
            if pan:
                devices.append(six_axis.POINTER)
            else:
                devices.append(six_axis.MOUSE)
            mouse = False
        if consumer_control:
            devices.append(six_axis.CONSUMER_CONTROL)
            consumer_control = False
        devices.append(six_axis.SIX_AXIS)
    if keyboard:
        if nkro:
            from kmk.hid_reports import nkro_keyboard

            devices.append(nkro_keyboard.NKRO_KEYBOARD)
        else:
            devices.append(usb_hid.Device.KEYBOARD)
    if mouse:
        if pan:
            from kmk.hid_reports import pointer

            devices.append(pointer.POINTER)
        else:
            devices.append(usb_hid.Device.MOUSE)
    if consumer_control:
        devices.append(usb_hid.Device.CONSUMER_CONTROL)
    if devices:
        usb_hid.enable(devices, boot_device)
    else:
        usb_hid.disable()

    # configure midi over usb
    if not midi:
        import usb_midi

        usb_midi.disable()

    # configure usb vendor and product id
    if usb_id:
        import supervisor

        try:
            supervisor.set_usb_identification(**usb_id)
        except Exception as e:
            print('supervisor.set_usb_identification: ', e, type(e))

    # configure data serial
    if cdc_data:
        import usb_cdc

        usb_cdc.enable(data=True)

    # sense not provided or pulled low -> Skip boot configuration that may
    # disable debug or rescue facilities.
    if sense is None or not sense.value:
        return False

    # Entries for serial console (REPL) and storage are intentionally evaluated
    # last to ensure the board is debuggable, mountable and rescueable, in case
    # any of the previous code throws an exception.
    if not cdc_console:
        import usb_cdc

        usb_cdc.enable(console=False)

    if not storage:
        import storage

        storage.disable_usb_drive()

    return True
