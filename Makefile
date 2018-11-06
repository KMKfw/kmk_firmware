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
	@rm -rf .submodules .circuitpy-deps .devdeps build

clean-build-log:
	@echo "===> Clearing previous .build.log"
	@rm -rf .build.log

powerwash: clean
	@echo "===> Removing vendor/ to force a re-pull"
	@rm -rf vendor
	@echo "===> Removing pipenv-managed virtual environment"
	@$(PIPENV) --rm || true

test: lint

.submodules: .gitmodules submodules.toml
	@echo "===> Pulling dependencies, this may take several minutes"
	@echo "===> Pulling dependencies, this may take several minutes" >> .build.log
	@git submodule sync 2>&1 >> .build.log
	@git submodule update --init --recursive 2>&1 >> .build.log
	@rsync -ah vendor/ build/
	@touch .submodules

submodules: .submodules

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
