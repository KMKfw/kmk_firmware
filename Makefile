.SILENT:

.PHONY: \
	devdeps \
	lint

.DEFAULT: all

DIST_DESCRIBE_CMD = git describe --always --abbrev=0 --dirty --broken

DOCKER_BASE_TAG ?= latest
DOCKER_TAG ?= latest

AMPY_PORT ?= /dev/ttyUSB0
AMPY_BAUD ?= 115200
AMPY_DELAY ?= 1.5
PIPENV ?= $(shell which pipenv 2>/dev/null)

MPY_CROSS ?= $(shell which mpy-cross 2>/dev/null)
MPY_FLAGS ?= '-O2'
MPY_SOURCES = 'kmk/'
MPY_TARGET_DIR ?= .compiled

all: copy-kmk copy-bootpy copy-keymap

compile: $(MPY_TARGET_DIR)/.mpy.compiled

$(MPY_TARGET_DIR)/.mpy.compiled: $(shell find $(MPY_SOURCES) -name "*.py")
ifeq ($(MPY_CROSS),)
	@echo "===> Could not find mpy-cross in PATH, exiting"
	@false
endif
	@mkdir -p $(MPY_TARGET_DIR)
	@find $(MPY_SOURCES) -name "*.py" -exec sh -c 'mkdir -p $(MPY_TARGET_DIR)/$$(dirname {}) && mpy-cross $(MPY_FLAGS) {} -o $(MPY_TARGET_DIR)/$$(dirname {})/$$(basename -s .py {}).mpy' \;
	@touch $(MPY_TARGET_DIR)/.mpy.compiled

dist: dist/latest.zip dist/latest.unoptimized.zip dist/$(shell $(DIST_DESCRIBE_CMD)).zip dist/$(shell $(DIST_DESCRIBE_CMD)).unoptimized.zip

dist/latest.zip: compile
	@mkdir -p dist
	@cd $(MPY_TARGET_DIR) && zip -r ../dist/latest.zip kmk

dist/$(shell $(DIST_DESCRIBE_CMD)).zip: dist/latest.zip
	@cp dist/latest.zip dist/$$($(DIST_DESCRIBE_CMD)).zip

dist/latest.unoptimized.zip:
	@mkdir -p dist
	@zip -r dist/latest.unoptimized.zip kmk

dist/$(shell $(DIST_DESCRIBE_CMD)).unoptimized.zip: dist/latest.unoptimized.zip
	@cp dist/latest.unoptimized.zip dist/$$($(DIST_DESCRIBE_CMD)).unoptimized.zip

.docker_base: Dockerfile
	@echo "===> Building Docker base image kmkfw/base:${DOCKER_BASE_TAG}"
	@docker build -t kmkfw/base:${DOCKER_BASE_TAG} .
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
	@rm -rf .devdeps build dist $(MPY_TARGET_DIR)

clean-build-log:
	@echo "===> Clearing previous .build.log"
	@rm -rf .build.log

# This is mostly a leftover from the days we vendored stuff from
# micropython-lib via submodules. Leaving this here mostly in case someone goes
# exploring through the history of KMK's repo and manages to screw up their
# repo state (those were glitchy times...)
powerwash: clean
	@echo "===> Removing vendor/ to force a re-pull"
	@rm -rf vendor
	@echo "===> Removing pipenv-managed virtual environment"
	@$(PIPENV) --rm || true

test: lint

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
	@touch $(MOUNTPOINT)/kmk/.copied
	@sync

copy-kmk: $(MOUNTPOINT)/kmk/.copied
else
copy-kmk:
	echo "**** MOUNTPOINT must be defined (wherever your CIRCUITPY drive is mounted) ****" && exit 1
endif

ifdef MOUNTPOINT
$(MOUNTPOINT)/kmk/boot.py: boot.py
	@echo "===> Copying required boot.py"
	@rsync -rh boot.py $(MOUNTPOINT)/
	@sync

copy-bootpy: $(MOUNTPOINT)/kmk/boot.py
else
copy-bootpy:
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
