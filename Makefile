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

.devdeps: Pipfile.lock
	@$(PIPENV) install --dev --ignore-pipfile
	@touch .devdeps

devdeps: .devdeps

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
	@git submodule sync
	@git submodule update --init --recursive
	@rsync -ah vendor/ build/
	@touch .submodules

.circuitpy-deps: .submodules
	@echo "===> Building circuitpython/mpy-cross"
	@pipenv run $(MAKE) -C build/circuitpython/mpy-cross
	@echo "===> Pulling Nordic BLE stack"
	@cd build/circuitpython/ports/nrf && ./drivers/bluetooth/download_ble_stack.sh 2>/dev/null >/dev/null
	@touch .circuitpy-deps

.micropython-deps: .submodules
	@echo "===> Building micropython/mpy-cross"
	@pipenv run $(MAKE) -C build/micropython/mpy-cross
	@touch .micropython-deps

submodules: .submodules
circuitpy-deps: .circuitpy-deps
micropython-deps: .micropython-deps

build/micropython/ports/unix/micropython: micropython-deps build/micropython/ports/unix/modules/.kmk_frozen
	@pipenv run $(MAKE) -j4 -C build/micropython/ports/unix

micropython-build-unix: build/micropython/ports/unix/micropython

freeze-atmel-samd-build-deps: build/circuitpython/ports/atmel-samd/modules/.kmk_frozen
freeze-nrf-build-deps: build/circuitpython/ports/nrf/freeze/.kmk_frozen
freeze-stm32-build-deps: build/micropython/ports/stm32/freeze/.kmk_frozen

build/micropython/ports/unix/modules/.kmk_frozen: upy-freeze.txt submodules.toml
	@echo "===> Preparing builded dependencies for local development"
	@rm -rf build/micropython/ports/unix/modules/*
	@cat upy-freeze.txt | egrep -v '(^#|^\s*$|^\s*\t*#)' | grep MICROPY | cut -d'|' -f2- | \
		xargs -I '{}' cp -a {} build/micropython/ports/unix/modules/
	@touch $@

build/circuitpython/ports/atmel-samd/modules/.kmk_frozen: upy-freeze.txt submodules.toml
	@echo "===> Preparing builded dependencies for bundling"
	@rm -rf build/circuitpython/ports/atmel-samd/modules/*
	@cat upy-freeze.txt | egrep -v '(^#|^\s*$|^\s*\t*#)' | grep CIRCUITPY | cut -d'|' -f2- | \
		xargs -I '{}' cp -a {} build/circuitpython/ports/atmel-samd/modules/
	@touch $@

build/circuitpython/ports/nrf/freeze/.kmk_frozen: upy-freeze.txt submodules.toml
	@echo "===> Preparing builded dependencies for bundling"
	@rm -rf build/circuitpython/ports/nrf/freeze/*
	@cat upy-freeze.txt | egrep -v '(^#|^\s*$|^\s*\t*#)' | grep CIRCUITPY | cut -d'|' -f2- | \
		xargs -I '{}' cp -a {} build/circuitpython/ports/nrf/freeze/
	@touch $@

build/micropython/ports/stm32/freeze/.kmk_frozen: upy-freeze.txt submodules.toml
	@echo "===> Preparing builded dependencies for bundling"
	@mkdir -p build/micropython/ports/stm32/freeze/
	@rm -rf build/micropython/ports/stm32/freeze/*
	@cat upy-freeze.txt | egrep -v '(^#|^\s*$|^\s*\t*#)' | grep MICROPY | cut -d'|' -f2- | \
		xargs -I '{}' cp -a {} build/micropython/ports/stm32/freeze/
	@touch $@

circuitpy-freeze-kmk-atmel-samd: freeze-atmel-samd-build-deps
	@echo "===> Preparing KMK source for bundling into CircuitPython"
	@rm -rf build/circuitpython/ports/atmel-samd/modules/kmk*
	@rsync -ah kmk build/circuitpython/ports/atmel-samd/modules/

circuitpy-freeze-kmk-nrf: freeze-nrf-build-deps
	@echo "===> Preparing KMK source for bundling into CircuitPython"
	@rm -rf build/circuitpython/ports/nrf/kmk*
	@rsync -ah kmk build/circuitpython/ports/nrf/freeze/

micropython-freeze-kmk-stm32: freeze-stm32-build-deps
	@echo "===> Preparing KMK source for bundling into MicroPython"
	@rm -rf build/micropython/ports/stm32/freeze/kmk*
	@rsync -ah kmk build/micropython/ports/stm32/freeze/

circuitpy-build-feather-m4-express:
	@echo "===> Building CircuitPython"
	@pipenv run $(MAKE) -C build/circuitpython/ports/atmel-samd BOARD=feather_m4_express FROZEN_MPY_DIRS="modules" clean all

circuitpy-build-itsybitsy-m4-express:
	@echo "===> Building CircuitPython"
	@pipenv run $(MAKE) -C build/circuitpython/ports/atmel-samd BOARD=itsybitsy_m4_express FROZEN_MPY_DIRS="modules" clean all

circuitpy-build-nrf:
	@echo "===> Building CircuitPython"
	@pipenv run $(MAKE) -C build/circuitpython/ports/nrf BOARD=feather_nrf52832 SERIAL=${AMPY_PORT} SD=s132 FROZEN_MPY_DIR=freeze clean all

circuitpy-flash-feather-m4-express:
	@echo "Flashing not available for Feather M4 Express over bossa right now"
	@echo "First, double tap the reset button on the Feather. You should see a red light near the USB port"
	@echo "Then, find and (if necessary) mount the USB drive that will show up (should be about 4MB)"
	@echo "Copy build/circuitpython/ports/atmel-samd/build-feather_m4_express/firmware.uf2 to this device"
	@echo "The device will auto-reboot. You may need to forcibly unmount the drive on Linuxes, with umount -f path/to/mountpoint"

circuitpy-flash-itsybitsy-m4-express:
	@echo "Flashing not available for ItsyBitsy M4 Express over bossa right now"
	@echo "First, double tap the reset button on the ItsyBitsy. You should see a red light near the USB port"
	@echo "Then, find and (if necessary) mount the USB drive that will show up (should be about 4MB)"
	@echo "Copy build/circuitpython/ports/atmel-samd/build-itsybitsy_m4_express/firmware.uf2 to this device"
	@echo "The device will auto-reboot. You may need to forcibly unmount the drive on Linuxes, with umount -f path/to/mountpoint"

circuitpy-flash-nrf: circuitpy-build-nrf
	@echo "===> Flashing CircuitPython with KMK and your keymap"
	@pipenv run $(MAKE) -C build/circuitpython/ports/nrf BOARD=feather_nrf52832 SERIAL=${AMPY_PORT} SD=s132 FROZEN_MPY_DIR=freeze dfu-gen dfu-flash

micropython-build-pyboard:
	@pipenv run $(MAKE) -j4 -C build/micropython/ports/stm32/ BOARD=PYBV11 FROZEN_MPY_DIR=freeze all

micropython-flash-pyboard: micropython-build-pyboard
	@pipenv run $(MAKE) -j4 -C build/micropython/ports/stm32/ BOARD=PYBV11 FROZEN_MPY_DIR=freeze deploy

circuitpy-flash-nrf-entrypoint:
	@echo "===> Flashing entrypoint if it doesn't already exist"
	@sleep 2
	@-timeout -k 5s 10s $(PIPENV) run ampy -p ${AMPY_PORT} -d ${AMPY_DELAY} -b ${AMPY_BAUD} rm main.py 2>/dev/null
	@-timeout -k 5s 10s $(PIPENV) run ampy -p ${AMPY_PORT} -d ${AMPY_DELAY} -b ${AMPY_BAUD} put entrypoints/feather_nrf52832.py main.py
	@echo "===> Flashed keyboard successfully!"

ifndef USER_KEYMAP
build-feather-m4-express:
	@echo "===> Must provide a USER_KEYMAP (usually from user_keymaps/...) to build!" && exit 1

flash-feather-m4-express:
	@echo "===> Must provide a USER_KEYMAP (usually from user_keymaps/...) to build!" && exit 1
else
ifndef SKIP_KEYMAP_VALIDATION
build-feather-m4-express: lint devdeps circuitpy-deps circuitpy-freeze-kmk-atmel-samd
else
build-feather-m4-express: lint devdeps circuitpy-deps circuitpy-freeze-kmk-atmel-samd micropython-build-unix
endif
	@echo "===> Preparing keyboard script for bundling into CircuitPython"
ifndef SKIP_KEYMAP_VALIDATION
	@MICROPYPATH=./ ./bin/micropython.sh bin/keymap_sanity_check.py ${USER_KEYMAP}
endif
	@rsync -ah ${USER_KEYMAP} build/circuitpython/ports/atmel-samd/modules/kmk_keyboard_user.py
	@rsync -ah kmk/entrypoints/global.py build/circuitpython/ports/atmel-samd/modules/_main.py
	@$(MAKE) circuitpy-build-feather-m4-express

flash-feather-m4-express: build-feather-m4-express circuitpy-flash-feather-m4-express
endif

ifndef USER_KEYMAP
build-feather-nrf52832:
	@echo "===> Must provide a USER_KEYMAP (usually from user_keymaps/...) to build!" && exit 1

flash-feather-nrf52832:
	@echo "===> Must provide a USER_KEYMAP (usually from user_keymaps/...) to build!" && exit 1
else
build-feather-nrf52832: lint devdeps circuitpy-deps circuitpy-freeze-kmk-nrf
	@echo "===> Preparing keyboard script for bundling into CircuitPython"
	@rsync -ah ${USER_KEYMAP} build/circuitpython/ports/nrf/freeze/kmk_keyboard_user.py
	@$(MAKE) circuitpy-build-nrf

flash-feather-nrf52832: build-feather-nrf52832 circuitpy-flash-nrf circuitpy-flash-nrf-endpoint
endif

ifndef USER_KEYMAP
build-itsybitsy-m4-express:
	@echo "===> Must provide a USER_KEYMAP (usually from user_keymaps/...) to build!" && exit 1

flash-itsybitsy-m4-express:
	@echo "===> Must provide a USER_KEYMAP (usually from user_keymaps/...) to build!" && exit 1
else
ifndef SKIP_KEYMAP_VALIDATION
build-itsybitsy-m4-express: lint devdeps circuitpy-deps circuitpy-freeze-kmk-atmel-samd
else
build-itsybitsy-m4-express: lint devdeps circuitpy-deps circuitpy-freeze-kmk-atmel-samd micropython-build-unix
endif
	@echo "===> Preparing keyboard script for bundling into CircuitPython"
ifndef SKIP_KEYMAP_VALIDATION
	@MICROPYPATH=./ ./bin/micropython.sh bin/keymap_sanity_check.py ${USER_KEYMAP}
endif
	@rsync -ah ${USER_KEYMAP} build/circuitpython/ports/atmel-samd/modules/kmk_keyboard_user.py
	@rsync -ah kmk/entrypoints/global.py build/circuitpython/ports/atmel-samd/modules/_main.py
	@$(MAKE) circuitpy-build-itsybitsy-m4-express

flash-itsybitsy-m4-express: build-itsybitsy-m4-express circuitpy-flash-itsybitsy-m4-express
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
	@rsync -ah ${USER_KEYMAP} build/micropython/ports/stm32/freeze/kmk_keyboard_user.py
	@rsync -ah kmk/entrypoints/global.py build/micropython/ports/stm32/freeze/_main.py
	@rsync -ah kmk/entrypoints/handwire/pyboard_boot.py build/micropython/ports/stm32/freeze/_boot.py
	@$(MAKE) AMPY_PORT=/dev/ttyACM0 AMPY_BAUD=115200 micropython-build-pyboard

flash-pyboard: build-pyboard micropython-flash-pyboard
endif

reset-bootloader:
	@-timeout -k 5s 10s $(PIPENV) run ampy -p /dev/ttyACM0 -d ${AMPY_DELAY} -b ${AMPY_BAUD} run util/bootloader.py

reset-board:
	@-timeout -k 5s 10s $(PIPENV) run ampy -p /dev/ttyACM0 -d ${AMPY_DELAY} -b ${AMPY_BAUD} run util/reset.py
