.SILENT:

.PHONY: \
	clean-dist \
	devdeps \
	dist \
	dockerbase \
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
PY_KMK_TREE = $(shell find $(MPY_SOURCES) -name "*.py")
DIST_DESCRIBE = $(shell $(DIST_DESCRIBE_CMD))

TIMESTAMP := $(shell date +%s)

all: copy-kmk copy-bootpy copy-keymap copy-board

compile: $(MPY_TARGET_DIR)/.mpy.compiled

$(MPY_TARGET_DIR)/.mpy.compiled: $(PY_KMK_TREE)
ifeq ($(MPY_CROSS),)
	@echo "===> Could not find mpy-cross in PATH, exiting"
	@false
endif
	@echo "===> Compiling all py files to mpy with flags $(MPY_FLAGS)"
	@mkdir -p $(MPY_TARGET_DIR)
	@echo "KMK_RELEASE = '$(DIST_DESCRIBE)'" > $(MPY_SOURCES)/release_info.py
	@find $(MPY_SOURCES) -name "*.py" -exec sh -c 'mkdir -p $(MPY_TARGET_DIR)/$$(dirname {}) && mpy-cross $(MPY_FLAGS) {} -o $(MPY_TARGET_DIR)/$$(dirname {})/$$(basename -s .py {}).mpy' \;
	@rm -rf $(MPY_SOURCES)/release_info.py
	@touch $(MPY_TARGET_DIR)/.mpy.compiled

.devdeps: Pipfile.lock
	@echo "===> Installing dependencies with pipenv"
	@$(PIPENV) sync --dev
	@touch .devdeps

devdeps: .devdeps

dist: clean-dist dockerbase
	@mkdir -p .dist
	@docker run --rm -it -v $$(pwd)/.dist:/dist kmkpy:$(TIMESTAMP)

dockerbase:
	docker build . \
		-t kmkpy:$(TIMESTAMP) \
		--build-arg KMKPY_URL=$$(cut -f1 < kmkpython_ref.tsv) \
		--build-arg KMKPY_REF=$$(cut -f2 < kmkpython_ref.tsv)

lint: devdeps
	@$(PIPENV) run flake8

fix-formatting: devdeps
	@$(PIPENV) run black .

fix-isort: devdeps
	@find kmk/ user_keymaps/ boards/ -name "*.py" | xargs $(PIPENV) run isort

clean: clean-dist
	@echo "===> Cleaning build artifacts"
	@rm -rf .devdeps build dist $(MPY_TARGET_DIR)

clean-dist:
	@echo "===> Cleaning KMKPython dists"
	@rm -rf .dist

# This is mostly a leftover from the days we vendored stuff from
# micropython-lib via submodules. Leaving this here mostly in case someone goes
# exploring through the history of KMK's repo and manages to screw up their
# repo state (those were glitchy times...)
powerwash: clean
	@echo "===> Removing vendor/ to force a re-pull"
	@rm -rf vendor
	@echo "===> Removing pipenv-managed virtual environment"
	@$(PIPENV) --rm || true

test: lint unit-tests

.PHONY: unit-tests
unit-tests: devdeps
	@$(PIPENV) run python3 -m unittest

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

copy-board: $(MOUNTPOINT)/kb.py
$(MOUNTPOINT)/kb.py: $(BOARD)
	@echo "===> Copying your board to kb.py"
	@rsync -rh $(BOARD) $@
	@sync

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

ifdef BOARD
copy-board: $(MOUNTPOINT)/kb.py
endif # BOARD

endif # MOUNTPOINT
