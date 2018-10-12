# Flashing Instructions

Flashing sequence:

1. Press the `KC.RESET` keycode, or tap the RESET button.
2. Wait for the OS to detect the device
3. Flash a .hex file (May be done automatically)
4. Reset the device into application mode (May be done automatically)

or:

    make flash-<board> USER_KEYMAP=user_keymaps/...

Example:

	make flash-feather-m4-express USER_KEYMAP=user_keymaps/kdb424/handwire_planck_featherm4.py


