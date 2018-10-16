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

all: copy-kmk copy-keymap

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
ifndef USER_KEYMAP
$(MOUNTPOINT)/main.py:
	@echo "**** USER_KEYMAP must be defined (ex. USER_KEYMAP=user_keymaps/noop.py) ****" && exit 1
else
$(MOUNTPOINT)/main.py: $(USER_KEYMAP)
	@echo "===> Copying your keymap to main.py"
	@rsync -rh $(USER_KEYMAP) $@
	@sync
endif # USER_KEYMAP

copy-keymap: $(MOUNTPOINT)/main.py
else
copy-keymap:
	echo "**** MOUNTPOINT must be defined (wherever your CIRCUITPY drive is mounted) ****" && exit 1
endif # MOUNTPOINT
