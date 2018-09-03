.PHONY: build-feather devdeps lint

devdeps: Pipfile.lock
	pipenv install --dev --ignore-pipfile

lint: devdeps
	pipenv run flake8

build-feather-test: lint devdeps
	@echo "===> Pulling dependencies, this may take several minutes"
	@git submodule update --init --recursive
	@echo "===> Building circuitpython/mpy-cross"
	@make -C vendor/circuitpython/mpy-cross
	@echo "===> Pulling Nordic BLE stack"
	@cd vendor/circuitpython/ports/nrf && ./drivers/bluetooth/download_ble_stack.sh 2>/dev/null >/dev/null
	@echo "===> Preparing KMK source for bundling into CircuitPython"
	@rm -rf vendor/circuitpython/ports/nrf/freeze/kmk
	@rm -rf vendor/circuitpython/ports/nrf/freeze/kmk_keyboard_user.py
	@cp -av kmk vendor/circuitpython/ports/nrf/freeze/
	@cp -av boards/klardotsh/twotwo_matrix_feather.py vendor/circuitpython/ports/nrf/freeze/kmk_keyboard_user.py
	@echo "===> Building and flashing CircuitPython with KMK and your keymap"
	@make -C vendor/circuitpython/ports/nrf BOARD=feather_nrf52832 SERIAL=/dev/ttyUSB0 SD=s132 FROZEN_MPY_DIR=freeze clean dfu-gen dfu-flash
	@echo "===> Flashing entrypoint if it doesn't already exist"
	@sleep 2
	@-timeout -k 5s 10s pipenv run ampy rm main.py 2>/dev/null
	@timeout -k 5s 10s pipenv run ampy put entrypoints/feather_nrf52832.py main.py
	@echo "===> Flashed keyboard successfully!"

# Fully wipe the board with only stock CircuitPython
burn-it-all-with-fire: lint devdeps
	@echo "===> Flashing STOCK CircuitPython with no KMK or user keyboard scripts, and wiping entrypoint"
	@echo "===> This is the nuclear option. Ctrl-C to cancel, or any key to continue"
	@read
	@echo "===> Pulling dependencies, this may take several minutes"
	@git submodule update --init --recursive
	@echo "===> Building circuitpython/mpy-cross"
	@make -C vendor/circuitpython/mpy-cross
	@echo "===> Pulling Nordic BLE stack"
	@cd vendor/circuitpython/ports/nrf && ./drivers/bluetooth/download_ble_stack.sh 2>/dev/null >/dev/null
	@echo "===> Preparing KMK source for bundling into CircuitPython"
	@rm -rf vendor/circuitpython/ports/nrf/freeze/kmk
	@rm -rf vendor/circuitpython/ports/nrf/freeze/kmk_keyboard_user.py
	@echo "===> Building CircuitPython WITHOUT KMK or user keyboard script to induce ImportError"
	@make -C vendor/circuitpython/ports/nrf BOARD=feather_nrf52832 SERIAL=/dev/ttyUSB0 SD=s132 FROZEN_MPY_DIR=freeze clean dfu-gen dfu-flash
	@echo "===> Wiping keyboard config"
	@sleep 2
	@-pipenv run ampy rm main.py 2>/dev/null
	@echo "===> Wiped! Probably safe to flash keyboard, try Python serial REPL to verify?"
