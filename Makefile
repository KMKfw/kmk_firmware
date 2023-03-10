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
MPY_SOURCES ?= 'kmk/'
MPY_TARGET_DIR ?= .compiled
PY_KMK_TREE = $(shell find $(MPY_SOURCES) -name "*.py")
DIST_DESCRIBE = $(shell $(DIST_DESCRIBE_CMD))

TIMESTAMP := $(shell date +%s)

all: copy-kmk copy-bootpy copy-keymap copy-board

.PHONY: compile compile-check
compile: compile-check
ifeq ($(MPY_CROSS),)
compile-check:
	@echo "===> Could not find mpy-cross in PATH, exiting"
	@false
else
compile-check: $(PY_KMK_TREE:%.py=$(MPY_TARGET_DIR)/%.mpy)
	@echo "===> Compiling all py files to mpy with flags $(MPY_FLAGS)"
$(MPY_TARGET_DIR)/%.mpy: %.py
	@mkdir -p $(dir $@)
	@$(MPY_CROSS) $(MPY_FLAGS) $? -o $@
endif

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
	@find boards/ kmk/ tests/ user_keymaps/ -name "*.py" | xargs $(PIPENV) run isort

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
	@$(PIPENV) run python3 -m unittest $(TESTS)

reset-bootloader:
	@echo "===> Rebooting your board to bootloader (safe to ignore file not found errors)"
	@-timeout -k 5s 10s $(PIPENV) run ampy -p /dev/ttyACM0 -d ${AMPY_DELAY} -b ${AMPY_BAUD} run util/bootloader.py

reset-board:
	@echo "===> Rebooting your board (safe to ignore file not found errors)"
	@-timeout -k 5s 10s $(PIPENV) run ampy -p /dev/ttyACM0 -d ${AMPY_DELAY} -b ${AMPY_BAUD} run util/reset.py


ifdef MOUNTPOINT
ifdef BOARD
copy-board:
	@echo "===> Copying your board from $(BOARD) to $(MOUNTPOINT)"
	@rsync -rhu $(BOARD)/*.py $(MOUNTPOINT)/
	@sync
else # BOARD
copy-board:
	@echo "**** Missing BOARD argument ****" && exit 1
endif # BOARD

copy-bootpy:
	@echo "===> Copying required boot.py"
	@rsync -rhu boot.py $(MOUNTPOINT)/boot.py
	@sync

copy-compiled:
	@echo "===> Copying compiled KMK folder"
	@rsync -rhu $(MPY_TARGET_DIR)/* $(MOUNTPOINT)/
	@sync

ifdef USER_KEYMAP
copy-keymap:
	@echo "===> Copying your keymap to main.py"
	@rsync -rhu $(USER_KEYMAP) $(MOUNTPOINT)/main.py
	@sync
else # USER_KEYMAP
copy-keymap:
	@echo "**** Missing USER_KEYMAP argument ****" && exit 1
endif # USER_KEYMAP

copy-kmk:
	@echo "===> Copying KMK source folder"
	@rsync -rhu kmk $(MOUNTPOINT)/
	@sync

else # MOUNTPOINT
copy-board copy-bootpy copy-compiled copy-keymap copy-kmk:
	@echo "**** MOUNTPOINT must be defined (wherever your CIRCUITPY drive is mounted) ****" && exit 1
endif # ifndef MOUNTPOINT
