.PHONY: \
	build-feather \
	circuitpy-deps \
	circuitpy-freeze-kmk-nrf \
	devdeps \
	freeze-nrf-build-deps \
	lint

AMPY_PORT ?= /dev/ttyUSB0
AMPY_BAUD ?= 115200
AMPY_DELAY ?= 1.5
ARDUINO ?= /usr/share/arduino
PIPENV ?= $(shell which pipenv)

devdeps: Pipfile.lock
	@$(PIPENV) install --dev --ignore-pipfile

lint: devdeps
	@$(PIPENV) run flake8

fix-isort: devdeps
	@find kmk/ user_keymaps/ -name "*.py" | xargs $(PIPENV) run isort

clean:
	rm -rf .submodules .circuitpy-deps .micropython-deps build

powerwash: clean
	rm -rf vendor
	$(PIPENV) --rm

test: micropython-build-unix
	@echo "===> Testing keymap_sanity_check.py script"
	@echo "    --> Known good layout should pass..."
	@MICROPYPATH=tests/test_data:./ ./bin/micropython.sh bin/keymap_sanity_check.py keymaps/known_good.py
	@echo "    --> Layer with ghosted MO should fail..."
	@MICROPYPATH=tests/test_data:./ ./bin/micropython.sh bin/keymap_sanity_check.py keymaps/ghosted_layer_mo.py 2>/dev/null && exit 1 || exit 0
	@echo "    --> Sharing a pin between rows/cols should fail..."
	@MICROPYPATH=tests/test_data:./ ./bin/micropython.sh bin/keymap_sanity_check.py keymaps/duplicated_pins_between_row_col.py 2>/dev/null && exit 1 || exit 0
	@echo "    --> Sharing a pin between two rows should fail..."
	@MICROPYPATH=tests/test_data:./ ./bin/micropython.sh bin/keymap_sanity_check.py keymaps/duplicate_row_pins.py 2>/dev/null && exit 1 || exit 0
	@echo "===> The sanity checker is sane, unlike klardotsh"

.submodules: .gitmodules submodules.toml
	@echo "===> Pulling dependencies, this may take several minutes"
	@git submodule update --init --recursive
	@rsync -avh vendor/ build/
	@touch .submodules

.circuitpy-deps: .submodules
	@echo "===> Building circuitpython/mpy-cross"
	@make -C build/circuitpython/mpy-cross
	@echo "===> Pulling Nordic BLE stack"
	@cd build/circuitpython/ports/nrf && ./drivers/bluetooth/download_ble_stack.sh 2>/dev/null >/dev/null
	@touch .circuitpy-deps

.micropython-deps: .submodules
	@echo "===> Building micropython/mpy-cross"
	@make -C build/micropython/mpy-cross
	@touch .micropython-deps

submodules: .submodules
circuitpy-deps: .circuitpy-deps
micropython-deps: .micropython-deps

build/micropython/ports/unix/micropython: micropython-deps build/micropython/ports/unix/modules/.kmk_frozen
	@make -j4 -C build/micropython/ports/unix

micropython-build-unix: build/micropython/ports/unix/micropython

freeze-nrf-build-deps: build/circuitpython/ports/nrf/freeze/.kmk_frozen
freeze-teensy3.1-build-deps: build/micropython/ports/teensy/freeze/.kmk_frozen
freeze-stm32-build-deps: build/micropython/ports/stm32/freeze/.kmk_frozen

build/micropython/ports/unix/modules/.kmk_frozen: upy-freeze.txt
	@echo "===> Preparing builded dependencies for local development"
	@rm -rf build/micropython/ports/unix/freeze/*
	@cat $< | xargs -I '{}' cp -a {} build/micropython/ports/unix/modules/
	@touch $@

build/circuitpython/ports/nrf/freeze/.kmk_frozen: upy-freeze.txt
	@echo "===> Preparing builded dependencies for bundling"
	@rm -rf build/circuitpython/ports/nrf/freeze/*
	@cat $< | xargs -I '{}' cp -a {} build/circuitpython/ports/nrf/freeze/
	@touch $@

build/micropython/ports/teensy/freeze/.kmk_frozen: upy-freeze.txt
	@echo "===> Preparing builded dependencies for bundling"
	@mkdir -p build/micropython/ports/teensy/freeze/
	@rm -rf build/micropython/ports/teensy/freeze/*
	@cat $< | xargs -I '{}' cp -a {} build/micropython/ports/teensy/freeze/
	@touch $@

build/micropython/ports/stm32/freeze/.kmk_frozen: upy-freeze.txt
	@echo "===> Preparing builded dependencies for bundling"
	@mkdir -p build/micropython/ports/stm32/freeze/
	@rm -rf build/micropython/ports/stm32/freeze/*
	@cat $< | xargs -I '{}' cp -a {} build/micropython/ports/stm32/freeze/
	@touch $@

circuitpy-freeze-kmk-nrf: freeze-nrf-build-deps
	@echo "===> Preparing KMK source for bundling into CircuitPython"
	@rm -rf build/circuitpython/ports/nrf/kmk*
	@cp -av kmk build/circuitpython/ports/nrf/freeze/

micropython-freeze-kmk-teensy3.1: freeze-teensy3.1-build-deps
	@echo "===> Preparing KMK source for bundling into MicroPython"
	@rm -rf build/micropython/ports/teensy/kmk*
	@cp -av kmk build/micropython/ports/teensy/memzip_files/

micropython-freeze-kmk-stm32: freeze-stm32-build-deps
	@echo "===> Preparing KMK source for bundling into MicroPython"
	@rm -rf build/micropython/ports/stm32/freeze/kmk*
	@cp -av kmk build/micropython/ports/stm32/freeze/

circuitpy-build-nrf:
	@echo "===> Building CircuitPython"
	@make -C build/circuitpython/ports/nrf BOARD=feather_nrf52832 SERIAL=${AMPY_PORT} SD=s132 FROZEN_MPY_DIR=freeze clean all

circuitpy-flash-nrf: circuitpy-build-nrf
	@echo "===> Flashing CircuitPython with KMK and your keymap"
	@make -C build/circuitpython/ports/nrf BOARD=feather_nrf52832 SERIAL=${AMPY_PORT} SD=s132 FROZEN_MPY_DIR=freeze dfu-gen dfu-flash

micropython-build-teensy3.1:
	@make -C build/micropython/ports/teensy/ BOARD=TEENSY_3.1 all

micropython-flash-teensy3.1: micropython-build-teensy3.1
	@make -C build/micropython/ports/teensy/ BOARD=TEENSY_3.1 deploy

micropython-build-pyboard:
	@make -j4 -C build/micropython/ports/stm32/ BOARD=PYBV11 FROZEN_MPY_DIR=freeze all

micropython-flash-pyboard: micropython-build-pyboard
	@make -j4 -C build/micropython/ports/stm32/ BOARD=PYBV11 FROZEN_MPY_DIR=freeze deploy

circuitpy-flash-nrf-entrypoint:
	@echo "===> Flashing entrypoint if it doesn't already exist"
	@sleep 2
	@-timeout -k 5s 10s $(PIPENV) run ampy -p ${AMPY_PORT} -d ${AMPY_DELAY} -b ${AMPY_BAUD} rm main.py 2>/dev/null
	@-timeout -k 5s 10s $(PIPENV) run ampy -p ${AMPY_PORT} -d ${AMPY_DELAY} -b ${AMPY_BAUD} put entrypoints/feather_nrf52832.py main.py
	@echo "===> Flashed keyboard successfully!"

ifndef USER_KEYMAP
build-feather-nrf52832:
	@echo "===> Must provide a USER_KEYMAP (usually from user_keymaps/...) to build!" && exit 1

flash-feather-nrf52832:
	@echo "===> Must provide a USER_KEYMAP (usually from user_keymaps/...) to build!" && exit 1
else
build-feather-nrf52832: lint devdeps circuitpy-deps circuitpy-freeze-kmk-nrf
	@echo "===> Preparing keyboard script for bundling into CircuitPython"
	@cp -av ${USER_KEYMAP} build/circuitpython/ports/nrf/freeze/kmk_keyboard_user.py
	@$(MAKE) circuitpy-build-nrf

flash-feather-nrf52832: lint devdeps circuitpy-deps circuitpy-freeze-kmk-nrf
	@echo "===> Preparing keyboard script for bundling into CircuitPython"
	@cp -av ${USER_KEYMAP} build/circuitpython/ports/nrf/freeze/kmk_keyboard_user.py
	@$(MAKE) circuitpy-flash-nrf circuitpy-flash-nrf-entrypoint
endif

ifndef USER_KEYMAP
build-teensy-3.1:
	@echo "===> Must provide a USER_KEYMAP (usually from user_keymaps/...) to build!" && exit 1

flash-teensy-3.1:
	@echo "===> Must provide a USER_KEYMAP (usually from user_keymaps/...) to build!" && exit 1
else
build-teensy-3.1: lint devdeps micropython-deps micropython-freeze-kmk-teensy3.1
	@echo "===> Preparing keyboard script for bundling into MicroPython"
	@cp -av ${USER_KEYMAP} build/micropython/ports/teensy/freeze/kmk_keyboard_user.py
	@$(MAKE) ARDUINO=${ARDUINO} micropython-build-teensy3.1

flash-teensy-3.1: lint devdeps micropython-deps micropython-freeze-kmk-teensy3.1
	@echo "===> Preparing keyboard script for bundling into MicroPython"
	@cp -av ${USER_KEYMAP} build/micropython/ports/teensy/freeze/kmk_keyboard_user.py
	@$(MAKE) ARDUINO=${ARDUINO} micropython-flash-teensy3.1
endif

ifndef USER_KEYMAP
build-pyboard:
	@echo "===> Must provide a USER_KEYMAP (usually from user_keymaps/...) to build!" && exit 1

flash-pyboard:
	@echo "===> Must provide a USER_KEYMAP (usually from user_keymaps/...) to build!" && exit 1
else
ifndef SKIP_KEYMAP_VALIDATION
build-pyboard: lint devdeps micropython-deps micropython-freeze-kmk-stm32 micropython-build-unix
else
build-pyboard: lint devdeps micropython-deps micropython-freeze-kmk-stm32
endif
	@echo "===> Preparing keyboard script for bundling into MicroPython"
ifndef SKIP_KEYMAP_VALIDATION
	@MICROPYPATH=./ ./bin/micropython.sh bin/keymap_sanity_check.py ${USER_KEYMAP}
endif
	@cp -av ${USER_KEYMAP} build/micropython/ports/stm32/freeze/kmk_keyboard_user.py
	@$(MAKE) AMPY_PORT=/dev/ttyACM0 AMPY_BAUD=115200 micropython-build-pyboard

flash-pyboard: lint devdeps micropython-deps micropython-freeze-kmk-stm32
	@echo "===> Preparing keyboard script for bundling into MicroPython"
	@cp -av ${USER_KEYMAP} build/micropython/ports/stm32/freeze/kmk_keyboard_user.py
	@cp -av kmk/entrypoints/global.py build/micropython/ports/stm32/freeze/_main.py
	@cp -av kmk/entrypoints/handwire/pyboard_boot.py build/micropython/ports/stm32/freeze/_boot.py
	@$(MAKE) micropython-flash-pyboard
endif

reset-bootloader:
	@-timeout -k 5s 10s $(PIPENV) run ampy -p /dev/ttyACM0 -d ${AMPY_DELAY} -b ${AMPY_BAUD} run util/bootloader.py

reset-board:
	@-timeout -k 5s 10s $(PIPENV) run ampy -p /dev/ttyACM0 -d ${AMPY_DELAY} -b ${AMPY_BAUD} run util/reset.py

# Fully wipe the board with only stock CircuitPython
burn-it-all-with-fire: lint devdeps
	@echo "===> Flashing STOCK CircuitPython with no KMK or user keyboard scripts, and wiping entrypoint"
	@echo "===> This is the nuclear option. Ctrl-C to cancel, or any key to continue"
	@read
	@echo "===> Pulling dependencies, this may take several minutes"
	@git submodule update --init --recursive
	@echo "===> Building circuitpython/mpy-cross"
	@make -C build/circuitpython/mpy-cross
	@echo "===> Pulling Nordic BLE stack"
	@cd build/circuitpython/ports/nrf && ./drivers/bluetooth/download_ble_stack.sh 2>/dev/null >/dev/null
	@echo "===> Preparing KMK source for bundling into CircuitPython"
	@rm -rf build/circuitpython/ports/nrf/*
	@echo "===> Building CircuitPython WITHOUT KMK or user keyboard script to induce ImportError"
	@$(MAKE) circuitpy-flash-nrf
	@echo "===> Wiping keyboard config"
	@sleep 2
	@-timeout -k 5s 10s $(PIPENV) run ampy -p ${AMPY_PORT} -d ${AMPY_DELAY} -b ${AMPY_BAUD} rm main.py 2>/dev/null
	@echo "===> Wiped! Probably safe to flash keyboard, try Python serial REPL to verify?"
