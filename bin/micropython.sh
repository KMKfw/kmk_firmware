if [ ! -f build/micropython/ports/unix/micropython ]; then
	echo "Run make micropython-build-unix"
	exit 1
fi

build/micropython/ports/unix/micropython $@
