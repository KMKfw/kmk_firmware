.PHONY: \
	build-feather \
	circuitpy-deps \
	circuitpy-freeze-kmk-nrf \
	devdeps \
	freeze-nrf-vendor-deps \
	lint

AMPY_PORT ?= /dev/ttyUSB0
AMPY_BAUD ?= 115200
AMPY_DELAY ?= 1.5
ARDUINO ?= /usr/share/arduino

devdeps: Pipfile.lock
	@pipenv install --dev --ignore-pipfile

lint: devdeps
	@pipenv run flake8

fix-isort: devdeps
	@find kmk/ boards/ entrypoints/ -name "*.py" | xargs pipenv run isort

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

.micropython-deps: .submodules
	@echo "===> Building micropython/mpy-cross"
	@make -C vendor/micropython/mpy-cross
	@touch .micropython-deps

circuitpy-deps: .circuitpy-deps

micropython-deps: .micropython-deps

freeze-nrf-vendor-deps: vendor/circuitpython/ports/nrf/freeze/.kmk_frozen
freeze-teensy3.1-vendor-deps: vendor/micropython/ports/teensy/freeze/.kmk_frozen
freeze-stm32-vendor-deps: vendor/micropython/ports/stm32/freeze/.kmk_frozen

vendor/circuitpython/ports/nrf/freeze/.kmk_frozen: upy-freeze.txt
	@echo "===> Preparing vendored dependencies for bundling"
	@rm -rf vendor/circuitpython/ports/nrf/freeze/*
	@cat $< | xargs -I '{}' cp -a {} vendor/circuitpython/ports/nrf/freeze/
	@touch $@

vendor/micropython/ports/teensy/freeze/.kmk_frozen: upy-freeze.txt
	@echo "===> Preparing vendored dependencies for bundling"
	@mkdir -p vendor/micropython/ports/teensy/freeze/
	@rm -rf vendor/micropython/ports/teensy/freeze/*
	@cat $< | xargs -I '{}' cp -a {} vendor/micropython/ports/teensy/freeze/
	@touch $@

vendor/micropython/ports/stm32/freeze/.kmk_frozen: upy-freeze.txt
	@echo "===> Preparing vendored dependencies for bundling"
	@mkdir -p vendor/micropython/ports/stm32/freeze/
	@rm -rf vendor/micropython/ports/stm32/freeze/*
	@cat $< | xargs -I '{}' cp -a {} vendor/micropython/ports/stm32/freeze/
	@touch $@

circuitpy-freeze-kmk-nrf: freeze-nrf-vendor-deps
	@echo "===> Preparing KMK source for bundling into CircuitPython"
	@rm -rf vendor/circuitpython/ports/nrf/kmk*
	@cp -av kmk vendor/circuitpython/ports/nrf/freeze/

micropython-freeze-kmk-teensy3.1: freeze-teensy3.1-vendor-deps
	@echo "===> Preparing KMK source for bundling into MicroPython"
	@rm -rf vendor/micropython/ports/teensy/kmk*
	@cp -av kmk vendor/micropython/ports/teensy/memzip_files/

micropython-freeze-kmk-stm32: freeze-stm32-vendor-deps
	@echo "===> Preparing KMK source for bundling into MicroPython"
	@rm -rf vendor/micropython/ports/stm32/freeze/kmk*
	@cp -av kmk vendor/micropython/ports/stm32/freeze/

circuitpy-build-nrf:
	@echo "===> Building CircuitPython"
	@make -C vendor/circuitpython/ports/nrf BOARD=feather_nrf52832 SERIAL=${AMPY_PORT} SD=s132 FROZEN_MPY_DIR=freeze clean all

circuitpy-flash-nrf: circuitpy-build-nrf
	@echo "===> Flashing CircuitPython with KMK and your keymap"
	@make -C vendor/circuitpython/ports/nrf BOARD=feather_nrf52832 SERIAL=${AMPY_PORT} SD=s132 FROZEN_MPY_DIR=freeze dfu-gen dfu-flash

micropython-build-teensy3.1:
	@cp entrypoints/teensy31.py vendor/micropython/ports/teensy/memzip_files/main.py
	@make -C vendor/micropython/ports/teensy/ BOARD=TEENSY_3.1 all

micropython-flash-teensy3.1: micropython-build-teensy3.1
	@make -C vendor/micropython/ports/teensy/ BOARD=TEENSY_3.1 deploy

micropython-build-pyboard:
	@make -j4 -C vendor/micropython/ports/stm32/ BOARD=PYBV11 FROZEN_MPY_DIR=freeze all

micropython-flash-pyboard: micropython-build-pyboard
	@make -j4 -C vendor/micropython/ports/stm32/ BOARD=PYBV11 FROZEN_MPY_DIR=freeze deploy

micropython-flash-pyboard-entrypoint:
	@echo "===> Flashing entrypoints if they doesn't already exist"
	@sleep 4
	@-timeout -k 5s 10s pipenv run ampy -p ${AMPY_PORT} -d ${AMPY_DELAY} -b ${AMPY_BAUD} rm /flash/main.py 2>/dev/null
	@-timeout -k 5s 10s pipenv run ampy -p ${AMPY_PORT} -d ${AMPY_DELAY} -b ${AMPY_BAUD} rm /flash/boot.py 2>/dev/null
	@-timeout -k 5s 10s pipenv run ampy -p ${AMPY_PORT} -d ${AMPY_DELAY} -b ${AMPY_BAUD} put entrypoints/pyboard.py /flash/main.py
	@-timeout -k 5s 10s pipenv run ampy -p ${AMPY_PORT} -d ${AMPY_DELAY} -b ${AMPY_BAUD} put entrypoints/pyboard_boot.py /flash/boot.py
	@echo "===> Flashed keyboard successfully!"

circuitpy-flash-nrf-entrypoint:
	@echo "===> Flashing entrypoint if it doesn't already exist"
	@sleep 2
	@-timeout -k 5s 10s pipenv run ampy -p ${AMPY_PORT} -d ${AMPY_DELAY} -b ${AMPY_BAUD} rm main.py 2>/dev/null
	@-timeout -k 5s 10s pipenv run ampy -p ${AMPY_PORT} -d ${AMPY_DELAY} -b ${AMPY_BAUD} put entrypoints/feather_nrf52832.py main.py
	@echo "===> Flashed keyboard successfully!"

ifndef BOARD
build-feather-nrf52832:
	@echo "===> Must provide a board (usually from boards/...) to build!"

flash-feather-nrf52832:
	@echo "===> Must provide a board (usually from boards/...) to build!"
else
build-feather-nrf52832: lint devdeps circuitpy-deps circuitpy-freeze-kmk-nrf
	@echo "===> Preparing keyboard script for bundling into CircuitPython"
	@cp -av ${BOARD} vendor/circuitpython/ports/nrf/freeze/kmk_keyboard_user.py
	@$(MAKE) circuitpy-build-nrf

flash-feather-nrf52832: lint devdeps circuitpy-deps circuitpy-freeze-kmk-nrf
	@echo "===> Preparing keyboard script for bundling into CircuitPython"
	@cp -av ${BOARD} vendor/circuitpython/ports/nrf/freeze/kmk_keyboard_user.py
	@$(MAKE) circuitpy-flash-nrf circuitpy-flash-nrf-entrypoint
endif

ifndef BOARD
build-teensy-3.1:
	@echo "===> Must provide a board (usually from boards/...) to build!"

flash-teensy-3.1:
	@echo "===> Must provide a board (usually from boards/...) to build!"
else
build-teensy-3.1: lint devdeps micropython-deps micropython-freeze-kmk-teensy3.1
	@echo "===> Preparing keyboard script for bundling into MicroPython"
	@cp -av ${BOARD} vendor/micropython/ports/teensy/freeze/kmk_keyboard_user.py
	@$(MAKE) ARDUINO=${ARDUINO} micropython-build-teensy3.1

flash-teensy-3.1: lint devdeps micropython-deps micropython-freeze-kmk-teensy3.1
	@echo "===> Preparing keyboard script for bundling into MicroPython"
	@cp -av ${BOARD} vendor/micropython/ports/teensy/freeze/kmk_keyboard_user.py
	@$(MAKE) ARDUINO=${ARDUINO} micropython-flash-teensy3.1
endif

ifndef BOARD
build-pyboard:
	@echo "===> Must provide a board (usually from boards/...) to build!"

flash-pyboard:
	@echo "===> Must provide a board (usually from boards/...) to build!"
else
build-pyboard: lint devdeps micropython-deps micropython-freeze-kmk-stm32
	@echo "===> Preparing keyboard script for bundling into MicroPython"
	@cp -av ${BOARD} vendor/micropython/ports/stm32/freeze/kmk_keyboard_user.py
	@$(MAKE) AMPY_PORT=/dev/ttyACM0 AMPY_BAUD=115200 micropython-build-pyboard

flash-pyboard: lint devdeps micropython-deps micropython-freeze-kmk-stm32
	@echo "===> Preparing keyboard script for bundling into MicroPython"
	@cp -av ${BOARD} vendor/micropython/ports/stm32/freeze/kmk_keyboard_user.py
	@$(MAKE) AMPY_PORT=/dev/ttyACM0 AMPY_BAUD=115200 micropython-flash-pyboard micropython-flash-pyboard-entrypoint
endif

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
	@-timeout -k 5s 10s pipenv run ampy -p ${AMPY_PORT} -d ${AMPY_DELAY} -b ${AMPY_BAUD} rm main.py 2>/dev/null
	@echo "===> Wiped! Probably safe to flash keyboard, try Python serial REPL to verify?"
