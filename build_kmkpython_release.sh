#!/bin/sh

TIMESTAMP=$(date +%s)
TARGETS=${TARGETS:-"nice_nano itsybitsy_nrf52840_express"}

for TARGET in ${TARGETS}; do
	make -C /opt/kmkpython/ports/nrf BOARD="${TARGET}"
	cp "/opt/kmkpython/ports/nrf/build-${TARGET}/firmware.uf2" "/dist/${TARGET}-${TIMESTAMP}.uf2"
	echo "===> Built /dist/${TARGET}-${TIMESTAMP}.uf2"
done
