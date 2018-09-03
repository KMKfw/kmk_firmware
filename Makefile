.PHONY: \
	build-feather \
	circuitpy-deps \
	circuitpy-freeze-kmk-nrf \
	devdeps \
	freeze-nrf-vendor-deps \
	lint

NRF_DFU_PORT ?= /dev/ttyUSB0
NRF_DFU_BAUD ?= 115200
NRF_DFU_DELAY ?= 1.5

devdeps: Pipfile.lock
	@pipenv install --dev --ignore-pipfile

lint: devdeps
	@pipenv run flake8

.submodules: .gitmodules
	@echo "===> Pulling dependencies, this may take several minutes"
	@git submodule update --init --recursive
	@touch .submodules

.circuitpy-deps: .submodules
	@echo "===> Building circuitpython/mpy-cross"
	@make -C vendor/circuitpython/mpy-cross
	@echo "===> Pulling Nordic BLE stack"
	@cd vendor/circuitpython/ports/nrf && ./drivers/bluetooth/download_ble_stack.sh 2>/dev/null >/dev/null
	@touch .circuitpy-deps

circuitpy-deps: .circuitpy-deps

freeze-nrf-vendor-deps: vendor/circuitpython/ports/nrf/freeze/.kmk_frozen

vendor/circuitpython/ports/nrf/freeze/.kmk_frozen: upy-freeze.txt
	@echo "===> Preparing vendored dependencies for bundling"
	@rm -rf vendor/circuitpython/ports/nrf/freeze/*
	@cat $< | xargs -I '{}' cp -a {} vendor/circuitpython/ports/nrf/freeze/
	@touch $@

circuitpy-freeze-kmk-nrf: freeze-nrf-vendor-deps
	@echo "===> Preparing KMK source for bundling into CircuitPython"
	@rm -rf vendor/circuitpython/ports/nrf/kmk*
	@cp -av kmk vendor/circuitpython/ports/nrf/freeze/

circuitpy-flash-nrf:
	@echo "===> Building and flashing CircuitPython with KMK and your keymap"
	@make -C vendor/circuitpython/ports/nrf BOARD=feather_nrf52832 SERIAL=${NRF_DFU_PORT} SD=s132 FROZEN_MPY_DIR=freeze clean dfu-gen dfu-flash

circuitpy-flash-nrf-entrypoint:
	@echo "===> Flashing entrypoint if it doesn't already exist"
	@sleep 2
	@-timeout -k 5s 10s pipenv run ampy -p ${NRF_DFU_PORT} -d ${NRF_DFU_DELAY} -b ${NRF_DFU_BAUD} rm main.py 2>/dev/null
	@-timeout -k 5s 10s pipenv run ampy -p ${NRF_DFU_PORT} -d ${NRF_DFU_DELAY} -b ${NRF_DFU_BAUD} put entrypoints/feather_nrf52832.py main.py
	@echo "===> Flashed keyboard successfully!"

build-feather-test: lint devdeps circuitpy-deps circuitpy-freeze-kmk-nrf
	@echo "===> Preparing keyboard script for bundling into CircuitPython"
	@cp -av boards/klardotsh/twotwo_matrix_feather.py vendor/circuitpython/ports/nrf/freeze/kmk_keyboard_user.py
	@$(MAKE) circuitpy-flash-nrf circuitpy-flash-nrf-entrypoint

build-feather-noop: lint devdeps circuitpy-deps circuitpy-freeze-kmk-nrf
	@echo "===> Preparing keyboard script for bundling into CircuitPython"
	@cp -av boards/noop.py vendor/circuitpython/ports/nrf/freeze/kmk_keyboard_user.py
	@$(MAKE) circuitpy-flash-nrf circuitpy-flash-nrf-entrypoint

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
	@rm -rf vendor/circuitpython/ports/nrf/*
	@echo "===> Building CircuitPython WITHOUT KMK or user keyboard script to induce ImportError"
	@$(MAKE) circuitpy-flash-nrf
	@echo "===> Wiping keyboard config"
	@sleep 2
	@-timeout -k 5s 10s pipenv run ampy -p ${NRF_DFU_PORT} -d ${NRF_DFU_DELAY} -b ${NRF_DFU_BAUD} rm main.py 2>/dev/null
	@echo "===> Wiped! Probably safe to flash keyboard, try Python serial REPL to verify?"
