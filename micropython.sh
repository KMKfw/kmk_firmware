if [ ! -f vendor/micropython/ports/unix/micropython ]; then
	echo "Run make micropython-build-unix"
	exit 1
fi

vendor/micropython/ports/unix/micropython $@
