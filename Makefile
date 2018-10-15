.SILENT:

.PHONY: \
	devdeps \
	lint

.DEFAULT: all

DOCKER_BASE_TAG ?= latest
DOCKER_TAG ?= latest

AMPY_PORT ?= /dev/ttyUSB0
AMPY_BAUD ?= 115200
AMPY_DELAY ?= 1.5
ARDUINO ?= /usr/share/arduino
PIPENV ?= $(shell which pipenv)

all: copy-kmk copy-keymap copy-main.py

.docker_base: Dockerfile_base
	@echo "===> Building Docker base image kmkfw/base:${DOCKER_BASE_TAG}"
	@docker build -f Dockerfile_base -t kmkfw/base:${DOCKER_BASE_TAG} .
	@touch .docker_base

docker-base: .docker_base

docker-base-deploy: docker-base
	@echo "===> Pushing Docker base image kmkfw/base:${DOCKER_BASE_TAG} to Docker Hub"
	@docker push kmkfw/base:${DOCKER_BASE_TAG}

.devdeps: Pipfile.lock
	@echo "===> Installing dependencies with pipenv"
	@$(PIPENV) install --dev --ignore-pipfile
	@touch .devdeps

devdeps: .devdeps

lint: devdeps
	@$(PIPENV) run flake8

fix-isort: devdeps
	@find kmk/ tests/ user_keymaps/ -name "*.py" | xargs $(PIPENV) run isort

clean: clean-build-log
	@echo "===> Cleaning build artifacts"
	@rm -rf .submodules .circuitpy-deps .micropython-deps .devdeps build

clean-build-log:
	@echo "===> Clearing previous .build.log"
	@rm -rf .build.log

powerwash: clean
	@echo "===> Removing vendor/ to force a re-pull"
	@rm -rf vendor
	@echo "===> Removing pipenv-managed virtual environment"
	@$(PIPENV) --rm || true

test: lint micropython-build-unix
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
	@echo "===> Pulling dependencies, this may take several minutes" >> .build.log
	@git submodule sync 2>&1 >> .build.log
	@git submodule update --init --recursive 2>&1 >> .build.log
	@rsync -ah vendor/ build/
	@touch .submodules

.micropython-deps: .submodules
	@echo "===> Building micropython/mpy-cross"
	@echo "===> Building micropython/mpy-cross" >> .build.log
	@pipenv run $(MAKE) -C build/micropython/mpy-cross 2>&1 >> .build.log
	@touch .micropython-deps

submodules: .submodules
micropython-deps: .micropython-deps

build/micropython/ports/unix/micropython: micropython-deps build/micropython/ports/unix/modules/.kmk_frozen
	@echo "===> Building MicroPython for Unix"
	@echo "===> Building MicroPython for Unix" >> .build.log
	@pipenv run $(MAKE) -j4 -C build/micropython/ports/unix 2>&1 >> .build.log

micropython-build-unix: build/micropython/ports/unix/micropython

build/micropython/ports/unix/modules/.kmk_frozen: upy-freeze.txt submodules.toml
	@echo "===> Preparing vendored dependencies for bundling into MicroPython for Unix"
	@echo "===> Preparing vendored dependencies for bundling into MicroPython for Unix" >> .build.log
	@rm -rf build/micropython/ports/unix/modules/*
	@cat upy-freeze.txt | egrep -v '(^#|^\s*$|^\s*\t*#)' | grep MICROPY | cut -d'|' -f2- | \
		xargs -I '{}' rsync -ah {} build/micropython/ports/unix/modules/
	@touch $@

build/micropython/ports/stm32/freeze/.kmk_frozen: upy-freeze.txt submodules.toml
	@echo "===> Preparing vendored dependencies for bundling into MicroPython for STM32"
	@echo "===> Preparing vendored dependencies for bundling into MicroPython for STM32" >> .build.log
	@mkdir -p build/micropython/ports/stm32/freeze/
	@rm -rf build/micropython/ports/stm32/freeze/*
	@cat upy-freeze.txt | egrep -v '(^#|^\s*$|^\s*\t*#)' | grep MICROPY | cut -d'|' -f2- | \
		xargs -I '{}' rsync -ah {} build/micropython/ports/stm32/freeze/
	@touch $@

micropython-freeze-kmk-stm32: freeze-stm32-build-deps
	@echo "===> Preparing KMK source for bundling into MicroPython for STM32"
	@echo "===> Preparing KMK source for bundling into MicroPython for STM32" >> .build.log
	@rm -rf build/micropython/ports/stm32/freeze/kmk*
	@rsync -ah kmk build/micropython/ports/stm32/freeze/ --exclude kmk/circuitpython

micropython-build-pyboard:
	@echo "===> Building MicroPython for STM32 - PYBV11"
	@echo "===> Building MicroPython for STM32 - PYBV11" >> .build.log
	@pipenv run $(MAKE) -j4 -C build/micropython/ports/stm32/ BOARD=PYBV11 FROZEN_MPY_DIR=freeze all 2>&1 >> .build.log

micropython-flash-pyboard: micropython-build-pyboard
	@echo "===> Flashing MicroPython with KMK and your keymap"
	@echo "===> Flashing MicroPython with KMK and your keymap" >> .build.log
	@pipenv run $(MAKE) -j4 -C build/micropython/ports/stm32/ BOARD=PYBV11 FROZEN_MPY_DIR=freeze deploy 2>&1 >> .build.log

ifndef USER_KEYMAP
build-pyboard:
	@echo "===> Must provide a USER_KEYMAP (usually from user_keymaps/...) to build!" && exit 1

flash-pyboard:
	@echo "===> Must provide a USER_KEYMAP (usually from user_keymaps/...) to build!" && exit 1
else
ifndef SKIP_KEYMAP_VALIDATION
build-pyboard: clean-build-log lint micropython-deps micropython-freeze-kmk-stm32 micropython-build-unix
else
build-pyboard: clean-build-log lint micropython-deps micropython-freeze-kmk-stm32
endif
	@echo "===> Preparing keyboard script for bundling into MicroPython for STM32"
ifndef SKIP_KEYMAP_VALIDATION
	@MICROPYPATH=./ ./bin/micropython.sh bin/keymap_sanity_check.py ${USER_KEYMAP}
endif
	@rsync -ah ${USER_KEYMAP} build/micropython/ports/stm32/freeze/main.py
	@rsync -ah kmk/entrypoints/global.py build/micropython/ports/stm32/freeze/_main.py
	@rsync -ah kmk/entrypoints/handwire/pyboard_boot.py build/micropython/ports/stm32/freeze/_boot.py
	@$(MAKE) AMPY_PORT=/dev/ttyACM0 AMPY_BAUD=115200 micropython-build-pyboard

flash-pyboard: build-pyboard micropython-flash-pyboard
endif

reset-bootloader:
	@echo "===> Rebooting your board to bootloader (safe to ignore file not found errors)"
	@-timeout -k 5s 10s $(PIPENV) run ampy -p /dev/ttyACM0 -d ${AMPY_DELAY} -b ${AMPY_BAUD} run util/bootloader.py

reset-board:
	@echo "===> Rebooting your board (safe to ignore file not found errors)"
	@-timeout -k 5s 10s $(PIPENV) run ampy -p /dev/ttyACM0 -d ${AMPY_DELAY} -b ${AMPY_BAUD} run util/reset.py

ifdef MOUNTPOINT
$(MOUNTPOINT)/kmk/.copied: $(shell find kmk/ -name "*.py" | xargs -0)
	@echo "===> Copying KMK source folder"
	@rsync -rh kmk $(MOUNTPOINT)/
	@cat upy-freeze.txt | egrep -v '(^#|^\s*$|^\s*\t*#)' | grep CIRCUITPY | cut -d'|' -f2- | \
		xargs -I '{}' rsync -h {} $(MOUNTPOINT)/
	@touch $(MOUNTPOINT)/kmk/.copied
	@sync

copy-kmk: $(MOUNTPOINT)/kmk/.copied
else
copy-kmk:
	echo "**** MOUNTPOINT must be defined (wherever your CIRCUITPY drive is mounted) ****" && exit 1
endif

ifdef MOUNTPOINT
$(MOUNTPOINT)/main.py: main.py
	@echo "===> Copying a basic main.py"
	@rsync -rh main.py $@
	@sync

copy-main.py: $(MOUNTPOINT)/main.py
else
copy-main.py:
	echo "**** MOUNTPOINT must be defined (wherever your CIRCUITPY drive is mounted) ****" && exit 1
endif

ifdef MOUNTPOINT
ifndef USER_KEYMAP
$(MOUNTPOINT)/kmk_keyboard.py:
	@echo "**** USER_KEYMAP must be defined (ex. USER_KEYMAP=user_keymaps/noop.py) ****" && exit 1
else
$(MOUNTPOINT)/kmk_keyboard.py: $(USER_KEYMAP)
	@echo "===> Copying your keymap to kmk_keyboard.py"
	@rsync -rh $(USER_KEYMAP) $@
	@sync
endif # USER_KEYMAP

copy-keymap: $(MOUNTPOINT)/kmk_keyboard.py
else
copy-keymap:
	echo "**** MOUNTPOINT must be defined (wherever your CIRCUITPY drive is mounted) ****" && exit 1
endif # MOUNTPOINT
