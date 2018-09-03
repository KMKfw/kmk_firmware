.PHONY: build-feather devdeps lint

devdeps: Pipfile.lock
	pipenv install --dev --ignore-pipfile

lint: devdeps
	pipenv run flake8

build-feather-test: lint devdeps
	@echo "===> Pulling dependencies, this may take several minutes"
	@git submodule update --init --recursive
	@echo "===> Building circuitpython/mpy-cross"
	@make -C vendor/circuitpython/mpy-cross
	@echo "===> Pulling Nordic BLE stack"
	@cd vendor/circuitpython/ports/nrf && ./drivers/bluetooth/download_ble_stack.sh 2>/dev/null
	@echo "===> Preparing KMK source for bundling into CircuitPython"
	@rm -rf vendor/circuitpython/ports/nrf/freeze/kmk
	@cp -av kmk vendor/circuitpython/ports/nrf/freeze
	@echo "===> Building CircuitPython with KMK"
	make -C vendor/circuitpython/ports/nrf BOARD=feather_nrf52832 SERIAL=/dev/ttyUSB0 SD=s132 FROZEN_MPY_DIR=freeze clean dfu-gen dfu-flash
	@echo "===> Pushing keyboard config"
	sleep 2
	-pipenv run ampy rm main.py
	#pipenv run ampy put boards/klardotsh/twotwo_matrix_feather.py main.py
	@echo
	@echo
	@echo "IT IS NOT SAFE TO AUTOMATICALLY FLASH THIS BOARD IF YOU USE A WHILE TRUE LOOP. YOUR DEVICE CAN BECOME UNRECOVERABLE WITHOUT A JLINK"
	@echo "TRY RUNNING pipenv run ampy run boards/klardotsh/twotwo_matrix_feather.py AND WATCHING THE SERIAL OUTPUT IN ANOTHER CONSOLE"
	@echo "THAT IS CURRENTLY ALL THE KEYBOARD YOU CAN ABSOLUTELY SAFELY USE"
	@echo "I'M DISCUSSING THIS WITH THE ADAFRUIT DEVELOPERS ON DISCORD, HOPEFULLY main.py BECOMES FLASHABLE BY DFU IN THE FUTURE"
	@echo
	@echo "Okay, now that the all caps disclaimer is out of the way..."
	@echo "You can still run pipenv run ampy put boards/klardotsh/twotwo_matrix_feather.py main.py"
	@echo "Your board will probably work. However, anything depending on the Python REPL (this includes ampy) will not."
	@echo "If you do get stuck in this purgatory, run 'make oh-god-everything-is-stuck', which will flash a purposefully-failing build to your device"
	@echo "This workaround ONLY works if your keyboard script tries to import from kmk, which I sure hope it does."
	@echo "Once that process finishes, you can come back to make build-feather-test safely, or go play in the REPL, or drink."

oh-god-everything-is-stuck: lint devdeps
	@echo "===> Building a keyboard that explicitly CANNOT import KMK. Assuming your infinite-looping keyboard script imported KMK, it will now fail and be wiped. Cheers!"
	@echo "===> Pulling dependencies, this may take several minutes"
	@git submodule update --init --recursive
	@echo "===> Building circuitpython/mpy-cross"
	@make -C vendor/circuitpython/mpy-cross
	@echo "===> Pulling Nordic BLE stack"
	@cd vendor/circuitpython/ports/nrf && ./drivers/bluetooth/download_ble_stack.sh 2>/dev/null
	@echo "===> Preparing KMK source for bundling into CircuitPython"
	@rm -rf vendor/circuitpython/ports/nrf/freeze/kmk
	@echo "===> Building CircuitPython WITHOUT KMK to induce ImportError"
	make -C vendor/circuitpython/ports/nrf BOARD=feather_nrf52832 SERIAL=/dev/ttyUSB0 SD=s132 FROZEN_MPY_DIR=freeze clean dfu-gen dfu-flash
	@echo "===> Wiping keyboard config"
	sleep 2
	pipenv run ampy rm main.py
	@echo "===> Done! Fix your board script and retry flashing the right way"
